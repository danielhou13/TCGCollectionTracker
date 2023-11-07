import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

url = "https://store.tcgplayer.com/collection?utm_campaign=18149059402&utm_source=google&utm_medium=cpc&utm_content=&utm_term=&adgroupid=&gclid=Cj0KCQiAuqKqBhDxARIsAFZELmJuDZ_ls6gqtQHcvZJCc9laiTZG6_xUJZ0yes2sNZcXOXve27yosPsaAmlOEALw_wcB"


def get_website(driver, url: str):
    driver.get(url)


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
    while True:
        username = input("Enter your TCG Player Username: ")
        password = input("Enter your TCG Player Password: ")
        print("we will not store your login credentials")
        get_website(driver, url)
        login(driver, username, password)