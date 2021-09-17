import discord
import pyrebase
import random
import string
import time
from discord.ext import commands

Moder = False		#False - если нет модерации у заданий, True - если есть
apiKey = 'AIzaSyBZ89phjIKS4ev_b_SOXx2kl5NMYPMc0R4'		#Для базы данных firebase
databaseURL = 'https://botest-ec7b7-default-rtdb.firebaseio.com'
Token = 'ODgyOTc1NzYwODQ2MDMyOTA2.YTDNQg.VHfLBo8CnOHsisIBoDPExnEuI7c'	#Для бота
game = 'помощника'	#В статусе бота "Игрет в ..."
prefix = '>'	#С чего начинаются команды у бота

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
	if len(text) == 4:
		z = 'Ник - "' + text[0] + '"\nНазвание заказа - "' + text[1] + '"\nВознаграждение - "' + text[2] + '"\nОписание - "' + text[3] + '"' #\n **Уже кто-то взял это задание**
		if Moder == False:
			base.child("quests").update({ids: z})
		else:
			base.child("Order").update({ids: z})
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
	if (str(base.child("quests").get().val())) == 'None':
		base.child("quests").update({'test': 'test'})

	if (str(base.child("Order").get().val())) == 'None' and Moder == True:
		base.child("Order").update({'test': 'test'})

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound ):
        await ctx.send(embed = discord.Embed(title = 'Данной команды не существует', description = 'Чтобы узнать доступные команды напишите ">help"', color=0xbd7800))

@bot.command()
async def Заказ(ctx: discord.Message):
	if ctx.guild is None and not ctx.author.bot:
		await ctx.send(embed = destext('Как оформить заказ', '**1. Ваш ник\n2. Название заказа\n3. Вознаграждение\n4. Описание (Возможное уточнее заказа, Адресс доставки и т.д.)**\n\nЗаказ вводится одним сообщением. В случае неправильного написания бот отменит заказ\nНужно обязательно заполнить все поля'))
		time.sleep(0.01)
		nord = 0
		while nord == 0:
			time.sleep(0.01)
			await ctx.send('Введите свой заказ')
			NewOrder = await bot.wait_for("message", check=check(ctx))
			time.sleep(0.01)
			embed=discord.Embed(title="Подтверждение", color=0xbd7800)
			embed.add_field(name='Если введёные данные верны напишите "Готово"', value='Если же вы ошиблись, то напишите "Повтор"', inline=False)
			embed.set_footer(text="Для отмены напишите любое слово")
			await ctx.send(embed=embed)
			Done = await bot.wait_for("message", check=check(ctx))
			time.sleep(0.01)
			if Done.content == 'Готово':
				Zag, code = new_quest(NewOrder.content)
				if Zag != 'error':
					nord = 1
					if Moder == False:
						await ctx.send('Готово!\nID вашего заказа - "' + code + '"\nТеперь вы можете добавть табличку с заданием на нашу базу\nВот примерный вид таблички:')
					else:
						await ctx.send('Готово!\nID вашего заказа - "' + code + '"\nТеперь ваш заказ отправлен на модерацию\nПосле проверки вы можете поставить табличку с вашим заказом на нашу базу\nВот примерный вид таблички:')
					embed=discord.Embed(title=Zag, description=code, color=0xbd7800)
					await ctx.send(embed=embed)
				else:
					await ctx.send(embed=destext('Ошибка','Неверный ввод даных'))
					nord = 1
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
			yes = await bot.wait_for("message", check=check(ctx))
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
async def Доска(ctx: discord.Message, *arg):
	if ctx.guild is None and not ctx.author.bot:
		if len(arg) == 0:
			t = base.child("quests").get()
			for user in t.each():
				if str(user.key()) != 'test' and str(user.val())[-1] !='*':
					await ctx.send(embed=destext('ID - "' + str(user.key()) + '"', '**' + str(user.val()) + '**' ))
		elif arg[0] == 'с':
			t = base.child("quests").get()
			s = []
			for user in t.each():
				if str(user.key()) != 'test' and str(user.val())[-1] !='*':
					s.append([str(user.key()),str(user.val())])
			rand = random.randint(0, len(s)-1)
			await ctx.send(embed=destext('ID - "' + s[rand][0] + '"', '**' + s[rand][1] + '**' ))
		elif len(arg) == 2 and int(arg[0]) == int(arg[0]) and int(arg[1]) == int(arg[1]):
			t = base.child("quests").get()
			ints = 0
			for user in t.each():
				if str(user.key()) != 'test' and str(user.val())[-1] !='*':
					ints += 1
					if ints > int(arg[0])-1 and ints < int(arg[1])+1:
						await ctx.send(embed=destext('ID - "' + str(user.key()) + '"', '**' + str(user.val()) + '**' ))
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
		delite = await bot.wait_for("message", check=check(ctx))
		if delite.content == 'Удалить':
			base.child("quests").child(code).remove()
			await ctx.send('Задание ID - "' + code + '" было удалено')
	else:
		await ctx.send('Я работаю только в ЛС')

