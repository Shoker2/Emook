import discord
import pyrebase
import random
import string
import time
from discord.ext import commands

Moder = False		#False - если нет модерации у заданий, True - если есть
apiKey = 'AIzaSyBZ89phjIKS4ev_b_SOXx2kl5NMYPMc0R4'		#Для базы данных firebase
databaseURL = 'https://botest-ec7b7-default-rtdb.firebaseio.com'
Token = 'ODgyOTc1NzYwODQ2MDMyOTA2.YTDNQg.VHfLBo8CnOHsisIBoDPExnEuI7c' #Для бота

def new_quest(z):
	plus = 0
	while plus == 0:
		replay = 0
		ids = grs(8)
		if Moder == False:
			t = base.child("quests").get()
		else:
			t = base.child("Order").get()
		for user in t.each():
			a = user.key()
			if a != ids and replay == 0:
				plus = 1
			elif a == ids:
				plus = 0
				replay = 1
	
	text = z.splitlines()
	z = 'Ник - "' + text[0] + '"\nНазвание заказа - "' + text[1] + '"\nВознаграждение - "' + text[3] + '"\nОписание - "' + text[3] + '"' #\n **Уже кто-то взял это задание**
	if Moder == False:
		base.child("quests").update({ids: z})
	else:
		base.child("Order").update({ids: z})
	return text[1], ids

def grs(y):
	return ''.join(random.choice(string.ascii_letters) for x in range(y))

config = {
  "apiKey": apiKey,
  "authDomain": "projectId.firebaseapp.com",
  "databaseURL": databaseURL,
  "storageBucket": "projectId.appspot.com"
}

firebase = pyrebase.initialize_app(config)
base = firebase.database()

if (str(base.child("quests").get().val())) == 'None':
	base.child("quests").update({'test': 'test'})

if (str(base.child("Order").get().val())) == 'None' and Moder == True:
	base.child("Order").update({'test': 'test'})

bot = commands.Bot(command_prefix='>')
bot.remove_command('help')

@bot.event
async def on_ready():
	print('Мы вошли как {0.user}'.format(bot))

@bot.command()
async def Заказ(ctx: discord.Message):
	if ctx.guild is None and not ctx.author.bot:
		embed=discord.Embed(title="Заказ вводится одним сообщением. В случае неправильного написания бот отменит заказ", color=0xbd7800)
		embed.set_author(name="Как оформить заказ")
		embed.add_field(name="1. Ваш ник", value="2. Название заказа", inline=False)
		embed.add_field(name="3. Вознаграждение", value="4. Описание (Возможное уточнее заказа, Адресс доставки и т.д.)", inline=False)
		embed.set_footer(text="Нужно обязательно заполнить все поля")
		await ctx.send(embed=embed)
		time.sleep(0.01)
		nord = 0
		while nord == 0:
			time.sleep(0.01)
			await ctx.send('Введите свой заказ')
			time.sleep(0.01)
			NewOrder = await bot.wait_for("message")
			time.sleep(0.01)
			embed=discord.Embed(title="Подтверждение", color=0xbd7800)
			embed.add_field(name='Если введёные данные верны напишите "Готово"', value='Если же вы ошиблись, то напишите "Повтор"', inline=False)
			embed.set_footer(text="Для отмены напишите любое слово")
			await ctx.send(embed=embed)
			time.sleep(0.01)
			Done = await bot.wait_for("message")
			time.sleep(0.01)
			
			if Done.content == 'Готово':
				Zag, code = new_quest(NewOrder.content)
				nord = 1
				if Moder == False:
					await ctx.send('Готово!\nID вашего заказа - "' + code + '"\nТеперь вы можете добавть табличку с заданием на нашу базу\nВот примерный вид таблички:')
				else:
					await ctx.send('Готово!\nID вашего заказа - "' + code + '"\nТеперь ваш заказ отправлен на модерацию\nПосле проверки вы можете поставить табличку с вашим заказом на нашу базу\nВот примерный вид таблички:')
				embed=discord.Embed(title=Zag, description=code, color=0xbd7800)
				await ctx.send(embed=embed)
			elif Done.content == 'Повтор':
				continue
			else:
				nord = 1
	else:
		await ctx.send('Я работаю только в ЛС')
	
@bot.command()
async def Принять(ctx: discord.Message, code):
	if ctx.guild is None and not ctx.author.bot:
		quest = base.child("quests/" + code).get()
		if str(quest.val())[-1] != '*':
			embed=discord.Embed(title='Задание', description=str(quest.val()), color=0xbd7800)
			embed.add_field(name='Чтобы взять задание напишите "Принять"', value='Для отмены напишите любое слово', inline=False)
			await ctx.send(embed=embed)
			time.sleep(0.01)
			yes = await bot.wait_for("message")
			if yes.content == 'Принять':
				UpdateQuest = str(quest.val()) + '\n*'
				base.child("quests").update({code: UpdateQuest})
				await ctx.send('Вы приняли задание')
		else:
			embed=discord.Embed(title='Задание', description=str(quest.val())[:-2], color=0xbd7800)
			await ctx.send(embed=embed)
			await ctx.send('**Вы не можете взять это задание, так как кто-то уже принял данное задание**')
	else:
		await ctx.send('Я работаю только в ЛС')

@bot.command()
async def Доска(ctx: discord.Message):
	if ctx.guild is None and not ctx.author.bot:
		await ctx.send('⟃⟞⟞⟞⟞⟞⟞⟞⟞✫⟮Доска Заказов⟯✫⟝⟝⟝⟝⟝⟝⟝⟝⟄')
		t = base.child("quests").get()
		for user in t.each():
			if str(user.key()) != 'test' and str(user.val())[-1] !='*':
				await ctx.send('ID - "' + str(user.key()) + '"\n' + str(user.val()) + '\n⟃⟝⟝⟝⟝⟝⟝⟝⟝⟝⟝⟝⟝⟝⟝⟝⟝⟝⟝⟝⟝⟝⟝⟝⟝⟝⟄')
	else:
		await ctx.send('Я работаю только в ЛС')

@bot.command()
async def Удалить(ctx: discord.Message, code):
	if ctx.guild is None and not ctx.author.bot:
		quest = base.child("quests/" + code).get()
		if str(quest.val())[-1] != '*':
			embed=discord.Embed(title='Задание', description=str(quest.val()), color=0xbd7800)
		elif str(quest.val())[-1] == '*':
			embed=discord.Embed(title='Задание', description=str(quest.val())[:-1], color=0xbd7800)
		
		embed.add_field(name='Чтобы удалить задание напишите "Удалить"', value='Для отмены напишите любое слово', inline=False)
		await ctx.send(embed=embed)
		time.sleep(0.01)
		delite = await bot.wait_for("message")
		if delite.content == 'Удалить':
			base.child("quests").child(code).remove()
			await ctx.send('Задание ID - "' + code + '" было удалено')
	else:
		await ctx.send('Я работаю только в ЛС')

@bot.command()
async def help(ctx: discord.Message):
	if ctx.guild is None and not ctx.author.bot:
		embed=discord.Embed(title="Команды", color=0xbd7800)
		embed.add_field(name=">Заказ - Создать заказ", value=">Принять <ID заказа> - Принять заказ", inline=False)
		embed.add_field(name=">Доска - Просмотр всех заказов", value=">Удалить <ID заказа> - Удалить заказ", inline=False)
		embed.set_footer(text=">help - Просмотр команд бота")
		await ctx.send(embed=embed)
	else:
		await ctx.send('Я работаю только в ЛС')

bot.run(Token)