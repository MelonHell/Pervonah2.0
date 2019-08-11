# --- SETTINGS --- #

login, password = 'yulia.casumova@mail.ru', 'pidoras'
mode = 1 # 0 = API, 1 = Selenium, 2 = Execute
comment_text = 'тест даня лох'

# --- CODE --- #

import vk_api
from time import sleep as time_sleep
import os

if mode == 1:
	import vk_selenium
	vk_selenium.auth(login, password)
elif mode == 2:
	with open("execute_mode_code.js", 'r', encoding = 'utf-8') as f:
		code = f.read()

# --- VK AUTH --- #

def captcha_handler(captcha):
	os.startfile(captcha.get_url())
	key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
	return captcha.try_again(key)

vk_session = vk_api.VkApi(login, password, captcha_handler=captcha_handler)

try:
	vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
	print(error_msg)

vk = vk_session.get_api()

# --- PERVONAH --- #

last_post_date = vk.newsfeed.get(filters='post', count=1)['items'][0]['date']

# --- API MODE + SELENIUM MODE --- #

def mode_default(last_post_date, comment_text, mode):
	post = vk.newsfeed.get(filters='post', count=1)['items'][0]
	if post['date'] > last_post_date:
		status = True
		try:
			if mode == 0:
				comment_id = vk.wall.createComment(owner_id=post['source_id'], post_id=post['post_id'], message=comment_text)['comment_id']
			elif mode == 1:
				comment_id = vk_selenium.create_comment(post['source_id'], post['post_id'], comment_text)
		except Exception as e:
			comment_id = None
			print(e)
	else:
		status = False
		comment_id = None

	return {'status': status, 'comment_id': comment_id, 'post_id': post['post_id'], 'source_id': post['source_id'], 'date': post['date']}


# --- EXECUTE MODE --- #

def mode_execute(last_post_date, comment_text):
	code_vars = "var last_post_date = {0}; var comment_text = '{1}';".format(last_post_date, comment_text)
	response = vk.execute(code=code_vars + code)
	return response

# --- WHILE TRUE --- #

while True:
	time_sleep(0.1)
	print('проверка ленты')

	if mode == 0 or mode == 1:
		response = mode_default(last_post_date, comment_text, mode)
	elif mode == 2:
		response = mode_execute(last_post_date, comment_text)
		
	if response['status']:
		if response['comment_id'] == None:
			print("\nНе удалось оставить комментарий")
		else:
			comment = vk.wall.getComment(owner_id=response['source_id'], comment_id=response['comment_id'])['items'][0]

			print("\nПрошло времени: " + str(comment['date'] - response['date']) + ' сек')
			print('Номер комментария: ' + str(comment['id'] - comment['post_id']))

		last_post_date = response['date']