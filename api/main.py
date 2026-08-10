from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def home():

    return {
        "message":"AI Agent API running"
    }