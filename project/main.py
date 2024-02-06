from fastapi import FastAPI, responses


app = FastAPI()


@app.get("/")
async def get_app():
    return {"message": "Hello world!"}