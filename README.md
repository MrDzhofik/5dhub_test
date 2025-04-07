# FastAPI app
1) First, you need to make docker image from Dockerfile with command
```docker build -t 5dhub_test .```
2) Then run it
```docker run -d -p 8080:8080 --name myapp 5dhub_test```
3) Go to http://localhost:8080/docs
4) For posting url use this command

```curl -X POST http://127.0.0.1:8080/ -H "Content-Type: application/json" -d '{"url":"https://example.com"}'```
5) Copy output of this command, it will be url-id
6) Go to http://localhost:8080/{url-id}
7) For making async service request go to http://localhost:8080/async-service