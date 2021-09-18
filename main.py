import discord
import pyrebase
import random
import string
from discord.ext import commands

apiKey = 'AIzaSyBZ89phjIKS4ev_b_SOXx2kl5NMYPMc0R4'		#Для базы данных firebase
databaseURL = 'https://botest-ec7b7-default-rtdb.firebaseio.com'
Token = 'ODgzNzAwOTk4NTcxNDUwMzY4.YTNwsA.k8I_fRs5AQeBNMGq2rroKRaEzd0'	#Для бота
game = 'бота'	#В статусе бота "Игрет в ..."
prefix = '>'	#С чего начинаются команды у бота

def new_quest(z, id_server):
	if (str(base.child(id_server + "/quests").get().val())) == 'None':
		base.child(id_server + "/quests").update({'test': 'test'})
	plus = 0
	while plus == 0:
		replay = 0
		ids = grs(8)
		t = base.child(id_server + "/quests").get()
		for user in t.each():
			a = user.key()
			if a != ids and replay == 0:
				plus = 1
			elif a == ids:
				plus = 0
				replay = 1
	
	text = z.splitlines()
	if len(text) == 4:
		z = 'Ник заказчика - "' + text[0] + '"\nНазвание заказа - "' + text[1] + '"\nВознаграждение - "' + text[2] + '"\nОписание - "' + text[3] + '"' #\n **Уже кто-то взял это задание**
		base.child(id_server + "/quests").update({ids: z})
		return text[1], ids
	if len(text) == 3:
		z = 'Ник заказчика - "' + text[0] + '"\nНазвание заказа - "' + text[1] + '"\nОписание - "' + text[2] + '"' #\n **Уже кто-то взял это задание**
		base.child(id_server + "/quests").update({ids: z})
		return text[1], ids
	else:
		return 'error', 'error'

def grs(y):
	return ''.join(random.choice(string.ascii_letters) for x in range(y))

def GuideUrl(title, text, url):
	embed = discord.Embed(title=title, description=text, color=0xbd7800)
	embed.set_image(url=url)
	return embed

def destext(title, text):
	embed = discord.Embed(title=title, description=text, color=0xbd7800)
	return embed

def check(ctx):
    def inner(msg):
        return msg.author == ctx.author
    return inner

config = {
  "apiKey": apiKey,
  "authDomain": "projectId.firebaseapp.com",
  "databaseURL": databaseURL,
  "storageBucket": "projectId.appspot.com"
}

firebase = pyrebase.initialize_app(config)
base = firebase.database()

bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')

@bot.event
async def on_ready():
	print('Мы вошли как {0.user}'.format(bot))
	await bot.change_presence(activity=discord.Game(name=game))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound ):
        await ctx.send(embed = discord.Embed(title = 'Данной команды не существует', description = 'Чтобы узнать доступные команды напишите ">help"', color=0xbd7800))

@bot.command()
async def Заказ(ctx):
	id_server = str(ctx.guild.id)
	await ctx.send(embed = destext('Как оформить заказ', '**1. Ваш ник\n2. Название заказа\n3. Вознаграждение\n4. Описание (Возможное уточнее заказа, Адресс доставки и т.д.)**\n\nИли\n\n**1. Ваш ник\n2. Название заказа\n3. Описание (Возможное уточнее заказа, Адресс доставки и т.д.)**\n\nЗаказ вводится одним сообщением. В случае неправильного написания бот отменит заказ\nНужно обязательно заполнить все поля'))
	nord = 0
	while nord == 0:
		await ctx.send('Введите свой заказ')
		NewOrder = await bot.wait_for("message", check=check(ctx))
		embed=discord.Embed(title="Подтверждение", color=0xbd7800)
		embed.add_field(name='Если введёные данные верны напишите "Готово"', value='Если же вы ошиблись, то напишите "Повтор"', inline=False)
		embed.set_footer(text="Для отмены напишите любое слово")
		await ctx.send(embed=embed)
		Done = await bot.wait_for("message", check=check(ctx))
		if Done.content == 'Готово':
			Zag, code = new_quest(NewOrder.content, id_server)
			if Zag != 'error':
				nord = 1
				await ctx.send('Готово!\nID вашего заказа - "' + code + '"')
			else:
				await ctx.send(embed=destext('Ошибка','Неверный ввод даных'))
				nord = 1
		elif Done.content == 'Повтор':
			continue
		else:
			nord = 1

@bot.command()
async def Принять(ctx, code):
	id_server = str(ctx.guild.id)
	quest = base.child(id_server + "/quests/" + code).get()
	if str(quest.val()) != 'None':
		if str(quest.val())[-1] != '*':
			embed=discord.Embed(title='Задание', description=str(quest.val()), color=0xbd7800)
			embed.add_field(name='Чтобы взять задание напишите "Принять"', value='Для отмены напишите любое слово', inline=False)
			await ctx.send(embed=embed)
			yes = await bot.wait_for("message", check=check(ctx))
			if yes.content == 'Принять':
				UpdateQuest = str(quest.val()) + '\n*'
				base.child(id_server + "/quests").update({code: UpdateQuest})
				await ctx.send('Вы приняли задание')
		else:
			embed=discord.Embed(title='Задание', description=str(quest.val())[:-2], color=0xbd7800)
			await ctx.send(embed=embed)
			await ctx.send('**Вы не можете взять это задание, так как кто-то уже принял данное задание**')
	else:
		await ctx.send(embed=destext('Ошибка','Данного задания не существует'))

