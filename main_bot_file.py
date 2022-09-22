import discord
from discord.ext import commands
from token_bot import token, prefix # токен и префикс хранятся в переменных token и prefix в отдельном файле 
import random, json, os

songs_by_words = {"крылья" : ["RSAC - Не мешай"], "песня": ["кис-кис - молчи"], "скука": ["pyrokinesis - сигаретка без кнопки"],
                  "кости": ["Алекша Нович - кости"], "туман": ["Екатерина Яшникова - Проведи меня через туман"],
                  "глаза": ["Мукка, Три дня дождя - Не выводи меня"], "любовь": ["гречка - здесь были", "маяк - ничего уже"]}

songs_by_genre = {"инди": ["RSAC - Не мешай", "pyrokinesis - сигаретка без кнопки", "кис-кис - мелочь", "Panic! At The Disco -House of Memories"],
                  "поп": ["монеточка - каждый раз"], "рок": ["Екатерина Яшникова - Проведи меня через туман", "Звери - До скорой встречи"]}

songs_by_singer = {"RSAC": ["RSAC - Не мешай"], "кис-кис": ["кис-кис - молчи", "кис-кис - не уходи"], "просто Лера": ["просто Лера - Инопланетяне"],
                   "ANIKV": ["ANIKV - там, где хорошо"], "Екатерина Яшникова": ["Екатерина Яшникова - Проведи меня через туман"]}

if not 'users.json' in os.listdir(os.getcwd()):  # создание файла, хранящего информацию о том, какие песни уже направлялись пользователям
    with open('users.json', "w",  encoding="utf-8") as file:
        json.dump({}, file)        

def random_song(songs_list): # определение случайной песни из подходящих запросу
    if songs_list:
        return random.choice(list(songs_list))
    else:
        return "боюсь, по этому запросу мне больше нечего предложить..."

def last_revision(songs_dict, word, user_id): # отбор подходящих песен 
    with open('users.json', 'r', encoding="utf-8") as file:
        users = json.load(file)
    if word in songs_dict.keys():
        if not user_id in users.keys():
            return random_song(songs_dict[word])
        else:
            return random_song(set(songs_dict[word]).difference(set(users[user_id])))
    else:
        return "боюсь, я такого не слушаю..."
    with open('users.json', 'w', encoding="utf-8") as file:
        json.dump(users, file)

bot = commands.Bot(command_prefix = prefix, intents=discord.Intents.default()) # создание бота

# обработка команд
@bot.command() 
async def word(ctx):
    with open('users.json', 'r', encoding="utf-8") as file:
        users = json.load(file)
    word = ctx.message.content[5:].strip()
    song = last_revision(songs_by_words, word, str(ctx.author.id))
    await ctx.send(song)
    if str(ctx.author.id) in users.keys():
        users[str(ctx.author.id)].append(song)
    else:
        users[str(ctx.author.id)] = [song]
    with open('users.json', 'w', encoding="utf-8") as file:
         json.dump(users, file)
    
@bot.command() 
async def genre(ctx): 
    with open('users.json', 'r', encoding="utf-8") as file:
        users = json.load(file)
    word = ctx.message.content[6:].strip()
    song = last_revision(songs_by_genre, word, str(ctx.author.id))
    await ctx.send(song)
    if str(ctx.author.id) in users.keys():
        users[str(ctx.author.id)].append(song)
    else:
        users[str(ctx.author.id)] = [song]
    with open('users.json', 'w', encoding="utf-8") as file:
         json.dump(users, file)
    
    
@bot.command() 
async def singer(ctx): 
    with open('users.json', 'r', encoding="utf-8") as file:
        users = json.load(file)
    word = ctx.message.content[7:].strip()
    song = last_revision(songs_by_singer, word, str(ctx.author.id))
    await ctx.send(song)
    if str(ctx.author.id) in users.keys():
        users[str(ctx.author.id)].append(song)
    else:
        users[str(ctx.author.id)] = [song]
    with open('users.json', 'w', encoding="utf-8") as file:
         json.dump(users, file)

# запуск бота
bot.run(token) 
