import numpy as np 
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

if __name__ == '__main__':
	PAGE_URL = "https://www.usnews.com/best-colleges/rankings/national-universities"

	# POST_LOADS is the number of pages to get reviews from a single product; manually update to number less than total # of page reviews available
	POST_LOADS = 55
	LOAD_PAUSE_TIME = 2
	PAGE_LOAD_TIME = .5

	# RETRIEVING THE URL
	driver = webdriver.Chrome(r"C:\Users\Michell\Box\School\Graduate School\Data Focused Python\chromedriver.exe")
	driver.get(PAGE_URL)

	#SCROLL TO THE BOTTOM
	# Get scroll height
	last_height = driver.execute_script("return document.body.scrollHeight")

	#explodes at 60 schools
	i = 0
	while i<POST_LOADS and True:
		# Scroll down to bottom
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Wait to load page
		time.sleep(PAGE_LOAD_TIME)

		# Calculate new scroll height and compare with last scroll height
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:

			driver.find_element_by_xpath("//a[contains(text(),'Load More')]").click() 

		last_height = new_height
		print(i)
		i += 1

	#save all links
	urls = []
	results = driver.find_elements_by_xpath('//*[@id="search-application-results-view"]/div/ol/li/div/section/div/h3/a')
		
	for each in results[272:]:
		schoollink = each.get_attribute("href")
		url = schoollink.strip()
		urls.append(url)
		#print(schoollink)


	#create empty data frame
	school_info = pd.DataFrame(columns=['rank','school_name','tuition','selectivity','acceptance_rate','percent_financial_aid','award'])

	#loop through each link to extract needed info
	for link_id in range(0,len(urls)):
		link = urls[link_id]
		time.sleep(PAGE_LOAD_TIME)

		#open link 
		driver.execute_script("window.open('');")
		driver.switch_to.window(driver.window_handles[1])
		driver.get(link)
		#driver.get(element.get_attribute("href"))
		time.sleep(PAGE_LOAD_TIME)

		#retrieve school name

		school_name = driver.find_element_by_class_name('hero-heading').text
		
		#retrieve rank
		rank = driver.find_element_by_xpath('//*[@class="hero-content-main"]/div/div/div/strong').text.split()
		rank = rank[0]
		rank = rank[1:]

		#retrive tuition
		try:
			tuition = driver.find_element_by_xpath('//*[@class="text-strong"][@data-test-id="v_private_tuition"]')
		except: 
			tuition = driver.find_element_by_xpath('//*[@class="text-strong"][@data-test-id="v_out_state_tuition"]')
		tuition1 = tuition.get_attribute("innerHTML").strip()


		#retrieve selectivity
		selectivity = driver.find_element_by_xpath('//*[@class="text-strong"][@data-test-id="c_select_class"]')
		selectivity1 = selectivity.get_attribute("innerHTML").strip()

		#retrieve acceptance_rate
		acceptance_rate = driver.find_element_by_xpath('//*[@class="text-strong"][@data-test-id="r_c_accept_rate"]')
		acceptance_rate1 = acceptance_rate.get_attribute("innerHTML").strip()
		
		#retrieve financial_aid
		financial_aid = driver.find_element_by_xpath('//*[@id="Cost & Financial Aid-section"]/following-sibling::p').text
		fin_string = financial_aid.split(',')
		try:
			percent_fin_aid = fin_string[1].split(" ")
			percent_fin_aid = percent_fin_aid[1]
		except:
			percent_fin_aid = 0
		try:
			award = fin_string[2].split(" ")
			award = award[-1] + fin_string[3]
			award = award[:-1]
		except:
			award = 0



		#print to dataframe
		school_info.loc[len(school_info)] = [rank,school_name, tuition1, selectivity1, acceptance_rate1, percent_fin_aid, award]


		#close this window, go back to initial tab
		driver.close()
		driver.switch_to.window(driver.window_handles[0])
	driver.close()

	#copy dataframe to csv file
	school_info.to_csv('us_news4.csv', index=False)


'''
#https://www.dataquest.io/blog/web-scraping-tutorial-python/
#scraping setup
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
page = requests.get('https://www.usnews.com/best-colleges/rankings/national-universities', headers = headers)
soup = BeautifulSoup(page.content, 'html.parser')

#print([type(item) for item in list(soup.children)])
html = list(soup.children)[3]
#print([type(item) for item in list(html.children)])
print(soup.find_all('h3'))
'''