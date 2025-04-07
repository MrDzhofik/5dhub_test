import os

from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import RedirectResponse
import secrets
from pydantic import BaseModel
from typing import Dict
import httpx
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

url_database: Dict[str, str] = {}

class URLRequest(BaseModel):
    url: str


@app.post("/", status_code=status.HTTP_201_CREATED)
async def shorten_url(url_request: URLRequest) -> Dict[str, str]:
    """
    Shorten a given URL and return a unique identifier for it.
    """
    short_id = secrets.token_urlsafe(6)

    url_database[short_id] = url_request.url

    return {"short_url_id": short_id}

@app.get("/async-service")
async def call_async_service(request: Request) -> dict:
    """
    Make an async request to weather service and return the data.
    """
    try:
        async with httpx.AsyncClient() as client:

            service_url = os.getenv("WEATHER_URL")

            response = await client.get(service_url)

            return response.json()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calling external service: {str(e)}"
        )

@app.get("/{short_id}")
async def redirect_to_original(short_id: str):
    """
    Redirect to the original URL using the shortened identifier.
    """
    original_url = url_database.get(short_id)
    if not original_url:
        raise HTTPException(status_code=404, detail="URL not found")

    return RedirectResponse(url=original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)





if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
