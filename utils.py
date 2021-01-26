from os import path, listdir
from wit import Wit
import json
from datetime import date
from random import randint
from pygame import mixer

# Initiate mixer - used in audio functions
mixer.init()

access_token = "IYIKWAHYLSFGUGI3CM3SRVF4MBM2GQ7C"
client = Wit(access_token)


def convertTuple(tup):
    res = ''.join(tup)
    return res


# Look for corresponding FaceHash image if found return path of file
def face_exists(facehash):
    acceptedExt = [".jpg", ".jpeg", ".png"]
    for ext in acceptedExt:
        file = "users/faces/" + facehash + ext
        if path.isfile(file):
            # print("Found: ", file)
            return file
    print("Sorry your FaceHash does not appear to be saved.\n")
    return False


# Get the highest confidence intent
def first_intent_name(intents):
    val = intents[0]['name']
    if not val:
        return None
    return val


# Get a certain entity
def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val


# Get a certain trait
def first_trait_value(traits, trait):
    if trait not in traits:
        return None
    val = traits[trait][0]['value']
    if not val:
        return None
    return val


def getMonth(month_nr):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    return months[month_nr - 1]


def getBirthday(bday):
    date = bday.split('-')
    Y = date[0]
    M = date[1]
    M = int(M)
    D = date[2]
    msg = D + " of " + getMonth(M) + " " + Y
    return convertTuple(msg)


def calAge(bday):
    born = bday.split('-')
    today = date.today()
    today = str(today)
    today = today.split('-')
    Y = today[0]
    Y = int(Y)
    M = today[1]
    M = int(M)
    D = today[2]
    D = int(D)
    Yb = born[0]
    Yb = int(Yb)
    Mb = born[1]
    Mb = int(Mb)
    Db = born[2]
    Db = int(Db)
    return Y - Yb - ((M, D) < (Mb, Db))


def get_music_genres(genres):
    msg = ""
    last = len(genres)
    genres.pop(last - 1)
    for x in genres:
        msg += x + ","
    return msg


def recommend_random_music(genres):
    last = len(genres)
    genres.pop(last - 1)
    last = len(genres)
    index = randint(0, last - 1)
    genre = genres[index]
    response = genre + " music"
    m_path = 'music/' + genre + '/' + get_music_file(genre)
    play_music(m_path)
    return response


def recommend_music(entity_value):
    genre = entity_value
    response = genre + " music"
    m_path = 'music/' + genre + '/' + get_music_file(genre)
    play_music(m_path)
    return response


def get_music_file(genre):
    f_path = 'music/' + genre + '/'

    if listdir(f_path):
        playlist = listdir(f_path)
        index = randint(0, len(playlist) - 1)
        music_path = playlist[index]
        return music_path
    else:
        return False


def play_music(m_path):
    mixer.music.load(m_path)
    mixer.music.play()


def stop_music():
    mixer.music.unload()
    mixer.music.stop()


def replay_music():
    mixer.music.rewind()


def pause_music():
    mixer.music.pause()


def continue_music():
    mixer.music.unpause()


def lower_volume():
    mixer.music.set_volume(0.5)


def increase_volume():
    mixer.music.set_volume(1)


def mute_volume():
    mixer.music.set_volume(0)


def unmute_volume():
    mixer.music.set_volume(0.7)


def approve_response():
    responses = ['Sure!', 'Ok.', 'Sure thing.', 'Yes Sir!', 'Done!']
    index = randint(0, len(responses) - 1)
    return responses[index]