@bot.command()
async def Гайд(ctx: discord.Message):
	if ctx.guild is None and not ctx.author.bot:
		await ctx.send(embed=destext('Напишите, какой гайд вы хотите увидеть', '"Размещение" - Как разместить заказ на базе\n"Лобби" - Как попасть  в лобби с заказами\n"Принять" - Как принять задание'))
		guide = await bot.wait_for("message", check=check(ctx))
		time.sleep(0.2)
		if guide.content == 'Размещение' or guide.content == 'размещение':
			await ctx.send('**Как разместить заказ на базе**')
			await ctx.send(embed=GuideUrl('Размещение задания ч.1','Поставьте табличку на стену. На табличке должно быть написано название заказа и ID','https://i.ibb.co/6m9krVY/javaw-6-DMI7-Pv-Yx-M.png'))
			time.sleep(0.2)
			await ctx.send(embed=GuideUrl('Размещение задания ч.2','Переименуйте 1 листок бумаги в ID заказа','https://i.ibb.co/c1BSL0L/javaw-H5-UYj7fy-V1.png'))
			time.sleep(0.2)
			await ctx.send(embed=GuideUrl('Размещение задания ч.3','Откройте сундук с табличкой "Не взятые задания"','https://i.ibb.co/xX2N1zZ/javaw-gnva-MBg-H9a.png'))
			time.sleep(0.2)
			await ctx.send(embed=GuideUrl('Размещение задания ч.4','Положите в сундук переименованный листок','https://i.ibb.co/BGPNQ94/javaw-Lwh5dz-Rekb.png'))
		elif guide.content == 'Лобби' or guide.content == 'лобби':
			await ctx.send('**Как попасть  в лобби с заказами**')
			await ctx.send(embed=GuideUrl('Координаты базы ч.1','В хабе нужно ехать по зелёной ветке','https://i.ibb.co/ZmCc4Lm/javaw-wtw-L6-Bg5-CI.png'))
			time.sleep(0.2)
			await ctx.send(embed=GuideUrl('Координаты базы ч.2','На координатах x = 2713, z = -1 находится проход к порталу','https://i.ibb.co/r0dt1Ng/javaw-JLMYu2jahd.png'))
			time.sleep(0.2)
			await ctx.send(embed=GuideUrl('Координаты базы ч.3','В конце проходу находится портал на базу','https://i.ibb.co/89KQBkP/javaw-Zbf83-Arh-ZD.png'))
			time.sleep(0.2)
			await ctx.send(embed=GuideUrl('Проход к лобби ч.1','После выхода из портала нужно подойти месту открытия прохода на базу','https://i.ibb.co/bmJJftp/javaw-lrck-Vp-N59-N.png'))
			time.sleep(0.2)
			await ctx.send(embed=GuideUrl('Проход к лобби ч.2','Там нужно нажать на кнопку','https://i.ibb.co/nmH74HR/javaw-q-Ej-Ae8qi-N4.png'))
			time.sleep(0.2)
			await ctx.send(embed=GuideUrl('Проход к лобби ч.3','И быстро запрыгнуть в открывшийся проход','https://i.ibb.co/Nn0j6QP/javaw-RLCDy2-GVvz.png'))
			time.sleep(0.2)
			await ctx.send(embed=GuideUrl('Проход к лобби ч.4','Нужно прыгнуть в воду','https://i.ibb.co/GP0wkCm/javaw-Kdgb-GXz-SI0.png'))
			time.sleep(0.2)
			await ctx.send(embed=GuideUrl('Проход к лобби ч.5','В проходе справа есть лифт','https://i.ibb.co/swy3zNw/javaw-e-Re-Soc7f-La.png'))
			time.sleep(0.2)
			await ctx.send(embed=GuideUrl('Проход к лобби ч.6','Нужно зайти в него и нажать на кнопку','https://i.ibb.co/ChVDLLG/javaw-g-Up98l-HVg1.png'))
			time.sleep(0.2)
			await ctx.send(embed=GuideUrl('Проход к лобби ч.7','После спуска вниз нужно идти вперёд по коридору в самый конец','https://i.ibb.co/34RV9yJ/javaw-l-Awv-Q1x-QBs.png'))
			time.sleep(0.2)
			await ctx.send(embed=GuideUrl('Проход к лобби ч.8','Поздравляю! Вы в лобби с заказами','https://i.ibb.co/D9NMD2x/javaw-E1-Ye-Gsh5-D6.png'))
		elif guide.content == 'Принять' or guide.content == 'принять':
			await ctx.send('**Как принять задание**')
			await ctx.send(embed=GuideUrl('Получение залания ч.1','Найдите подходящее задание в лобби. Запомните его ID','https://i.ibb.co/6m9krVY/javaw-6-DMI7-Pv-Yx-M.png'))
			time.sleep(0.2)
			await ctx.send(embed=GuideUrl('Получение залания ч.2','Откройте сундук с табличкой "Не взятые задания"','https://i.ibb.co/xX2N1zZ/javaw-gnva-MBg-H9a.png'))
			time.sleep(0.2)
			await ctx.send(embed=GuideUrl('Получение залания ч.3','Возмите листок с ID этого задания. (Если листка нет, то это задание кто-то взял)','https://i.ibb.co/BGPNQ94/javaw-Lwh5dz-Rekb.png'))
			time.sleep(0.2)
			await ctx.send(embed=GuideUrl('Получение залания ч.4','Напиши мне команду ">Принять <ID задания>"','https://i.ibb.co/yS5dC4G/Discord-CVcu7h3rrl.png'))
			time.sleep(0.2)
			await ctx.send(embed=GuideUrl('Получение залания ч.5','Если задание ещё не кто не взял, то в ответ вы бот напишет - "Вы приняли задание"','https://i.ibb.co/jgdRgXB/Discord-G7i-I5-YYMp1.png'))
			time.sleep(0.2)
			await ctx.send(embed=GuideUrl('Завершение задания','Если вы выполнили задание и получили награду, то задание нужно удалить.\nВы можете договориться, кто удалит задание.\nНапишите мне ">Удалить <ID заказа>" для удаления задания.','https://i.ibb.co/5jHLYcN/Discord-s-Tf-TQd-Aj3-Z.png'))
			time.sleep(0.2)
	else:
		await ctx.send('Я работаю только в ЛС')

