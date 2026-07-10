# AudioEnhancement — Full Stack Project

A web app that takes a YouTube URL, downloads the audio, runs it through **DeepFilterNet** AI noise removal, and gives back a mastered WAV file — ready to download and play.

**Stack:** FastAPI · yt-dlp · librosa · DeepFilterNet · Pedalboard · Vanilla HTML/CSS/JS

---

## Prerequisites

Before you start, make sure you have:

- **Python 3.10 or higher** — check with `python --version`
- **Git** — check with `git --version`
- **FFmpeg** — installation steps are below
- **(Only if the pip install fails)** a **Rust toolchain** — DeepFilterNet ships prebuilt wheels for most platforms, so plain `pip install deepfilternet` usually just works. Rust is only needed if pip has to build it from source for your OS/Python version (see Step 4 troubleshooting below).

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

This installs: `fastapi`, `uvicorn`, `yt-dlp`, `librosa`, `soundfile`, `python-multipart`, `pedalboard`, `torch`, `torchaudio`, and `deepfilternet`.

Takes 3–8 minutes depending on your internet speed (torch is the largest download).

**If `deepfilternet` fails to install** with a build/compile error (rather than a simple network timeout), it means pip couldn't find a prebuilt wheel for your platform and is trying to compile from Rust source. Install Rust first, then retry:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"
pip install maturin
pip install -r requirements.txt
```

(Windows users: install Rust via https://rustup.rs instead of the curl script.)

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

> **Note:** The first request after starting the server will be slower than the rest — DeepFilterNet's model weights load into memory on the first call and are cached for every request after that.

---

## Project Structure

```
AudioEnhancement-FullStackProject/
├── main.py              ← FastAPI backend (audio pipeline)
├── requirements.txt     ← Python dependencies
├── static/
│   └── index.html       ← Frontend UI
└── README.md
```

---

## How It Works

1. You paste a YouTube URL into the frontend
2. The backend uses **yt-dlp** to download the best quality audio as MP3
3. **librosa** resamples it to 48kHz — the sample rate DeepFilterNet requires
4. **DeepFilterNet** runs deep-learning-based noise suppression on the audio (loaded once per server process and reused across requests)
5. **Pedalboard** applies a mastering chain — highpass filter, presence-boost EQ, compression, and gain
6. **soundfile** writes the final cleaned output as a lossless WAV
7. The file is served back to your browser for playback and download

---

## Common Errors & Fixes

| Error | Fix |
|---|---|
| `Could not import module "main"` | You are in the wrong folder. Run `cd AudioEnhancement-FullStackProject` first |
| `ffprobe and ffmpeg not found` | FFmpeg is not installed or not on PATH. Follow Step 2 again and restart your terminal |
| `Directory 'static' does not exist` | Make sure `index.html` is inside a `static/` folder next to `main.py` |
| `ModuleNotFoundError` | You forgot to activate the venv. Run the activate command from Step 3 |
| `ModuleNotFoundError: No module named 'df'` | `deepfilternet` didn't install correctly — retry Step 4, and if it fails on a build step, follow the Rust toolchain instructions there |
| Build error installing `deepfilternet` | No prebuilt wheel for your platform/Python version — install Rust + `maturin` as shown in Step 4, then retry |
| Port 8000 already in use | Run on a different port: `uvicorn main:app --port 8001` |

---

## Stopping the Server

Press `Ctrl + C` in the terminal to stop the server.

---

## Dataset Reference

Original noisy audio used for testing: https://www.youtube.com/watch?v=mLyOj_QD4a4