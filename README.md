# Beep Beep Bot

This is a simple Telegram chatbot. It asks the name and his location from the user.  It provides the top 3 news and weather information of the user's area.


## Installation

This bot is created with Flask and python-telegram-bot. To check its working bot has to be deployed on Heroku server. So you should have an account on Heroku and Telegram.
 

* Create a bot in [Telegram](https://web.telegram.org/#/login). Search BotFather and follow the instructions. It will give you a bot token.
* Clone this repository.
* **This app is using some API's to get weather, and news.**
  * For Weather: [https://www.weatherbit.io/](https://www.weatherbit.io/)
  * For News: [https://newsapi.org](https://newsapi.org/) (currently it supported are 54 countries)
* Create accounts in these 2 sites and get the api key.

* Now Heroku login to Heroku account use Heroku CLI. Run Heroku login.
```
heroku login
```

* Once you logged in to the system, create an app in Heroku.
```
heroku create APPNAME --buildpack heroku/python
```
* Once app is created it will give you an app url.
* The app URL needs to be updated in the main.py file. Replace "LIVE_HEROKU_URL" with your app url. 
* and push this code to Heroku repository.
```
git push heroku master
```
* Once the build is successful. 
* Now we have to give all API keys and bot token to the app.
* 3 environment variables need to be set.
* Application is using python 3.7.6.
```
heroku config:set BOT_TOKEN="YOUR_BOT_TOKEN"
heroku config:set WEATHER_API_KEY="YOUR_WEATHER_API_KEY"
heroku config:set NEWS_API_KEY="YOUR_NEWS_API_KEY"
```
* **requirement file and Procfile is required to run the app on the server.**

* **Bot Name** : Smart bot

![Smart bot](https://i.paste.pics/7THLP.png)
**Search Deep77Bot in Telegram.**
