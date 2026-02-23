"""Mock backend for demo/visualization without a webcam."""
import time
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulated parking state
parking_state = {"cars": 1}


def get_mock_results():
    # Randomly change parking state occasionally for demo purposes
    if random.random() < 0.3:
        parking_state["cars"] = random.choice([0, 1, 2])

    cars = parking_state["cars"]
    spots_available = max(0, 2 - cars)

    return {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "cars_detected": cars,
        "spots_available": spots_available,
        "image_with_boxes": "",
    }


@app.get("/latest_results")
async def get_latest_results():
    return JSONResponse(content=get_mock_results())


@app.get("/")
async def serve_frontend():
    with open("/home/user/ev_smart_parking/index.html", "r") as f:
        html = f.read()
    return HTMLResponse(content=html)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
