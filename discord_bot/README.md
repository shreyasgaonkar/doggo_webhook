## Doggo Discord bot

You can invoke the bot to send [random dog pictures](https://www.reddit.com/r/dogpictures) on demand using ```!woof``` while running ```app.py``` in the background. This can be changed by altering the conditional statement:

```python
if message.content.startswith('!woof'):
```

Rename the ```.env_sample``` file to ```.env``` and replace the value of ```TOKEN``` for your bot application from https://discord.com/developers:

```
TOKEN=DISCORD-BOT-TOKEN
```

Run the bot using ```python bot.py``` and call it using the invoke command set: ```!woof```

### See in action:
![Discord](/img/discord_bot.PNG)
