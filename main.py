import os
import uuid
import asyncio
import shutil
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="AudioClear API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Works on Windows, Mac and Linux
WORK_DIR = Path(os.environ.get("TEMP", os.environ.get("TMPDIR", "/tmp"))) / "audioclear"
WORK_DIR.mkdir(parents=True, exist_ok=True)

class EnhanceRequest(BaseModel):
    url: str

def run_pipeline(job_id: str, url: str):
    import librosa
    import soundfile as sf
    import noisereduce as nr
    import yt_dlp

    job_dir = WORK_DIR / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    raw_path = str(job_dir / "raw.%(ext)s")
    output_path = str(job_dir / "enhanced.wav")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": raw_path,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "audio")

    # Find the downloaded file
    downloaded = list(job_dir.glob("raw.*"))
    if not downloaded:
        raise RuntimeError("Download failed: no audio file found")
    input_path = str(downloaded[0])

    audio_data, sample_rate = librosa.load(input_path, sr=None)
    reduced = nr.reduce_noise(y=audio_data, sr=sample_rate, stationary=False)
    sf.write(output_path, reduced, sample_rate)

    return output_path, title

@app.post("/enhance")
async def enhance(req: EnhanceRequest):
    url = req.url.strip()
    if not url:
        raise HTTPException(400, "URL is required")
    if "youtube.com" not in url and "youtu.be" not in url:
        raise HTTPException(400, "Only YouTube URLs are supported")

    job_id = str(uuid.uuid4())
    try:
        loop = asyncio.get_event_loop()
        output_path, title = await loop.run_in_executor(
            None, run_pipeline, job_id, url
        )
    except Exception as e:
        shutil.rmtree(WORK_DIR / job_id, ignore_errors=True)
        raise HTTPException(500, f"Processing failed: {str(e)}")

    return JSONResponse({"job_id": job_id, "title": title})

@app.get("/download/{job_id}")
def download(job_id: str):
    if not all(c in "0123456789abcdef-" for c in job_id):
        raise HTTPException(400, "Invalid job ID")
    output_path = WORK_DIR / job_id / "enhanced.wav"
    if not output_path.exists():
        raise HTTPException(404, "File not found")
    return FileResponse(
        str(output_path),
        media_type="audio/wav",
        filename="enhanced_audio.wav",
    )

@app.get("/health")
def health():
    return {"status": "ok"}

# Serve frontend — path relative to this file, works on any OS
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")