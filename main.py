import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

class InstaFollower:
    def __init__(self):
        self.username = os.environ.get("USERNAME")
        self.password = os.environ.get("PASSWORD")
        self.similar_acc = os.environ.get("SIMILAR_ACCOUNT")
        self.url = os.environ.get("BASE_URL")
        self.login_url = os.environ.get("LOGIN_URL")
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def login(self):
        pass

    def find_followers(self):
        pass

    def follow(self):
        pass

try:
    bot = InstaFollower()
    bot.login()

    time.sleep(5)
except TimeoutException:
    print("A step failed, aborting run")
finally:
    bot.driver.quit()
