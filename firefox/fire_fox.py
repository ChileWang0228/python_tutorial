from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
options = Options()
binary = FirefoxBinary('/usr/lib/firefox/firefox')  # 这个路径一定要写
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
brower = webdriver.Firefox(firefox_options=options, firefox_binary=binary)
brower.get("http://www.baidu.com")

brower.find_element_by_id('kw').send_keys('selenium')
brower.find_element_by_id('su').click()

time.sleep(3)
print(brower.current_url)
brower.save_screenshot('1111')
brower.quit()