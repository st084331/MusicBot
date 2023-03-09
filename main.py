import telebot
import csv
import random
from telebot import types
from info import GENRES, MOODS, TOKEN

BOT = telebot.TeleBot(TOKEN)
GENRE = ''
MOOD = ''


def find_track(genre, mood):
    list = []
    with open('music.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if genre in row['genres'].split('.') and mood in row['moods'].split('.'):
                list.append(row)
    if len(list):
        return random.choice(list)['url']
    else:
        return "Нет треков с такими характеристиками."


def genre_buttons_init():
    genre_buttons = []
    for genre in GENRES:
        genre_buttons.append(genre)
    return genre_buttons


def mood_buttons_init():
    mood_buttons = []
    for mood in MOODS:
        mood_buttons.append(mood)
    return mood_buttons


@BOT.message_handler(commands=['start'])
def start(message):
    genre_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    genre_buttons = genre_buttons_init()
    for genre_button in genre_buttons:
        genre_markup.add(genre_button)
    BOT.send_message(message.chat.id, 'Здравствуйте! Для начала выберите жанр.', reply_markup=genre_markup)


@BOT.message_handler(content_types=['text'])
def bot_message(message):
    global GENRE
    global MOOD
    if message.chat.type == 'private':
        if message.text == 'Назад':
            genre_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            genre_buttons = genre_buttons_init()
            for genre_button in genre_buttons:
                genre_markup.add(genre_button)
            BOT.send_message(message.chat.id, 'Выберите жанр.', reply_markup=genre_markup)
        elif message.text in GENRES:
            GENRE = message.text
            mood_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            mood_buttons = mood_buttons_init()
            for mood_button in mood_buttons:
                mood_markup.add(mood_button)
            mood_markup.add('Назад')
            BOT.send_message(message.chat.id, 'Выберите настроение.', reply_markup=mood_markup)
        elif message.text in MOODS:
            MOOD = message.text
            genre_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            genre_buttons = genre_buttons_init()
            for genre_button in genre_buttons:
                genre_markup.add(genre_button)
            BOT.send_message(message.chat.id, find_track(GENRE, MOOD), reply_markup=genre_markup)


if __name__ == "__main__":
    BOT.polling(none_stop=True)
