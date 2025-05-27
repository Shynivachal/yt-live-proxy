from fastapi import FastAPI, Response
import subprocess

app = FastAPI()

# Replace with your YouTube live URL
YOUTUBE_URL = "https://www.youtube.com/watch?v=Ko18SgceYX8"

@app.get("/")
def root():
    return {"status": "YT proxy working"}

@app.get("/live.m3u8")
def stream():
    try:
        # Get direct stream URL using yt-dlp
        result = subprocess.run(
            ["yt-dlp", "-g", YOUTUBE_URL],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )

        stream_url = result.stdout.strip().split('\n')[-1]

        # Return in M3U format
        content = f"#EXTM3U\n#EXTINF:-1,YouTube Live\n{stream_url}"
        return Response(content, media_type="application/x-mpegURL")
    except Exception as e:
        return {"error": str(e)}
