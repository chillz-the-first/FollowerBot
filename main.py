import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import TimeoutException, StaleElementReferenceException, ElementClickInterceptedException
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
        self.followers = []

    def login(self):
        print("Logging in...")
        self.driver.get(self.login_url)

        username_input = self.wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username_input.send_keys(self.username)

        password_input = self.wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password_input.send_keys(self.password)

        login_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Log in']")))
        login_btn.click()

        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Not now')]"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Not Now']"))).click()

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "naan-rail-logo")))
        print("Logged in...")

    def find_followers(self):
        print("Finding followers...")

        self.driver.get(f"{self.url}/u/{self.similar_acc}")
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(text(),'followers')]")
        )).click()

        followers_list = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "followers-scroll")))
        height = self.driver.execute_script("return arguments[0].scrollHeight;", followers_list)
        stable_checks = 0

        while stable_checks < 2:
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", followers_list) # Scroll to the bottom of the container
            time.sleep(1.5)

            new_height = self.driver.execute_script("return arguments[0].scrollHeight;", followers_list)
            if new_height == height:
                stable_checks += 1 # Reached the bottom of the list, but one more iteration to confirm
            else:
                stable_checks = 0 # List grew, so reset
                height = new_height

        btn_list = followers_list.find_elements(By.CLASS_NAME, "naan-follow-btn")
        self.followers = btn_list
        print("Followers found")

    def follow(self):
        # btns and btn both re-locate the buttons, this they remain 'fresh' instead of holding a stale reference
        btns = self.driver.find_elements(By.CLASS_NAME, "naan-follow-btn")
        if not btns:
            print("No followers found")
            return

        followed = 0
        for i in range(len(btns)):
            try:
                btn = self.driver.find_elements(By.CLASS_NAME, "naan-follow-btn")[i]
                if "is-following" in btn.get_attribute("class"):
                    continue
                btn.click()
                followed += 1
            except StaleElementReferenceException as e:
                print(f"Skipped one account: {type(e).__name__}")
                continue
            except ElementClickInterceptedException:
                cancel = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Cancel')]")
                cancel.click()

        print(f"Now following {followed} new accounts")

bot = None
try:
    bot = InstaFollower()
    bot.login()
    bot.find_followers()
    bot.follow()

    time.sleep(5)
except TimeoutException:
    print("A step failed, aborting run")
finally:
    if bot is not None:
        bot.driver.quit()
