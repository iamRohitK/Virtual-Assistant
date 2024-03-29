from decouple import config
import requests 
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib

EMAIL = config('EMAIL')
PASSWORD = config('PASSWORD')
NEWS_API_KEY = config('NEWS_API_KEY')
OPEN_WEATHER_APP_ID = config('OPEN_WEATHER_APP_ID')
TMDB_API_KEY = config('TMDB_API_KEY')

def find_my_ip():
    # ipify provides a simple public ip address API. We just need to make a GET request on the URL provided by ipify
    ip_address = requests.get('https://api.ipify.org?format=json').json()
    return ip_address["ip"]

def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences = 2)
    return results

def play_on_youtube(video):
    kit.playonyt(video)

def search_on_google(query):
    kit.search(query)

def send_whatsapp_message(number, message):
    try:
        # To understand the reason for (It is just copying the message in the text field of recipient but it is not sent automatically).
        # error, check this out: https://github.com/Ankit404butfound/PyWhatKit/issues/20
        kit.sendwhatmsg_instantly(f"+91{number}", message)  
        return True
    except:
        return False

def send_email(receiver_address, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email['Subject'] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)   # initialize connection to our email server
        s.starttls()    # tell server we want to communicate with TLS encryption
        s.login(EMAIL, PASSWORD)   # login to our email server.
        s.send_message(email)
        s.close()   # don't forget to close the connection
        return True
    except Exception as e:
        print(e)
        return False

def get_latest_news():
    news_headline = []
    res = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general").json()  
    articles = res['articles']
    for article in articles:
        news_headline.append(article['title'])
    return news_headline[:5]

def get_weather_report(city):
    res = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER_APP_ID}&units=metric").json()
    weather = res['weather'][0]['main']
    temperature = res['main']['temp']
    feels_like = res['main']['feels_like']
    return weather, f"{temperature}°C", f"{feels_like}°C"   # Press and hold the ALT key and type the number 0176 to make a degree sign.

def get_trending_movies():
    trending_movies = []
    res = requests.get(f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}").json()
    results = res["results"]
    for r in results:
        trending_movies.append(r["original_title"])
    return trending_movies[:5]

def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']