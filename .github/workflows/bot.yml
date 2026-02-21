name: Bilet Kontrol

on:
  schedule:
    - cron: "*/15 * * * *"
  workflow_dispatch:

jobs:
  run-bot:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Install Chrome
        uses: browser-actions/setup-chrome@v1

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run bot
        run: python main.py
        env:
          TOKEN: ${{ secrets.TOKEN }}
          CHAT_ID: ${{ secrets.CHAT_ID }}
