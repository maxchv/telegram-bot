# Simple telegram bot demo

To start:

1. Make virtual environment (require python 3.7). Install modules pyTelegramBotAPI, django and others by command:

    ``` cmd
    pip install -r  .\requirements.txt
    ```

2. Creat your bot by @Botfather, create file `tokens.py` and put token into value `telegram`
3. Prepare service:

    ```cmd
    python manage.py makemigrations
    python manage.py migrate
    python manage.py loaddate mydata.json
    ```

4. Start rest service from lunchbot:

    ```cmd
    python manage.py runserver
    ```

5. Start telegram bot: `python bot.py`
6. Enjoy

## Usefull links

* [Пишем ботов для Telegram на языке Python](https://mastergroosha.github.io/telegram-tutorial/)
* [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
