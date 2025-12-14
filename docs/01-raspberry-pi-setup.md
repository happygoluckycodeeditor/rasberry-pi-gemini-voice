# 01 — Raspberry Pi setup (Beginner-friendly)

This guide gets you from **“new Raspberry Pi”** to a working Linux system ready for **GPIO, I2C**, and Python projects.

> Works for Raspberry Pi 5 / 4 / 3. Screens look slightly different depending on model + OS version, but the steps are the same.

## What you’ll need

- Raspberry Pi (Pi 5 recommended, but any modern Pi works)
- MicroSD card (16GB+ recommended)
- Power supply (official Pi PSU strongly recommended)
- Keyboard + mouse + HDMI monitor (or a second computer for “headless” setup)
- Internet (Ethernet or Wi‑Fi)

## Step 1: Flash Raspberry Pi OS onto the SD card

1. Install **Raspberry Pi Imager** on your computer:
   - https://www.raspberrypi.com/software/
2. Insert the microSD card.
3. Open Raspberry Pi Imager:
   - **Choose Device** → select your Pi model (e.g., *Raspberry Pi 5*)
   - **Choose OS** → *Raspberry Pi OS (64-bit)* (recommended)
   - **Choose Storage** → your SD card
4. (Recommended) Click the **⚙️ settings** (or **Edit settings**) and configure:
   - Hostname (e.g. `pi-voice`)
   - Username + password
   - Wi‑Fi (SSID + password) if you’ll use Wi‑Fi
   - Enable SSH (very handy)
5. Click **Write**.

## Step 2: First boot

1. Put the SD card into the Pi.
2. Connect HDMI + keyboard/mouse (or boot headless if you enabled SSH).
3. Power on.
4. Finish any welcome wizard.

## Step 3: Update your Pi

Open a terminal and run:

```bash
sudo apt update
sudo apt -y full-upgrade
sudo reboot
```

## Step 4: Enable I2C (needed for I2C LCD screens)

### Option A (easy): GUI

- **Preferences → Raspberry Pi Configuration → Interfaces → I2C → Enable**

### Option B: Terminal

```bash
sudo raspi-config
```

Then:
- **Interface Options → I2C → Enable**

Reboot after enabling:

```bash
sudo reboot
```

## Step 5: Install common tools (recommended)

```bash
sudo apt update
sudo apt -y install \
  python3-pip python3-venv \
  i2c-tools \
  git \
  alsa-utils
```

### Quick checks

- Check I2C devices (only works after wiring your LCD):

```bash
i2cdetect -y 1
```

- List audio capture devices (useful for microphones):

```bash
arecord -l
```

## Step 6: Project folder + virtual environment (recommended)

Inside your project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

## Step 7: Python packages used by this repo

This repo’s `ai_assistant.py` uses:

- `gpiozero` (GPIO button)
- `RPLCD` (I2C LCD)
- `requests` (weather tool)
- `openai` (speech-to-text)
- `google-genai` (Gemini)

Install them:

```bash
pip install gpiozero RPLCD requests openai google-genai
```

> If you run into build issues on Raspberry Pi OS, update pip first (Step 6) and try again.

## Step 8: API keys (for the AI assistant)

You’ll need environment variables:

- `OPENAI_API_KEY`
- `GEMINI_API_KEY`

Add them to your shell (example using `~/.bashrc` or `~/.zshrc` depending on your setup):

```bash
export OPENAI_API_KEY="..."
export GEMINI_API_KEY="..."
```

Then reload:

```bash
source ~/.bashrc  # or: source ~/.zshrc
```

## Next guides

- **02 — I2C LCD screen**: wiring + simple script
- **03 — Button/switch input**: wiring + simple script
- **04 — Build the AI voice assistant**: everything together
