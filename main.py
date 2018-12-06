#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from random import shuffle
import time


b_url = "https://www.facebook.com/events/birthdays/"
home_url = "https://www.facebook.com"
messanger_url = "https://www.facebook.com/messages/t/"

enter_key = u'\ue007'


def read_file(filename):
	import codecs
	with codecs.open(filename, "r", encoding="utf-8") as file_reader:
		lines = file_reader.readlines()
	return lines

def offiline_page(filename):
	lines = read_file(filename)
	string = ''.join(lines)
	return BeautifulSoup( string, features="html.parser")

def get_browser(url,proxy=""):
	from selenium import webdriver
	from selenium.webdriver.common.proxy import Proxy, ProxyType

	if proxy == "":
		browser = webdriver.Chrome() #replace with .Firefox(), or with the browser of your choice

	else:
		prox = Proxy()
		prox.proxy_type = ProxyType.MANUAL
		prox.https_proxy = proxy
		#prox.https_proxy = proxy

		#prox.socks_proxy = "ip_addr:port"
		#prox.ssl_proxy = "ip_addr:port"

		capabilities = webdriver.DesiredCapabilities.CHROME
		prox.add_to_capabilities(capabilities)

		browser = webdriver.Chrome(desired_capabilities=capabilities)

	browser.get(url) #navigate to the page
	#browser.close()
	return browser

def get_credential(filename):
	file = read_file(filename)
	string = ''.join(file)
	return eval(string)

def facebook_login(browser,configs):
	print("Logging in...")
	#browser = get_browser(home_url)
	#login_form = browser.find_element_by_css_selector("div.menu_login_container")
	login_form = browser.find_element_by_id('login_form')
	email_s = login_form.find_element_by_name('email')
	email_s.send_keys(configs['email'])
	
	password_s = login_form.find_element_by_name('pass')
	password_s.send_keys(configs['pass'])
	
	c = login_form.find_element_by_id('loginbutton')
	c.click()
	print("Logged in.")

def get_bd_user_names(browser):
	print("Getting birthday persons...")
	page = browser.page_source
	page = BeautifulSoup( page, features="html.parser")
	birthdays_content = page.find("div",id="birthdays_content")
	todays_birthday_div = birthdays_content.find("div",id="birthdays_today_card").find_next_sibling("div")
	imgs = todays_birthday_div.find_all("img")
	birthday_names = [img.attrs["aria-label"].strip() for img in imgs]
	a_s = todays_birthday_div.find_all('a')
	b_user_names = [a.attrs["href"].replace("https://www.facebook.com/","") for a in a_s if not "friendship" in a.attrs["href"]]
	b_user_names_dic = dict(zip(b_user_names,birthday_names))
	return b_user_names_dic

def send_fb_message(browser,user_name,name,message,sleep=0):
	print('Sending message to '+ name +'...')
	if sleep > 0:
		time.sleep(sleep)

	text_box_class='.notranslate'
	browser.get(messanger_url+user_name)
	text_s = browser.find_element_by_css_selector(text_box_class)
	text_s.send_keys(message+'\n--Dedicated to dear '+name+' by Bbot')
	text_s.send_keys(enter_key)

def main():
	browser = get_browser(home_url)
	configs = get_credential('../config.py')
	facebook_login(browser,configs)
	browser.get(b_url)
	b_user_names = get_bd_user_names(browser)

	message = 'Thank you so much for your patience.'
	## saving to mysql database
	[send_fb_message(browser,user_name,b_user_names[user_name],message,sleep=3) for user_name in b_user_names]
	browser.close()

if __name__ == "__main__":
	main()