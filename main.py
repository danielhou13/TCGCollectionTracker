import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import requests

url = "https://store.tcgplayer.com/collection"


def get_website(driver, url: str):
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "lxml")
    print("soup test 1")
    print(soup)
    text = requests.get(url).text
    soup2 = BeautifulSoup(text, "lxml")
    print("soup test 2")
    print(soup2)


def login(driver, username: str, password: str):
    login = driver.find_element(By.LINK_TEXT, "Login")
    login2 = driver.find_element(By.XPATH, '//a[text()="Login"]')
    login3 = driver.find_element(By.XPATH, '//a[contains(text(), "Login")]')
    login.click()
    username_field = driver.find_element(By.NAME, "Email")
    username_field.send_keys(username)
    password_field = driver.find_element(By.NAME, "Password")
    password_field.send_keys(password)
    submit_button = driver.find_element(By.XPATH, '//span[text()="Sign In"]')
    submit_button.click()

    try:
        frame = driver.find_element(By.XPATH, '//iframe[contains(@src, "recaptcha")]')
        driver.switch_to.frame(frame)
        if captcha := WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='challenge']"))
        ):
            raise Exception("Oh no, theres a captcha!")
    except TimeoutException as e:
        driver.switch_to.default_content()
        pass

    try:
        if error_message := WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "signin-content__error-message")
            )
        ):
            raise Exception(error_message.text)
    except TimeoutException as e:
        pass


if __name__ == "__main__":
    driver = webdriver.Chrome()
    time.sleep(5)
    username = input("Enter your TCG Player Username: ")
    password = input("Enter your TCG Player Password: ")
    while True:
        print("we will not store your login credentials")
        get_website(driver, url)
        login(driver, username, password)

        time.sleep(60 * 60)
