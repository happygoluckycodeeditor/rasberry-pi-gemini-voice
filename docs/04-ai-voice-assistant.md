# 04 — Build the AI voice assistant (LCD + button + voice)

This guide explains how `ai_assistant.py` works and how to run it on a Raspberry Pi.

It combines:

- **Microphone input** → records `input.wav`
- **OpenAI speech-to-text** → transcribes audio into text
- **Gemini** → generates a short reply
- **Tool calling** (weather) → Gemini can call a Python function
- **LCD output** → displays the response on a 16x2 screen
- **Button/switch** → starts an interaction

## The “contract” (what the assistant expects)

Inputs:
- Press/flip a switch connected to **GPIO17**
- A microphone available to `arecord`

Outputs:
- A 16x2 LCD shows status (“Listening…”, “Thinking…”, etc.) and the final answer

Error modes:
- Missing API keys → authentication errors
- Wrong audio device → `arecord` fails
- Wrong I2C address/wiring → LCD errors (I/O error)

## Hardware checklist (before running)

Make sure you already completed:

- `docs/02-i2c-lcd-screen.md` (LCD wired + address known)
- `docs/03-button-or-switch.md` (button wired to GPIO17)

## Software setup

### 1) Install OS packages

On the Pi:

```bash
sudo apt update
sudo apt -y install python3-pip python3-venv i2c-tools alsa-utils
```

### 2) Create a virtual environment + install Python deps

From the repo folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip

pip install gpiozero RPLCD requests openai google-genai
```

### 3) Add API keys

You need both:

- `OPENAI_API_KEY` (for transcription)
- `GEMINI_API_KEY` (for Gemini replies + tool calling)

Set them in your shell profile (example):

```bash
export OPENAI_API_KEY="..."
export GEMINI_API_KEY="..."
```

Then reload your shell or run `source ...`.

## Configure `ai_assistant.py`

Open `ai_assistant.py` and check the **CONFIG** section.

### Audio device

Your script uses:

- `ARECORD_DEVICE = "plughw:2,0"`

That’s specific to *your* microphone enumeration.

On your Pi, list capture devices:

```bash
arecord -l
```

You’ll see output like:

- `card 2: ... device 0: ...`

Update `ARECORD_DEVICE` to match the card/device you see.

### Recording length

- `RECORD_SECONDS = 6`

Increase if you want longer questions.

### LCD address

- `LCD_I2C_ADDR = 0x27`

Check with:

```bash
i2cdetect -y 1
```

If you see `3f` instead, change it to `0x3f`.

## How it works (quick tour)

### 1) Record audio with `arecord`

`record_audio()` runs:

- `arecord -D <device> -f cd -t wav -d <seconds> -q input.wav`

### 2) Speech-to-text (OpenAI)

`transcribe_with_openai()` calls:

- `oai_client.audio.transcriptions.create(model="gpt-4o-transcribe", ...)`

It returns plain text.

### 3) Gemini + tool calling

`gemini_with_tools(user_text)` does:

1. Ask Gemini: “Do you want to call a tool?”
2. If Gemini requests `get_weather(location=...)`, run your Python function.
3. Send the tool result back to Gemini.
4. Ask Gemini for the final answer.
5. Rewrite the final answer into **one short LCD-friendly sentence**.

### 4) LCD display

The script writes:
- status messages (“Listening…”, “Transcribing…”, “Thinking…”)\
- then the final reply split across 2 lines

## Run it

On the Pi, from the repo folder inside the venv:

```bash
python ai_assistant.py
```

You should see “Pi Voice Ready” on the LCD.

Flip the switch toward 3.3V (ON) to start an interaction.

## Common issues

### `arecord: main:831: audio open error`

- Wrong device string in `ARECORD_DEVICE`.
- Use `arecord -l` and update the value.

### LCD stays blank

- Turn the LCD’s contrast screw on the backpack.
- Confirm address with `i2cdetect -y 1`.

### Button never triggers

- Confirm wiring matches `pull_up=False` (switch sends 3.3V to GPIO17).
- Try the minimal `examples/button_test.py` first.

### Replies are cut off

This is intentional: the assistant rewrites to fit a 16x2 LCD (~32 chars).

If you want longer replies, remove the “Rewrite as ONE short sentence…” step in `gemini_with_tools()`.

## Optional improvements (nice beginner stretch goals)

- Add a beep or LED while recording
- Save transcripts to a log file
- Add more tools (time, timers, Wikipedia, jokes)
- Add text scrolling on the LCD for longer answers
