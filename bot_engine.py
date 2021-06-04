# -*- coding: utf-8 -*-

# @pirog - telegram
import os
import random
import threading
import utils
import config
import telebot
from telebot import types
import hash_image

bot = telebot.TeleBot(config.token)




""""
отправка мема в чат
"""
@bot.message_handler(commands=['mem'])
def lession(message):

        chat_id = message.chat.id
        x = utils.get_id_photo_for_chat(chat_id)

        if x == None: return
        # Выбираем случайный элемент списка
        photo_id = x[random.randrange(0, len(x), 1)]
        # Отсылаем в чат
        bot.send_photo(message.chat.id, photo=photo_id)


    #достаем список сохраненных id изображений



"""
Приветствие вновь прибывших
"""

@bot.message_handler(content_types=["new_chat_members"])
def handler_new_member(message):
    #достаем имя пользователя
    user_name = message.new_chat_member.first_name
    #выбираем рандомно одно из приветствий и отправляем в чат
    random_answer=random.randrange(0, 6, 1)
    if random_answer == 0:
        bot.send_message(message.chat.id, f"Добро пожаловать, {user_name}! С новеньких по мему, местное правило (честно, всё именно так 😊)")
    elif random_answer == 1:
        bot.send_message(message.chat.id,
                         f"Привет, {user_name}! Есть местное правило с новеньких по мему. У тебя 1 час. Потом тебя удалят (честно, всё именно так 😊)")
    elif random_answer == 2:
        bot.send_message(message.chat.id,
                         f"Добро пожаловать, {user_name}! Ваше заявление об увольнениии принято отделом кадров, для отмены пришлите мем (честно, всё именно так 😊)")
    elif random_answer == 3:
        bot.send_message(message.chat.id,
                         f"Добро пожаловать, {user_name}! Подтвердите свою личность прислав мем в этот чат."
                         f" Все не идентифицированные пользователи удаляются быстро - в течении 60 лет. (честно, всё именно так 😊)")
    elif random_answer == 4:
        bot.send_message(message.chat.id,
                         f"Добро пожаловать, {user_name}! К сожалению ваше заявление на отпуск потеряно, следующий отпуск можно взять через 4 года 7 месяцев,"
                         f"для востановления заявления пришлите мем (честно, всё именно так 😊)")
    elif random_answer == 5:
        bot.send_message(message.chat.id,
                         f" 900: {user_name},Вас приветствует Служба безопасности Сбербанка. Для отмены операции 'В фонд озеленения Луны' Сумма: 34765.00 рублей, пришлите мем "
                         f"(честно, всё именно так 😊)")
    else:
        bot.send_message(message.chat.id,
                         f"Добро пожаловать, {user_name}! К сожалению ваше заявление на отпуск потеряно, следующий отпуск можно взять через 4 года 7 месяцев,"
                         f"для востановления заявления пришлите мем (честно, всё именно так 😊)")


"""Сбор фото мемов"""
@bot.message_handler(content_types=['photo'])
def handle_docs_audio(message):
        #достаем id изображения
        photo_id = message.photo[0].file_id
        #Сохраняем фото
        file_info = bot.get_file(photo_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src =  os.getcwd() + '\\images\\' + photo_id;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        #Получаем hash из фото
        hash_images=hash_image.CalcImageHash(src)
        #удаляем файл
        if os.path.isfile(src):
            os.remove(src)
        else:
            None

        #Достаем словарь хэшей, если он пуст то создаем и добавляем элемент в словарь и добавляем фото в список
        rows = utils.get_hush_photo_for_chat(message.chat.id)
        if rows == None:
            rows = dict()
            rows[hash_images]= photo_id
            utils.set_hash_photo_for_chat(message.chat.id, rows)

            answer = utils.get_answer_for_user(message.chat.id)
            if answer == None:
                answer = []

                answer.append(photo_id)

                utils.set_id_photo_for_chat(message.chat.id, answer)
            else:
                answer.append(photo_id)

        #Смотрим есть ли в нашем словаре такой хэш, проверяем на боян
        else:

                if hash_images in rows:
                    bot.send_message(message.chat.id, f"Алярм!!! Нас кормят боянами 99%")
                    bot.send_photo(message.chat.id, photo=rows.get(hash_images))

                # проверяем на 95% совпадение хэшей
                else:
                    for key in rows.keys():
                        count = hash_image.CompareHash(key,hash_images)
                        if count <= 5:
                            bot.send_message(message.chat.id, f"Ой, да боян же, совпадение более 95%")
                            bot.send_photo(message.chat.id, photo=rows.get(key))
                            break



                    #После всех проверок добаляем хеш и id изображения в словарь и в список для мемов
                    rows[hash_images] = photo_id
                    utils.set_hash_photo_for_chat(message.chat.id, rows)

                    answer = utils.get_answer_for_user(message.chat.id)
                    if answer == None:
                        answer = []

                        answer.append(photo_id)

                        utils.set_id_photo_for_chat(message.chat.id, answer)
                    else:
                            answer.append(photo_id)
                            utils.set_id_photo_for_chat(message.chat.id, answer)


""""Меню старт"""


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Для Гильдии Python")

if __name__ == '__main__':
    bot.remove_webhook()


    bot.polling(none_stop=True)
