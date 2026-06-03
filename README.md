# AudioEnhancement — Full Stack Project

A web app that takes a YouTube URL, downloads the audio, runs non-stationary noise reduction, and gives back a clean WAV file — ready to download and play.

**Stack:** FastAPI · yt-dlp · librosa · noisereduce · soundfile · Vanilla HTML/CSS/JS

---

## Prerequisites

Before you start, make sure you have:

- **Python 3.10 or higher** — check with `python --version`
- **Git** — check with `git --version`
- **FFmpeg** — installation steps are below

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/ayushpandey78001-creator/AudioEnhancement-FullStackProject.git
cd AudioEnhancement-FullStackProject
```

---

## Step 2 — Install FFmpeg

FFmpeg is required by yt-dlp to extract audio from YouTube. Follow the steps for your OS.

### Windows

1. Go to **https://www.gyan.dev/ffmpeg/builds/**
2. Download `ffmpeg-release-essentials.zip`
3. Extract it to `C:\ffmpeg` so the structure looks like:
   ```
   C:\ffmpeg\
       bin\
           ffmpeg.exe
           ffprobe.exe
   ```
4. Add FFmpeg to your system PATH:
   - Press `Win + S` → search **Environment Variables**
   - Click **Edit the system environment variables**
   - Click **Environment Variables**
   - Under **System variables** → select **Path** → click **Edit**
   - Click **New** → enter `C:\ffmpeg\bin`
   - Click **OK** on all windows
5. **Restart your terminal**, then verify:
   ```powershell
   ffmpeg -version
   ```

### macOS

```bash
brew install ffmpeg
ffmpeg -version
```

> If you don't have Homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

### Linux / WSL (Ubuntu)

```bash
sudo apt update && sudo apt install ffmpeg -y
ffmpeg -version
```

---

## Step 3 — Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows (PowerShell)**
```powershell
venv\Scripts\activate
```

**macOS / Linux / WSL**
```bash
source venv/bin/activate
```

> Your terminal prompt will change to show `(venv)` when it is active. You need to activate it every time you open a new terminal.

---

## Step 4 — Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs: `fastapi`, `uvicorn`, `yt-dlp`, `librosa`, `noisereduce`, `soundfile`, `python-multipart`.

Takes 1–3 minutes depending on your internet speed.

---

## Step 5 — Run the App

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

You should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

Open your browser and go to:

```
http://localhost:8000
```

Paste any YouTube URL, click **Enhance**, and download the cleaned WAV file.

---

## Project Structure

```
AudioEnhancement-FullStackProject/
├── main.py              ← FastAPI backend (audio pipeline)
├── requirements.txt     ← Python dependencies
├── final.ipynb          ← Original Colab notebook (reference)
├── static/
│   └── index.html       ← Frontend UI
└── README.md
```

---

## How It Works

1. You paste a YouTube URL into the frontend
2. The backend uses **yt-dlp** to download the best quality audio as MP3
3. **librosa** loads the audio at its native sample rate
4. **noisereduce** runs a non-stationary spectral gating pass to remove background noise
5. **soundfile** writes the cleaned output as a lossless WAV
6. The file is served back to your browser for playback and download

---

## Common Errors & Fixes

| Error | Fix |
|---|---|
| `Could not import module "main"` | You are in the wrong folder. Run `cd AudioEnhancement-FullStackProject` first |
| `ffprobe and ffmpeg not found` | FFmpeg is not installed or not on PATH. Follow Step 2 again and restart your terminal |
| `Directory 'static' does not exist` | Make sure `index.html` is inside a `static/` folder next to `main.py` |
| `ModuleNotFoundError` | You forgot to activate the venv. Run the activate command from Step 3 |
| Port 8000 already in use | Run on a different port: `uvicorn main:app --port 8001` |

---

## Stopping the Server

Press `Ctrl + C` in the terminal to stop the server.

---

## Dataset Reference

Original noisy audio used for testing: https://www.youtube.com/watch?v=mLyOj_QD4a4
