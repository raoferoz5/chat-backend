from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def home():
    return {"message": "Welcome Sajid"}
@app.get("/about")
def get_about():
    return {
        "project": "Chat Backend"
    }