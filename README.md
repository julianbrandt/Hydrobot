# Hydrobot

A discord chatbot for generating memes from predefined templates.

## Install and run

```bash
git clone https://github.com/julianbrandt/Hydrobot && cd Hydrobot

python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
echo "HYDROBOT_TOKEN=your_discord_bot_token" > ".env"

python hydrobot.py
```

## Commands

Current slash-commands:
* `meme_<template>` where `<template>` is replaced with the name of the template. You can browse the available templates through autocomplete, or in `meme_templates.py`
