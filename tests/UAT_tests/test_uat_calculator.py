
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time

APP_URL = "http://127.0.0.1:5000/"


class UatCalculatorTest(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=chrome_options)

    def test_add(self):
        driver = self.driver
        driver.get(APP_URL)

        Select(driver.find_element(By.ID, "type")).select_by_value("add")
        driver.find_element(By.ID, "num1").clear()
        driver.find_element(By.ID, "num1").send_keys("15")
        driver.find_element(By.ID, "num2").clear()
        driver.find_element(By.ID, "num2").send_keys("7")
        driver.find_element(By.ID, "submit").click()
        time.sleep(1)
        result_element = driver.find_element(By.ID, "result")
        self.assertIn("22.0", result_element.text)
    
    def test_subtract(self):
        driver = self.driver
        driver.get(APP_URL)

        Select(driver.find_element(By.ID, "type")).select_by_value("subtract")
        driver.find_element(By.ID, "num1").clear()
        driver.find_element(By.ID, "num1").send_keys("10")
        driver.find_element(By.ID, "num2").clear()
        driver.find_element(By.ID, "num2").send_keys("2")
        driver.find_element(By.ID, "submit").click()
        time.sleep(1)
        result_element = driver.find_element(By.ID, "result")
        self.assertIn("8.0", result_element.text)

    def test_multiply(self):
            driver = self.driver
            driver.get(APP_URL)

            Select(driver.find_element(By.ID, "type")).select_by_value("multiply")
            driver.find_element(By.ID, "num1").clear()
            driver.find_element(By.ID, "num1").send_keys("2")
            driver.find_element(By.ID, "num2").clear()
            driver.find_element(By.ID, "num2").send_keys("8")
            driver.find_element(By.ID, "submit").click()
            time.sleep(1)
            result_element = driver.find_element(By.ID, "result")
            self.assertIn("16.0", result_element.text)

    def test_divide_by_zero(self):
            driver = self.driver
            driver.get(APP_URL)

            Select(driver.find_element(By.ID, "type")).select_by_value("divide")
            driver.find_element(By.ID, "num1").clear()
            driver.find_element(By.ID, "num1").send_keys("10")
            driver.find_element(By.ID, "num2").clear()
            driver.find_element(By.ID, "num2").send_keys("0")
            driver.find_element(By.ID, "submit").click()
            time.sleep(1)
            result_element = driver.find_element(By.ID, "result")
            self.assertIn("Invalid input", result_element.text)

    def test_divede(self):
            driver = self.driver
            driver.get(APP_URL)

            Select(driver.find_element(By.ID, "type")).select_by_value("divide")
            driver.find_element(By.ID, "num1").clear()
            driver.find_element(By.ID, "num1").send_keys("20")
            driver.find_element(By.ID, "num2").clear()
            driver.find_element(By.ID, "num2").send_keys("4")
            driver.find_element(By.ID, "submit").click()
            time.sleep(1)
            result_element = driver.find_element(By.ID, "result")
            self.assertIn("5.0", result_element.text)

    def tearDown(self):
        if self.driver:
            self.driver.quit()