# Giving response
def give_response(wit_output, u_data):
    # Getting user data
    data = u_data[0]
    name = data['Name']
    surname = data['Surname']
    bday = data['Birthday']
    music = data['Music']
    music_genres = music.split(",")
    movies = data['Movies']
    movie_genres = movies.split(",")
    beta1 = data['Beta1']
    beta2 = data['Beta2']
    beta3 = data['Beta3']

    # print("Wit API:")
    # print(wit_output)

    # Getting intents, entities and traits from API response
    # And classifying according to intent name or trait (question, greeting, bye, thanks)
    # INIT VARIABLES
    intents = "NULL"
    entities = "NULL"
    traits = "NULL"
    # --------------------------------INTENTS----------------------------------------
    intent_type = "NULL"
    # --------------------------------ENTITIES---------------------------------------
    entity_age_of_person = "NULL"
    entity_music_genre = "NULL"
    # --------------------------------TRAITS-----------------------------------------
    trait_greeting = "NULL"
    trait_thanks = "NULL"
    trait_bye = "NULL"
    trait_sentiment = "NULL"
    trait_question = "NULL"

    understood = False
    if wit_output['intents']:
        intents = wit_output['intents']
        intent_type = first_intent_name(intents)
        understood = True
    if wit_output['entities']:
        entities = wit_output['entities']
        entity_age_of_person = first_entity_value(entities, 'wit$age_of_person:age_of_person')
        entity_music_genre = first_entity_value(entities, "music_genre:music_genre")
        understood = True
    if wit_output['traits']:
        traits = wit_output['traits']
        trait_greeting = first_trait_value(traits, 'wit$greetings')  # Values: true
        trait_thanks = first_trait_value(traits, 'wit$thanks')  # Values: true
        trait_bye = first_trait_value(traits, 'wit$bye')  # Values: true
        trait_sentiment = first_trait_value(traits, 'wit$sentiment')  # Values: positive, neutral, negative
        trait_question = first_trait_value(traits, 'question')  # Value: true, false
        understood = True
    else:
        return "Uh..."

    if understood:
        if intent_type == 'creator_related':
            return "I was created by Juled Zaganjori and Elmer Dema"
        elif intent_type == 'greeting_related' or trait_greeting == 'true':
            msg = "Hello there ", name + "!"
            return convertTuple(msg)
        elif intent_type == 'goodbye_related' or trait_bye == 'true':
            msg = "Goodbye ", name + "!"
            return convertTuple(msg)
        elif intent_type == 'name_related' and trait_question == 'true':
            msg = "Your name is ", name + "."
            return convertTuple(msg)
        elif intent_type == 'surname_related' and trait_question == 'true':
            msg = "Your surname is ", surname + "."
            return convertTuple(msg)
        elif intent_type == 'sindi_related' and trait_question == 'true':
            return "I'm your personal assistant. I'm going to help you out when you need me and cheer you up with music, videos and jokes."
        elif intent_type == 'thanks_related' or trait_thanks == 'true':
            return "Thank YOU! :)"
        elif intent_type == 'bday_related':
            msg = "You were born on ", getBirthday(bday)
            return convertTuple(msg)
        elif intent_type == 'age_related':
            if trait_question == 'true':
                msg = "You are ", calAge(bday), " years old."
                return convertTuple(msg)
            elif trait_question == 'false':
                age = entity_age_of_person.split(" ")
                age = age[0]
                age = int(age)
                if age != calAge(bday):
                    msg = "Don't be silly I know you are ", calAge(bday)
                    return convertTuple(msg)
                elif age == calAge(bday):
                    return "Yes you are."
        elif intent_type == 'music_related':
            if trait_question == 'true':
                msg = "You like listening to ", get_music_genres(music_genres), " music genres."
                return convertTuple(msg)
        elif intent_type == 'music_recommend':
            if not entity_music_genre:
                msg = "Playing ", recommend_random_music(music_genres), " for you now."
                return convertTuple(msg)
            elif entity_music_genre:
                msg = "Playing ", recommend_music(entity_music_genre), " for you now."
                return convertTuple(msg)
        elif intent_type == 'pause':
            pause_music()
            return approve_response()
        elif intent_type == 'unpause':
            continue_music()
            return approve_response()
        elif intent_type == 'stop':
            stop_music()
            return approve_response()
        elif intent_type == 'replay':
            replay_music()
            return approve_response()
        elif intent_type == 'lower_volume':
            lower_volume()
            return approve_response()
        elif intent_type == 'increase_volume':
            increase_volume()
            return approve_response()
        elif intent_type == 'mute':
            mute_volume()
            return approve_response()
        elif intent_type == 'unmute':
            unmute_volume()
            return approve_response()


def giveInput(user_input):
    data_path = "users/data/Mshsp.json"
    with open(data_path) as json_file:
        data = json.load(json_file)

    if user_input == '':
        user_input = "NULL"  # Error from wit for empty values
    wit_output = client.message(user_input)
    return give_response(wit_output, data)


'''
# Testing
data_path = "users/data/Mshsp.json"
with open(data_path) as json_file:
    data = json.load(json_file)

while True:
    user_input = input(">>>")
    if user_input == '':
        user_input = "NULL"  # Error from wit for empty values
    wit_output = client.message(user_input)
    print(give_response(wit_output, data))
'''
