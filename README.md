# Raspberry Pi Gemini Voice Assistant

Build a beginner-friendly **Raspberry Pi voice assistant** with:

- a **button / slide switch** to start listening
- an **IIC/I2C LCD 1602 (16x2)** for status + replies
- **OpenAI** speech-to-text
- **Gemini** answers + simple tool calling (weather)

The main program is `ai_assistant.py`.

## Start here (docs)

1. `docs/01-raspberry-pi-setup.md` — flash OS, update, enable I2C, install Python deps
2. `docs/02-i2c-lcd-screen.md` — wire LCD + run `examples/lcd_test.py`
3. `docs/03-button-or-switch.md` — wire a **3.3V slide switch** + run `examples/button_test.py`
4. `docs/04-ai-voice-assistant.md` — configure + run `ai_assistant.py`

## Repo layout

- `ai_assistant.py` — full assistant (record → transcribe → Gemini → LCD)
- `examples/lcd_test.py` — quick LCD sanity test
- `examples/button_test.py` — quick GPIO button/switch sanity test
- `docs/` — step-by-step beginner guides

## Notes

- Some Python imports (like `gpiozero` and `RPLCD`) will show as “missing” on your laptop. That’s normal—these are meant to run on the Raspberry Pi.
- You must set `OPENAI_API_KEY` and `GEMINI_API_KEY` to run the assistant.

## License

Add a license file if you plan to share/redistribute this project.

---

# Raspberry Pi Gemini 音声アシスタント（日本語）

このリポジトリは、初心者でも作れる **Raspberry Pi 音声アシスタント** のサンプルです。

- **ボタン／スライドスイッチ**で録音開始
- **IIC/I2C LCD 1602（16x2）** にステータスと返答を表示
- **OpenAI** で音声→テキスト（文字起こし）
- **Gemini** で回答生成＋簡単なツール呼び出し（天気）

メインのプログラムは `ai_assistant.py` です。

## まずはここから（ドキュメント）

1. `docs/01-raspberry-pi-setup.md` — Raspberry Pi OS の書き込み、更新、I2C 有効化、Python 依存関係の準備
2. `docs/02-i2c-lcd-screen.md` — LCD の配線＋ `examples/lcd_test.py` で動作確認
3. `docs/03-button-or-switch.md` — **3.3V スライドスイッチ**の配線＋ `examples/button_test.py` で確認
4. `docs/04-ai-voice-assistant.md` — 設定（音声デバイスなど）＋ `ai_assistant.py` の実行

## フォルダ構成

- `ai_assistant.py` — 音声録音 → 文字起こし → Gemini → LCD 表示
- `examples/lcd_test.py` — LCD の簡易テスト
- `examples/button_test.py` — GPIO ボタン／スイッチの簡易テスト
- `docs/` — 手順をまとめたガイド

## 注意点

- 手元のPC（macOS/Windows）では `gpiozero` や `RPLCD` が「見つからない」と表示されることがありますが問題ありません。基本的に Raspberry Pi 上で動かす前提です。
- アシスタントを動かすには環境変数 `OPENAI_API_KEY` と `GEMINI_API_KEY` の設定が必要です。

## ライセンス

公開・再配布する場合は、必要に応じてライセンスファイルを追加してください。