@bot.command()
async def Доска(ctx, *arg):
	id_server = str(ctx.guild.id)
	if len(arg) == 0:
		t = base.child(id_server + "/quests").get()
		for user in t.each():
			if str(user.key()) != 'test' and str(user.val())[-1] !='*':
				await ctx.send(embed=destext('ID - "' + str(user.key()) + '"', '**' + str(user.val()) + '**' ))
	elif arg[0] == 'с':
		t = base.child(id_server + "/quests").get()
		s = []
		for user in t.each():
			if str(user.key()) != 'test' and str(user.val())[-1] !='*':
				s.append([str(user.key()),str(user.val())])
		rand = random.randint(0, len(s)-1)
		await ctx.send(embed=destext('ID - "' + s[rand][0] + '"', '**' + s[rand][1] + '**' ))
	elif len(arg) == 2 and int(arg[0]) == int(arg[0]) and int(arg[1]) == int(arg[1]):
		t = base.child(id_server + "/quests").get()
		ints = 0
		for user in t.each():
			if str(user.key()) != 'test' and str(user.val())[-1] !='*':
				ints += 1
				if ints > int(arg[0])-1 and ints < int(arg[1])+1:
					await ctx.send(embed=destext('ID - "' + str(user.key()) + '"', '**' + str(user.val()) + '**' ))

@bot.command()
async def Удалить(ctx, code):
	id_server = str(ctx.guild.id)
	quest = base.child(id_server + "/quests/" + code).get()
	if str(quest.val()) != 'None':
		if str(quest.val())[-1] != '*':
			embed=discord.Embed(title='Задание', description=str(quest.val()), color=0xbd7800)
		elif str(quest.val())[-1] == '*':
			embed=discord.Embed(title='Задание', description=str(quest.val())[:-1], color=0xbd7800)
			
		embed.add_field(name='Чтобы удалить задание напишите "Удалить"', value='Для отмены напишите любое слово', inline=False)
		await ctx.send(embed=embed)
		delite = await bot.wait_for("message", check=check(ctx))
		if delite.content == 'Удалить':
			base.child(id_server + "/quests").child(code).remove()
			await ctx.send('Задание ID - "' + code + '" было удалено')
	else:
		await ctx.send(embed=destext('Ошибка','Данного задания не существует'))

@bot.command()
async def add(ctx, *arg):
	if ctx.guild is None and not ctx.author.bot:
		author_id = ctx.message.author.id
		if (str(base.child(author_id).get().val())) == 'None':
			base.child(author_id).update({'vbg092g49s87yА*(Р)ц': 'test'})
		t = base.child(author_id).get()
		
		title = ' '.join(arg)
		
		if title != '':
			await ctx.send('Теперь напишите текст заметки')
			text = await bot.wait_for("message", check=check(ctx))
			
			base.child(author_id).update({title: text.content})
			await ctx.send('Готово')
		else:
			await ctx.send(embed = destext('Ошибка', 'Отсутствует заголовок'))
	else:
		await ctx.send('Эта команда работает только в ЛС ')

@bot.command()
async def remove(ctx, *arg):
	if ctx.guild is None and not ctx.author.bot:
		title = ' '.join(arg)
		
		author_id = ctx.message.author.id
		text = str(base.child(str(author_id) + '/' + title).get().val())
		if (text) == 'None':
			await ctx.send(embed = destext('Ошибка', 'Такой заметки не найдено'))
		else:
			base.child(str(author_id) + '/' + title).remove()
			await ctx.send('Готово')
	else:
		await ctx.send('Эта команда работает только в ЛС ')

@bot.command()
async def list(ctx):
	if ctx.guild is None and not ctx.author.bot:
		author_id = ctx.message.author.id
		if (str(base.child(author_id).get().val())) == 'None':
			base.child(author_id).update({'vbg092g49s87yА*(Р)ц': 'test'})
		t = base.child(author_id).get()
		list = []
		
		await ctx.send('Ваши заметки:\n')
		
		for ind in t.each():
			if str(ind.key()) != 'vbg092g49s87yА*(Р)ц': 
				list.append('"' + str(ind.key()) + '"')
		text = '\n'.join(list)
		await ctx.send(embed=destext('Ваши записки', text))
	else:
		await ctx.send('Эта команда работает только в ЛС ')

@bot.command()
async def read(ctx, *arg):
	if ctx.guild is None and not ctx.author.bot:
		title = ' '.join(arg)
		
		author_id = ctx.message.author.id
		text = str(base.child(str(author_id) + '/' + title).get().val())
		if (text) == 'None':
			await ctx.send(embed = destext('Ошибка', 'Такой заметки не найдено'))
		else:
			await ctx.send(embed = destext(title, text))
	else:
		await ctx.send('Эта команда работает только в ЛС ')

@bot.command()
async def clear(ctx, amount=100):
	user = ctx.author
	if user.permissions_in(ctx.message.channel).administrator:
		await ctx.channel.purge(limit=amount)
		await ctx.channel.send('Сообщения успешно удалены')
	else:
		await ctx.send('У вас недостаточно прав для выполнения данной команды')

@bot.command()
async def help(ctx):
	await ctx.send(embed = discord.Embed(title="Команды", color=0xbd7800, description='**>Заказ - Создать заказ\n>Принять <ID заказа> - Принять заказ\n>Удалить <ID заказа> - Удалить заказ\n\n>Доска - Просмотр всех заказов\n>Доска с - Просмотр случайного заказа\n>Доска <a> <b> - Просмотр всх заказов по списку от a до b\n\n>add <Заголовок> - Создать заметку\n>list - Просмотреть список заголовков заметок\n>read <Заголовок> - Просмотр заметки\n>remove <Заголовок> - Удалить заметку\n\n>help - Просмотр команд бота**'))

bot.run(Token)