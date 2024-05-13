from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import unittest
import time
import json
import imaplib
import email
import regex  # thư viện trích chuỗi
import ezgmail  # thư viện đọc mail
from email.header import decode_header
from selenium import webdriver


class TestForgotPasswordFunction(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:3000')

    def tearDown(self):
        self.driver.quit()

    def login(self, username):
        self.driver.find_element(
            By.CSS_SELECTOR, 'div > ul > li:nth-child(4) > a').click()
        self.driver.find_element(
            By.CSS_SELECTOR, "body > div > div > div > a").click()
        self.driver.find_element(By.ID, "email").send_keys(username)
        self.driver.find_element(
            By.CSS_SELECTOR, 'body > div > div > div > form > div:nth-child(2) > button').click()

    # Happy Cases
    # TC_16
    def test16_login_with_valid_credentials(self):
        with open("Data/forgot_password_function_data.json", encoding="utf-8") as f:
            data = json.load(f)
            email = data["test_cases_Forgot_Password"][0]["email"]
            password = data["test_cases_Forgot_Password"][0]["password"]
            self.login(email)
            time.sleep(5)
            # Lấy OTP
            unreadThreads = ezgmail.unread()
            a = str(unreadThreads[0])
            otpmatch = regex.search(r'\b\d{8}\b', a)
            otp = otpmatch.group(0)
            # print(a)
            # print(otp)
            time.sleep(5)
            # Điền OTP và đổi mật khẩu
            self.driver.find_element(By.ID, "otp").send_keys(otp)
            self.driver.find_element(
                By.CSS_SELECTOR, "body > div > div > div > form > div:nth-child(3) > button").click()
            self.driver.find_element(By.ID, "password").send_keys(password)
            self.driver.find_element(
                By.ID, "confirmPassword").send_keys(password)
            self.driver.find_element(
                By.CSS_SELECTOR, "body > div.container.my-5 > div > div > form > div:nth-child(3) > button").click()

            success_message_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME, "alert-success"))
            )
            success_message = success_message_element.text.strip()
            # self.driver.save_screenshot('123lmss.png')
            print(success_message)
            self.assertEqual(success_message, "Đổi mật khẩu thành công! x")


if __name__ == "__main__":
    unittest.main()
