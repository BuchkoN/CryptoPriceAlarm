# CryptoPriceAlarm

CryptoPriceAlarm is a telegram bot, the main task of the bot is to inform when the cryptocurrency rate drops to the value the user needs, after which the bot will send him a notification.
The cryptocurrency exchange rate is provided by the Binance API.

## Installation

The application is launched using [Docker](https://www.docker.com/).

To launch the bot, you will need to get a [token](https://t.me/BotFather) for the bot's telegrams. After the token is generated, it must be specified in telegram_bot\bot\settings.py
```python
TOKEN = '' #Enter your token for the bot
```

Now you can run the application, to do this, enter the command in the working directory of the project:
```cmd
docker-compose up --build
```
## Further planned
1. Transfer a bot from polling to a web hook.
2. To work out the delisting of cryptocurrencies on binance.
