from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from time import sleep as time_sleep

opts = Options()
#opts.set_headless()
#assert opts.headless # без графического интерфейса

browser = Firefox(options=opts)

def auth(login, password):
	browser.get('https://vk.com/')

	index_email = browser.find_element_by_css_selector('#index_email')
	index_email.send_keys(login)

	index_pass = browser.find_element_by_css_selector('#index_pass')
	index_pass.send_keys(password)

	index_login_button = browser.find_element_by_css_selector('#index_login_button')
	index_login_button.click()

def create_comment(source_id, post_id, text):
	browser.get('https://vk.com/wall' + str(source_id) + '_' + str(post_id))

	reply_fakebox = browser.find_elements_by_class_name('reply_fakebox')
	if len(reply_fakebox) == 0:
		return None

	reply_fakebox[0].click()

	reply_field = browser.find_element_by_css_selector('#reply_field' + post_id)
	reply_field.send_keys(text)

	reply_button = browser.find_element_by_css_selector('#reply_button' + post_id)
	reply_button.click()

	# CAPTCHA
	while browser.find_elements_by_class_name('popup_box_container') != []:
		pass
	
	time_sleep(0.1)
	reply_replieable = browser.find_elements_by_class_name('reply_replieable')[-1]
	comment_id = reply_replieable.get_attribute('data-post-id').split('_')

	return comment_id[1]