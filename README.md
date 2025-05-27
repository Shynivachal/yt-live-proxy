FastAPI YT Live Proxy – Deploy on Render

This project sets up a simple FastAPI-based API to stream or proxy live videos (like YouTube Live) using yt-dlp and ffmpeg. It can help you extract streams from URLs and serve them through your own Render-hosted endpoint.


---

Features

Proxy YouTube live video or other supported URLs.

Automatically fetches live stream URLs using yt-dlp.

Lightweight and free deployment on Render.com.



---

Files Structure

.
├── main.py              # FastAPI app code
├── requirements.txt     # Python dependencies
├── render.yaml          # Render build instructions
└── README.md            # This file


---

1. Requirements

A free Render account.

yt-dlp binary (installed during Render build).

Basic knowledge of Python (optional).



---

2. requirements.txt

fastapi
uvicorn


---

3. render.yaml

services:
  - type: web
    name: yt-live-proxy
    env: python
    plan: free
    buildCommand: |
      apt-get update && apt-get install -y ffmpeg wget
      wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp
      chmod a+rx /usr/local/bin/yt-dlp
      pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port 10000

This installs:

yt-dlp system-wide

ffmpeg for stream support

Python dependencies via pip



---

4. main.py (basic sample)

from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import subprocess

app = FastAPI()

@app.get("/")
def root():
    return {"status": "YT Proxy Live"}

@app.get("/stream")
def stream(url: str = Query(...)):
    command = [
        "yt-dlp",
        "-o", "-",
        "-f", "best",
        url
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    return StreamingResponse(process.stdout, media_type="video/mp4")


---

5. Deploy to Render

1. Push this code to GitHub.


2. Go to Render.com.


3. Create a new Web Service.


4. Connect your GitHub repo.


5. Render detects render.yaml and installs everything automatically.


6. Wait for build + deploy.




---

6. Usage Example

Once deployed, access:

https://your-app-name.onrender.com/stream?url=https://www.youtube.com/watch?v=xxxxxxx

Make sure:

You provide a live stream link.

You use only public URLs (not DRM or region-locked).



---

Limitations

Render free tier has bandwidth and uptime limits.

Some videos might not work due to age restriction, geoblocking, or YouTube changes.
