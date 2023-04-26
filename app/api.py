from fastapi import FastAPI
import uvicorn
from image import create_image

app = FastAPI()


@app.post("/")
async def send_message(body: dict):
    print(f"Creating tell... \nMessage: {body['message']}")
    create_image(body["message"])
    url = f"https://graph.facebook.com/v5.0/{ig_user_id}/media?image_url={image_url}&caption={caption}&access_token={access_token}"


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="127.0.0.1",
        reload=True,
        port=8000
    )
