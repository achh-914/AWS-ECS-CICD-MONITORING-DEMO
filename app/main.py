from fastapi import FastAPI

app = FastAPI(title="AWS ECS CloudPulse API")

@app.get("/")
def read_root():
    return {"status": "online", "message": "CloudPulse Microservice is Running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