@bot.command()
async def add(ctx: discord.Message, *arg):
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

@bot.command()
async def remove(ctx: discord.Message, *arg):
	title = ' '.join(arg)
	
	author_id = ctx.message.author.id
	text = str(base.child(str(author_id) + '/' + title).get().val())
	if (text) == 'None':
		await ctx.send(embed = destext('Ошибка', 'Такой заметки не найдено'))
	else:
		base.child(str(author_id) + '/' + title).remove()
		await ctx.send('Готово')

@bot.command()
async def list(ctx):
	author_id = ctx.message.author.id
	if (str(base.child(author_id).get().val())) == 'None':
		base.child(author_id).update({'vbg092g49s87yА*(Р)ц': 'test'})
	t = base.child(author_id).get()
	
	for ind in t.each():
		if str(ind.key()) != 'vbg092g49s87yА*(Р)ц': 
			await ctx.send('"' + str(ind.key()) + '"')

@bot.command()
async def read(ctx, *arg):
	title = ' '.join(arg)
	
	author_id = ctx.message.author.id
	text = str(base.child(str(author_id) + '/' + title).get().val())
	if (text) == 'None':
		await ctx.send(embed = destext('Ошибка', 'Такой заметки не найдено'))
	else:
		await ctx.send(embed = destext(title, text))

@bot.command()
async def help(ctx: discord.Message):
	if ctx.guild is None and not ctx.author.bot:
		await ctx.send(embed = discord.Embed(title="Команды", color=0xbd7800, description='**>Заказ - Создать заказ\n>Принять <ID заказа> - Принять заказ\n\n>Доска - Просмотр всех заказов\n>Доска с - Просмотр случайного заказа\n>Доска <a> <b> - Просмотр всх заказов по списку от a до b\n\n>Удалить <ID заказа> - Удалить заказ\n>Гайд - небольшие гайды\n\n>add <Заголовок> - Создать заметку\n>list - Просмотреть список заголовков заметок\n>read <Заголовок> - Просмотр заметки\n>remove <Заголовок> - Удалить заметку\n\n>help - Просмотр команд бота**'))
	else:
		await ctx.send('Я работаю только в ЛС')

bot.run(Token)