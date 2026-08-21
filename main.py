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
        self.username = os.environ.get("IG_USERNAME")
        self.password = os.environ.get("PASSWORD")
        self.similar_acc = os.environ.get("SIMILAR_ACCOUNT")
        self.url = os.environ.get("BASE_URL")
        self.login_url = os.environ.get("LOGIN_URL")
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def login(self):
        print("Logging in...")
        self.driver.get(self.login_url)

        username_input = self.wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username_input.send_keys(self.username)

        password_input = self.wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password_input.send_keys(self.password)

        login_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Log in']")))
        login_btn.click()

        # self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="popup-save-login"]/div/div[2]'))).click()
        # self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="popup-notifications"]/div/button[2]'))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Not now')]"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Not Now']"))).click()

        # self.wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/nav/a[1]')))
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "naan-rail-logo")))
        print("Logged in...")

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
    if bot is not None:
        bot.driver.quit()
