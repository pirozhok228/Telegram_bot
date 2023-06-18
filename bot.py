import telebot
import requests
import datetime
import pytz


TOKEN = '6182433038:AAHUtxaIM3Owk2qkRZ158c_6HW48dvGTCAs'
bot = telebot.TeleBot(TOKEN)
api_service = 'https://api.weather.yandex.ru/v2/forecast'
yandex_token = 'd16b9cf0-c065-4e07-8986-090bf3c48abf'


@bot.message_handler(content_types=["text"])
def weather(message):
    params_weather = {
        'lat': '33',
        'lon': '33',
        'lang': 'ru_RU'
    }
    params_city = {
        'apikey': 'd11b06c8-971c-4d2c-8808-9346d8772e64',
        'geocode': 'Москва',
        'format': 'json'
    }
    try:
        if message.text == '/start':
            bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}, укажи город')
        elif message.text:
            params_city['geocode'] = message.text
            city = requests.get('https://geocode-maps.yandex.ru/1.x', params=params_city)
            city = city.json()
            params_weather['lon'], params_weather['lat'] = (city['response']
                                                            ['GeoObjectCollection']['featureMember'][0]
                                                            ['GeoObject']['Point']['pos'].split())
            response = requests.get(api_service, params=params_weather,
                                    headers={'X-Yandex-API-Key': 'd16b9cf0-c065-4e07-8986-090bf3c48abf'})
            response = response.json()
            condition = response['fact']['condition']
            if condition == 'clear':
                condition = 'Ясно☀'
            if condition == 'partly-cloudy':
                condition = 'Малооблачно🌤️'
            if condition == 'cloudy':
                condition = 'Облачно с прояснениями⛅'
            if condition == 'overcast':
                condition = 'Пасмурно☁'
            if condition == 'drizzle':
                condition = 'Морось🌨️'
            if condition == 'light-rain':
                condition = 'Небольшой дождь🌨️'
            if condition == 'rain':
                condition = 'Дождь🌧️'
            if condition == 'moderate-rain':
                condition = 'Умеренно сильный дождь🌧️'
            if condition == 'heavy-rain':
                condition = 'Сильный дождь🌧️'
            if condition == 'continuous-heavy-rain':
                condition = 'Длительный сильный дождь🌧️'
            if condition == 'showers':
                condition = 'Ливень🌧️'
            if condition == 'wet-snow':
                condition = 'Дождь со снегом🌧️❄️'
            if condition == 'light-snow':
                condition = 'Небольшой снег❄'
            if condition == 'snow':
                condition = 'Снег❄'
            if condition == 'snow-showers':
                condition = 'Снегопад❄'
            if condition == 'hail':
                condition = 'Град🌨️'
            if condition == 'thunderstorm':
                condition = 'Гроза⚡'
            if condition == 'thunderstorm-with-rain':
                condition = 'Дождь с грозой⛈'
            if condition == 'thunderstorm-with-hail':
                condition = 'Гроза с градом⛈'
            tz = pytz.timezone(response['info']['tzinfo']['name'])
            date = pytz.timezone('Europe/Moscow').localize(datetime.datetime.now()).astimezone(tz)
            date = date + datetime.timedelta(hours=3)
            date = date.astimezone(tz)
            day = date.strftime('%A')
            if day == 'Monday':
                day = 'Понедельник'
            if day == 'Tuesday':
                day = 'Вторник'
            if day == 'Wednesday':
                day = 'Среда'
            if day == 'Thursday':
                day = 'Четверг'
            if day == 'Friday':
                day = 'Пятница'
            if day == 'Saturday':
                day = 'Суббота'
            if day == 'Sunday':
                day = 'Воскресенье'
            bot.send_message(message.chat.id,
                             f"{str(date.strftime('%d.%m.%Y'))}, {day}, "
                             f"{str(date.strftime('%H:%M'))}\n"
                             f"Температура: {response['fact']['temp']}°C\n"
                             f"{condition}\n"
                             f"Ветер: {response['fact']['wind_speed']} м/c\n"
                             f"Давление: {response['fact']['pressure_mm']} мм рт. ст.\n"
                             f"Влажность воздуха: {response['fact']['humidity']}%\n")
    except IndexError:
        bot.send_message(message.chat.id, 'Неверно указан город')


bot.polling(none_stop=True)