from flask import Flask, Response, stream_with_context
import subprocess
import requests
import os

app = Flask(__name__)

def get_youtube_live_url(youtube_url):
    # Use yt-dlp to get the direct live stream URL
    result = subprocess.run(['yt-dlp', '-g', youtube_url], capture_output=True, text=True)
    if result.returncode == 0:
        urls = result.stdout.strip().split('\n')
        # Return the first URL (usually the best quality live stream)
        return urls[0]
    return None

@app.route('/live')
def live():
    youtube_live_url = get_youtube_live_url('https://www.youtube.com/watch?v=Ko18SgceYX8')
    if not youtube_live_url:
        return "Failed to fetch live stream URL", 500

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Referer': 'https://www.youtube.com/'
    }

    def generate():
        with requests.get(youtube_live_url, headers=headers, stream=True) as r:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk

    return Response(stream_with_context(generate()), content_type='application/vnd.apple.mpegurl')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
