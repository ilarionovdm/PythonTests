import test_1
import pytest
import allure
from allure.constants import AttachmentType
import person
from base_test import BaseTest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


class Test2(BaseTest):

    def test_2(self):
        with pytest.allure.step('Тест 1. Добавление нового сотрудника'):
            new_person = test_1.Test1().test_1()
            allure.attach('1step', BaseTest.driver.get_screenshot_as_png(), type=AttachmentType.PNG)
        with pytest.allure.step('Удаление нового сотрудника'):
            BaseTest.driver.find_element_by_xpath("//div[contains(@id,'persons')]"
                                                  "/div[contains(@class,'person')]"
                                                  "//div[contains(@class, 'name') "
                                                  "and contains(text(), '" + new_person.lastName + "')]"
                                                  "//div[@title = 'Удалить человека']").click()
            BaseTest.driver.find_element_by_xpath("//button/span[contains(text(),'Да')]").click()
            allure.attach('2step', BaseTest.driver.get_screenshot_as_png(), type=AttachmentType.PNG)
        with pytest.allure.step('Проверка удаления нового сотрудника'):
            BaseTest.driver.refresh()
            number = int(
                BaseTest.driver.find_element_by_xpath("//div[contains(@class, 'pages')][1]/a[last()]/span").text)
            i = 1
            while i <= number:
                elem = WebDriverWait(BaseTest.driver, 10).until(
                    ec.presence_of_element_located(
                        (By.XPATH, "//a[contains(@href, 'page')]/span[text()=" + str(i) + "]"))
                )
                elem.click()
                i += 1
                person_list = BaseTest.driver.find_elements_by_xpath("//*[contains(@id, 'persons')]"
                                                                     "/*[contains(@class, 'person')]")
                j = 1
                while j <= len(person_list):
                    name = BaseTest.driver.find_element_by_xpath("//div[contains(@id,'persons')]"
                                                                 "/div[contains(@class,'person')][" + str(j) + "]"
                                                                 "//div[contains(@class, 'name')]").text
                    parts = name.split()
                    leaf = person.Person()
                    leaf.lastName = parts[0]
                    leaf.firstName = parts[1]
                    if person.compare_persons(new_person, leaf):
                        allure.attach('4step', BaseTest.driver.get_screenshot_as_png(), type=AttachmentType.PNG)
                        assert False
                    j += 1
            allure.attach('3step', BaseTest.driver.get_screenshot_as_png(), type=AttachmentType.PNG)