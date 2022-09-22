import discord
from discord.ext import commands
from token_bot import token, prefix
import random

songs_by_words = {"крылья" : ["RSAC - Не мешай"], "песня": ["кис-кис - молчи"], "скука": ["pyrokinesis - сигаретка без кнопки"],
                  "кости": ["Алекша Нович - кости"], "туман": ["Екатерина Яшникова - Проведи меня через туман"],
                  "глаза": ["Мукка, Три дня дождя - Не выводи меня"], "любовь": ["гречка - здесь были", "маяк - ничего уже"]}

songs_by_genre = {"инди": ["RSAC - Не мешай", "pyrokinesis - сигаретка без кнопки", "кис-кис - мелочь", "Panic! At The Disco -House of Memories"],
                  "поп": ["монеточка - каждый раз"], "рок": ["Екатерина Яшникова - Проведи меня через туман", "Звери - До скорой встречи"]}

songs_by_singer = {"RSAC": ["RSAC - Не мешай"], "кис-кис": ["кис-кис - молчи", "кис-кис - не уходи"], "просто Лера": ["просто Лера - Инопланетяне"],
                   "ANIKV": ["ANIKV - там, где хорошо"], "Екатерина Яшникова": ["Екатерина Яшникова - Проведи меня через туман"]}

users = {}

def random_song(songs_list):
    if songs_list:
        return random.choice(list(songs_list))
    else:
        return "боюсь, по этому запросу мне больше нечего предложить..."

def last_revision(songs_dict, word, user_id):
    if word in songs_dict.keys():
        if not user_id in users.keys():
            return random_song(songs_dict[word])
        else:
            return random_song(set(songs_dict[word]).difference(set(users[user_id])))
    else:
        return "боюсь, я такого не слушаю..."


bot = commands.Bot(command_prefix = prefix, intents=discord.Intents.default())

@bot.command() 
async def word(ctx):
    global users
    word = ctx.message.content[5:].strip()
    song = last_revision(songs_by_words, word, ctx.author.id)
    await ctx.send(song)
    if ctx.author.id in users.keys():
        users[ctx.author.id].append(song)
    else:
        users[ctx.author.id] = [song]
    
@bot.command() 
async def genre(ctx): 
    word = ctx.message.content[6:].strip()
    song = last_revision(songs_by_genre, word, ctx.author.id)
    await ctx.send(song)
    if ctx.author.id in users.keys():
        users[ctx.author.id].append(song)
    else:
        users[ctx.author.id] = [song]
    
@bot.command() 
async def singer(ctx): 
    word = ctx.message.content[7:].strip()
    song = last_revision(songs_by_singer, word, ctx.author.id)
    await ctx.send(song)
    if ctx.author.id in users.keys():
        users[ctx.author.id].append(song)
    else:
        users[ctx.author.id] = [song]

bot.run(token) 