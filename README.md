# unrestrict-bot

This is a bot to get content from restricted telegram content.

# Supported Media

- Images
- Video/mp4
- Documents (i'll be sent with 'document' name)

# How it works

Self bot that gets the message, downloads and send it using the bot.

# Getting started

First we need to set some environment variables:

```sh
export API_HASH=""
export API_ID=""
export SESSION_STRING=""
export BOT_TOKEN=""
```

Then install the requirements with `pip install -r requirements.txt` and run `python3 main.py`

Or just build the docker image and run the container with:

```
docker run --rm -it -e API_HASH=$API_HASH -e API_ID=$API_ID -e SESSION_STRING=$SESSION_STRING -e BOT_TOKEN=$BOT_TOKEN kamuri/unrestrict-bot
```

# Getting the SESSION_STRING
Just run this script: https://github.com/kamuridesu/save-restricted-bot/blob/main/generate_session.py

If it asks you for a bot token or your number, use your number.
