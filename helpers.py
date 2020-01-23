import messages
import os
import json
import requests
import time

WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]
NEWS_API_KEY = os.environ["NEWS_API_KEY"]

country_codes = {
    "united arab emirates": "ae",
    "argentina": "ar",
    "austria": "at",
    "australia": "au",
    "belgium": "be",
    "bulgaria": "bg",
    "brazil": "br",
    "canada": "ca",
    "switzerland": "ch",
    "china": "cn",
    "colombia": "co",
    "cuba": "cu",
    "czechia": "cz",
    "germany": "de",
    "egypt": "eg",
    "france": "fr",
    "greece": "gr",
    "hong kong": "hk",
    "hungary": "hu",
    "indonesia": "id",
    "ireland": "ie",
    "israel": "il",
    "india": "in",
    "italy": "it",
    "japan": "jp",
    "korea": "kr",
    "lithuania": "lt",
    "latvia": "lv",
    "morocco": "ma",
    "mexico": "mx",
    "malaysia": "my",
    "nigeria": "ng",
    "netherlands": "nl",
    "norway": "no",
    "new zealand": "nz",
    "philippines": "ph",
    "poland": "pl",
    "portugal": "pt",
    "romania": "ro",
    "serbia": "rs",
    "russian federation": "ru",
    "saudi arabia": "sa",
    "sweden": "se",
    "singapore": "sg",
    "slovenia": "si",
    "slovakia": "sk",
    "thailand": "th",
    "turkey": "tr",
    "taiwan": "tw",
    "ukraine": "ua",
    "united states of america": "us",
    "venezuela": "ve",
    "south africa": "za",
}


def get_reply(query, chat_id, user_id):
    """All the messages added by user can be handled here.
    :param query:
    :param chat_id:
    :param user_id:
    :return:
    """
    time.sleep(1.5)
    try:
        if query == "hi" or query.lower() == "hi" or query.lower() == "hello":
            return "HI ! I am a chat bot. Please enter your name in @name format"
        elif "@" in query and query.count("@") == 1:
            name = query.split("@")[1]
            if name and len(name) > 0:
                return "Hi {}. I am a Beep Beep Bot. I can give you details of the weather and news of your location. Can you please enter your location in #city,country format.".format(
                    name
                )
            else:
                return "Please Try Again. Use /start to start the process."
        elif (
            "#" in query
            and query.count("#") == 1
            and query.split("#")[1] != ""
            and "," in query.split("#")[1]
        ):
            location = query.split("#")[1]
            city, country = location.split(",")
            check_updated_location(user_id, city, country)
            return "Thanks for sharing your location. Your location is {}, {}. To know the top 3 news and weather of your location you can use /news and /weather respectively.".format(
                city, country
            )
        else:
            return "Please Try Again. Use /start to start the process."
    except Exception as e:
        return messages.exception_msg


def read_locations():
    """It reads the locations json file.
    it returns a list of locations.
    :return locations:
    """
    file_path = "location.json"

    if os.stat(file_path).st_size > 0:
        with open("location.json") as f:
            file_obj = f.read()
            if file_obj != "{}":
                json_obj = json.loads(file_obj)
                return json_obj["locations"]
            else:
                return None
    else:
        return None


def get_user_location(user_id):
    """It takes the user id. It will send the country and city of the user from location json file.
    it returns city and country if record exists.
    :param user_id:
    :return location city, country:
    """
    stored_locations = read_locations()
    if stored_locations:
        for stored_location in stored_locations:
            if stored_location["user_id"] == user_id:
                return (
                    stored_location["city"].strip(),
                    stored_location["country"].strip(),
                )
                break
        else:
            return None
    else:
        return None


def add_in_locations(user_id, city, country):
    """If the user location does not exists in the json file or file is empty
    It will add the user information in json file.
    :param user_id:
    :param city:
    :param country:
    :return:
    """
    data = {"locations": []}

    stored_location = read_locations()

    if stored_location:
        stored_location.append({"user_id": user_id, "city": city, "country": country})
    else:
        stored_location = [{"user_id": user_id, "city": city, "country": country}]

    data["locations"] = stored_location

    with open("location.json", "w") as f:
        json.dump(data, f)


def update_in_locations(user_id, city, country):
    """If the user location exists in the json file but city or country is updated.
    It will update the user information in json file.
    :param user_id:
    :param city:
    :param country:
    :return:
    """
    data = {"locations": []}

    stored_locations = read_locations()
    for stored_location in stored_locations:
        if stored_location["user_id"] == user_id:
            stored_location["city"] = city
            stored_location["country"] = country
    else:
        data["locations"] = stored_locations

        with open("location.json", "w") as f:
            json.dump(data, f)


def check_updated_location(user_id, city, country):
    """This function is called when location is added.
    It will check if user info exists in the file.
    If record not exists it will add the info or if info present.
    it will update the information only if city or country is changed.
    :param user_id:
    :param city:
    :param country:
    :return:
    """
    stored_locations = read_locations()
    if stored_locations:
        for stored_location in stored_locations:
            if stored_location["user_id"] == user_id:
                if (
                    stored_location["city"] != city
                    or stored_location["country"] != country
                ):
                    update_in_locations(user_id, city, country)
                    break
                else:
                    break
        else:
            add_in_locations(user_id, city, country)
    else:
        add_in_locations(user_id, city, country)


def get_weather(city):
    """
    This function calls an api with city name and returns the weather of the location.
    :param city:
    :return Weather string:
    """
    try:
        url = "https://api.weatherbit.io/v2.0/current?city={}&key={}".format(
            city, WEATHER_API_KEY
        )
        response = requests.get(url=url)
        if response.status_code == 200:
            results = json.loads(response.text)
            msg = "The weather of {} is {}. \nThe wind speed is {} m/s and temperature is {} °C.".format(
                city,
                results["data"][0]["weather"]["description"],
                results["data"][0]["wind_spd"],
                results["data"][0]["temp"],
            )
            return msg
        else:
            return messages.location_error
    except Exception as e:
        return messages.exception_msg


def get_country_code(country):
    """
    :param country:
    :return country code:
    This function is used to return country code present on country code dict.
    """
    if country.lower() in country_codes.keys():
        return country_codes[country.lower()]
    else:
        return None


def get_news(country):
    """
    :param country:
    :return News as string:
    This function is used to return news.
    """
    try:
        code = get_country_code(country)

        if code:
            url = "https://newsapi.org/v2/top-headlines?country={}&apiKey={}&pageSize=3".format(
                code, NEWS_API_KEY
            )
            response = requests.get(url)

            if response.status_code == 200:
                results = json.loads(response.text)
                news = ""
                for article in results["articles"]:
                    news += "* {} \n\n".format(article["description"])

                return news
            else:
                return messages.exception_msg
        else:
            return messages.country_err_msg
    except Exception as e:
        return messages.exception_msg
