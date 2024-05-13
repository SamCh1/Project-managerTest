from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import unittest
import time
import json


class TestRegisterFunction(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:3000')

    def tearDown(self):
        self.driver.quit()

    def login(self, name, username, password):
        self.driver.find_element(
            By.CSS_SELECTOR, 'body > header > div > div > div.col-4 > div > ul > li:nth-child(5) > a').click()
        self.driver.find_element(By.ID, "fullName").send_keys(name)
        self.driver.find_element(By.ID, "email").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)

        self.driver.find_element(
            By.CSS_SELECTOR, "body > div > div > div > form > div:nth-child(4) > button").click()

    # Happy Cases
    # TC_08
    def test1_login_with_valid_credentials(self):
        with open("Data/register_function_data.json", encoding="utf-8") as f:
            data = json.load(f)
            name = data["test_cases_login"][0]["name"]
            username = data["test_cases_login"][0]["username"]
            password = data["test_cases_login"][0]["password"]
            self.login(name, username, password)

            success_message_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME, "alert-success"))
            )
            success_message = success_message_element.text.strip()
            self.driver.save_screenshot('123lmss.png')
            print(success_message)
            self.assertEqual(success_message, "Đăng nhập thành công! x")


if __name__ == "__main__":
    unittest.main()
