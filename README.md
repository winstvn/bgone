# bgone 🤖
A Discord bot for removing the background from images using the [remove.bg](https://www.remove.bg/api) background removal API

[Invite this bot to your server!](https://discord.com/api/oauth2/authorize?client_id=781945733121048576&permissions=116736&scope=bot)

## Features
- You can specify more than 1 API key to extend the number of free remove.bg API calls per month.
  - The deployed app uses 10 API keys for a total of 500 free API calls per month.
- Can handle concurrent requests.

## Usage
1. Install the required libraries using pip
```
~/bgone$ pip install -r requirements.txt
```

2. Replace placeholders in ```bgone/env/.env``` with your tokens.

3. Run the bot
```
~/bgone$ python bgone_bot.py
```
