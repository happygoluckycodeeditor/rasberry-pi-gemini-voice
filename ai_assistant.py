import subprocess
import time
import requests

from gpiozero import Button
from openai import OpenAI
from google import genai
from google.genai import types
from RPLCD.i2c import CharLCD

# =========================
# CONFIG
# =========================
AUDIO_PATH = "input.wav"
ARECORD_DEVICE = "plughw:2,0"   # Blue Yeti: card 2, device 0 (from arecord -l)
RECORD_SECONDS = 6              # recording length per interaction
SWITCH_GPIO = 17                # GPIO17 (Pin 11)

LCD_I2C_ADDR = 0x27             # from i2cdetect
LCD_COLS = 16
LCD_ROWS = 2

GEMINI_MODEL = "gemini-2.5-flash"
OPENAI_STT_MODEL = "gpt-4o-transcribe"


# =========================
# CLIENTS
# =========================
oai_client = OpenAI()           # uses OPENAI_API_KEY from env
gem_client = genai.Client()     # uses GEMINI_API_KEY from env


# =========================
# LCD
# =========================
lcd = CharLCD(
    i2c_expander="PCF8574",
    address=LCD_I2C_ADDR,
    port=1,
    cols=LCD_COLS,
    rows=LCD_ROWS,
    charmap="A02",
)

def lcd_message(line1: str = "", line2: str = ""):
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string(line1[:LCD_COLS])
    lcd.cursor_pos = (1, 0)
    lcd.write_string(line2[:LCD_COLS])

def split_for_lcd(text: str) -> tuple[str, str]:
    # keep it simple and robust
    t = (text or "").strip().replace("\n", " ")
    return t[:LCD_COLS], t[LCD_COLS:LCD_COLS*2]


# =========================
# SWITCH
# =========================
button = Button(SWITCH_GPIO, pull_up=False)  # internal pulldown; switch connects 3.3V to GPIO


# =========================
# AUDIO
# =========================
def record_audio():
    cmd = [
        "arecord",
        "-D", ARECORD_DEVICE,
        "-f", "cd",
        "-t", "wav",
        "-d", str(RECORD_SECONDS),
        "-q",
        AUDIO_PATH,
    ]
    subprocess.run(cmd, check=True)


# =========================
# OPENAI STT
# =========================
def transcribe_with_openai(audio_path: str) -> str:
    with open(audio_path, "rb") as f:
        transcription = oai_client.audio.transcriptions.create(
            model=OPENAI_STT_MODEL,
            file=f,
            response_format="text",
        )
    return transcription


# =========================
# TOOL: WEATHER (Open-Meteo)
# =========================
def get_weather(location: str) -> dict:
    """
    Returns a compact dict with current temperature & wind for a location.
    Uses Open-Meteo geocoding + forecast. No API key needed.
    """
    try:
        # Geocode city name to lat/lon
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": location, "count": 1, "language": "en", "format": "json"},
            timeout=6,
        )
        geo.raise_for_status()
        gdata = geo.json()

        if not gdata.get("results"):
            return {"ok": False, "error": f"Unknown location: {location}"}

        loc = gdata["results"][0]
        lat, lon = loc["latitude"], loc["longitude"]
        name = loc.get("name", location)
        country = loc.get("country_code", "")

        # Current weather
        w = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,wind_speed_10m",
                "timezone": "auto",
            },
            timeout=6,
        )
        w.raise_for_status()
        current = (w.json() or {}).get("current", {})

        return {
            "ok": True,
            "location": f"{name} ({country})" if country else name,
            "temperature_c": current.get("temperature_2m"),
            "wind_mps": current.get("wind_speed_10m"),
            "time": current.get("time"),
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


# =========================
# GEMINI FUNCTION CALLING SETUP
# =========================
weather_decl = {
    "name": "get_weather",
    "description": "Get current weather for a given city (temperature and wind).",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City name like 'Tokyo' or 'New York'.",
            }
        },
        "required": ["location"],
    },
}

tools = types.Tool(function_declarations=[weather_decl])
tool_config = types.GenerateContentConfig(tools=[tools])

def gemini_with_tools(user_text: str) -> str:
    """
    Ask Gemini. If Gemini requests a function call, execute it and return final short answer.
    """
    contents = [types.Content(role="user", parts=[types.Part(text=user_text)])]

    # First call: Gemini decides whether to call a tool
    resp = gem_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents,
        config=tool_config,
    )

    # Search for a function_call in returned parts
    tool_call = None
    for part in resp.candidates[0].content.parts:
        if part.function_call:
            tool_call = part.function_call
            break

    # If no tool call, return a short direct answer
    if not tool_call:
        # Force LCD-friendly style
        short = gem_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=(
                "Reply in ONE short sentence for a 16x2 LCD (max ~32 characters). "
                "No newlines. Answer the user.\n"
                f"User: {user_text}"
            ),
        )
        return (short.text or "").strip()

    # Execute tool
    if tool_call.name == "get_weather":
        result = get_weather(**tool_call.args)
    else:
        result = {"ok": False, "error": f"Unknown tool: {tool_call.name}"}

    # Send tool result back to Gemini
    function_response_part = types.Part.from_function_response(
        name=tool_call.name,
        response={"result": result},
    )

    contents.append(resp.candidates[0].content)  # include Gemini tool-call message
    contents.append(types.Content(role="user", parts=[function_response_part]))

    final = gem_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents,
        config=tool_config,
    )

    # Make it short for LCD
    short = gem_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=(
            "Rewrite the following as ONE short sentence for a 16x2 LCD "
            "(max ~32 characters). No newlines.\n"
            f"Text: {final.text}"
        ),
    )
    return (short.text or "").strip()


# =========================
# MAIN LOOP
# =========================
def main():
    lcd_message("Pi Voice Ready", "Flip switch to talk")
    print("Pi Voice Assistant ready.")
    print("Slide switch toward 3.3V to start (ON).")

    while True:
        button.wait_for_press()
        print("Switch ON detected! Starting interaction...")

        try:
            lcd_message("Listening...", "")
            record_audio()

            lcd_message("Transcribing...", "")
            text = transcribe_with_openai(AUDIO_PATH)
            print("User said:", text)

            if not text.strip():
                lcd_message("No speech", "Try again")
                time.sleep(2.5)
                lcd_message("Pi Voice Ready", "Flip switch to talk")
                button.wait_for_release()
                continue

            lcd_message("Thinking...", "")
            answer = gemini_with_tools(text)
            print("Assistant:", answer)

            line1, line2 = split_for_lcd(answer)
            lcd_message(line1, line2)
            time.sleep(6)

        except Exception as e:
            print("Error:", e)
            lcd_message("Error", str(e)[:16])
            time.sleep(3)

        lcd_message("Pi Voice Ready", "Flip switch to talk")
        print("Interaction finished. Waiting for next switch...")
        button.wait_for_release()


if __name__ == "__main__":
    main()
