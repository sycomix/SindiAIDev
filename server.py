from flask import Flask, render_template, request
import pymysql
import utils
from pyowm import OWM

# OpenWeather
weatherAPI_token = "44edc82d5c54a7d0cd68aec1904e810e"
mgr = OWM(weatherAPI_token)

# initializing variables
s = 0
q = 0
facehash = ""

app = Flask(__name__)


def insert_sql(user_input):  # inserting user inputs, bot outputs and time into database
    global s
    global facehash
    s = s + 1  # ID
    resp = utils.giveInput(user_input, facehash)
    resp = str(resp)
    try:
        sql = 'INSERT INTO user_bot_chat (id, User_input, Bot_output) VALUES("' + str(
            s) + '","' + user_input + '","' + resp + '");'
        a.execute(sql)
        conn.commit()
    except Exception as e:
        print("Line 27")
        print("Exeception occured:{}".format(e))


def user_list():  # extracting user inputs from user_bot_chat database
    user = []
    sql = 'select User_input from user_bot_chat;'
    a.execute(sql)
    w_user = list(a.fetchall())
    for i in w_user:
        # user.append('You: ' + i[0])
        user.append(i[0])
    return user


def bot_list():  # extracting bot responses from user_bot_chat database
    bot = []
    sql = 'select Bot_output from user_bot_chat;'
    a.execute(sql)
    w_bot = list(a.fetchall())
    for i in w_bot:
        # bot.append('Sindi' + i[0])
        bot.append(i[0])
    return bot


@app.route('/home')  # links to the first page - index.html
def index():
    weather = getWeather()
    return render_template("index.html", user_input=r(), temp=weather[0], location=weather[1], icon=weather[2], humidity=weather[3], wind=weather[4], music=utils.music_playing())


@app.route('/')  # links to the first page - index.html
def home():
    return render_template("setup.html")


@app.route('/setup', methods=['POST'])
def setup():
    weather = getWeather()
    global facehash
    facehash= request.form["facehash"]
    return render_template("index.html", user_input=r(), temp=weather[0], location=weather[1], icon=weather[2], humidity=weather[3], wind=weather[4], music=utils.music_playing())


@app.route('/clear')
def clearChat():
    weather = getWeather()
    # Clear all table rows
    sql = "TRUNCATE TABLE user_bot_chat;"
    a.execute(sql)
    return render_template("index.html", user_input=r(), temp=weather[0], location=weather[1], icon=weather[2], humidity=weather[3], wind=weather[4], music=utils.music_playing())


def r():  # takes user inputs and bot outputs and insert into a array to later send to html file
    try:
        user_input = request.form["user_input"]
        insert_sql(user_input)
        r = []
        user = user_list()
        bot = bot_list()
        for j in range(0, len(user)):
            r.append(user[j])
            r.append(bot[j])
        return r
    except:
        r = []
        user = user_list()
        bot = bot_list()
        for j in range(0, len(user)):
            r.append(user[j])
            r.append(bot[j])
        return r


def getWeather():
    observation = mgr.weather_at_place('Shkodër')
    w = observation.get_weather()
    wind_data = w.get_wind()
    humidity = w.get_humidity()
    temp_data = w.get_temperature('celsius')
    icon = w.get_weather_icon_name()
    weatherData = [str(int(temp_data['temp'])), 'Shkodër', str(icon), str(int(humidity)), str(int(wind_data['speed']))]
    return weatherData


@app.route('/process', methods=['POST'])
def process():
    weather = getWeather()
    # called when user input is given and submit button is pressed
    return render_template("index.html", user_input=r(), temp=weather[0], location=weather[1], icon=weather[2], humidity=weather[3], wind=weather[4], music=utils.music_playing())


if __name__ == '__main__':
    try:  # connects to the database
        conn = pymysql.connect(host='localhost', user='root', password='', db='sindi_db')
        a = conn.cursor()
    except Exception as e:
        print("QUERY ERROR: Connection")
        print("Exeception occured:{}".format(e))

    app.run(host='0.0.0.0', port=int('8000'), debug=True)  # 0.0.0.0.,80
    # conn.close()
    # a.close()
