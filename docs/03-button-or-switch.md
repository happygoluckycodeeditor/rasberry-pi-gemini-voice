# 03 — Connect a 3.3V slide switch / button (GPIO)

This guide shows how to connect a **button** or **slide switch** to a Raspberry Pi and read it from Python.

Your `ai_assistant.py` uses:

- `SWITCH_GPIO = 17` (GPIO17)
- `Button(SWITCH_GPIO, pull_up=False)`

That means the wiring expects:
- The GPIO pin is normally **LOW** (0V)
- It becomes **HIGH** (3.3V) when the switch is turned ON / pressed

## What you’ll need

- Raspberry Pi
- A **3.3V slide switch** (recommended) or a push button
- Jumper wires

## Safe GPIO reminder

- Raspberry Pi GPIO is **3.3V only**.
- Do **not** connect 5V directly to a GPIO input.

## Wiring option A (recommended, matches `ai_assistant.py`) — slide switch connects 3.3V → GPIO

Wire like this (exactly what you’re using):

- One side of switch → Pi **3.3V**
- Other side of switch → Pi **GPIO17** (physical pin 11)

With this wiring, when the switch closes, it sends **3.3V** to GPIO17.

### Why no resistor?

`gpiozero.Button(..., pull_up=False)` enables an **internal pull-down resistor**, which keeps the pin LOW when the switch is open.

## Wiring option B (alternate) — switch connects GPIO → GND

You *can* wire a button to ground and use `pull_up=True` (internal pull-up). That wiring is also common.

But since your assistant script uses `pull_up=False`, option A is the simplest and matches the repo.

## Install the Python library

```bash
pip install gpiozero
```

## Minimal button test script

This repo includes `examples/button_test.py`.

It:
- Waits for a press
- Prints when pressed and released

## Troubleshooting

### It’s always “pressed”

- Your wiring might be reversed (stuck at 3.3V).
- Confirm you used GPIO17 (physical pin 11), not pin 17.

### It never detects a press

- Confirm one side is **3.3V** and the other is **GPIO17**.
- If you used the alternate wiring to GND, you must also change the code to `pull_up=True`.
