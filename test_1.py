import person
import pytest
import allure
from allure.constants import AttachmentType
from base_test import BaseTest
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


class Test1(BaseTest):

    new_person = None

    def test_1(self):
        with pytest.allure.step('Авторизация в системе'):
            BaseTest.driver.find_element_by_id("login-username").send_keys("admin")
            BaseTest.driver.find_element_by_id("login-password").send_keys("admin")
            BaseTest.driver.find_element_by_id("login-button").click()
            allure.attach('1step', BaseTest.driver.get_screenshot_as_png(), type=AttachmentType.PNG)
        with pytest.allure.step('Открытие формы добавления нового сотрудника'):
            BaseTest.driver.find_element_by_id("add-person").click()
            global new_person
            new_person = person.get_random_person()
            new_person.lastName = new_person.lastName
            allure.attach('2step', BaseTest.driver.get_screenshot_as_png(), type=AttachmentType.PNG)
        with pytest.allure.step('Заполнение формы нового сотрудника'):
            BaseTest.driver.find_element_by_id("person-last-name").send_keys(new_person.lastName)
            BaseTest.driver.find_element_by_id("person-first-name").send_keys(new_person.firstName)
            BaseTest.driver.find_element_by_id("person-patronymic-name").send_keys(new_person.patronymic)
            Select(BaseTest.driver.find_element_by_id("person-position")).select_by_index(new_person.position)
            BaseTest.driver.find_element_by_id("person-project").send_keys(new_person.project)
            BaseTest.driver.find_element_by_id("person-expire").send_keys(new_person.expire)
            BaseTest.driver.find_element_by_id("person-future").send_keys(new_person.future)
            BaseTest.driver.find_element_by_id("person-nickname").send_keys(new_person.nickname)
            BaseTest.driver.find_element_by_class_name("ui-dialog-buttonset").click()
            allure.attach('3step', BaseTest.driver.get_screenshot_as_png(), type=AttachmentType.PNG)
        with pytest.allure.step('Поиск нового сотрудника'):
            BaseTest.driver.refresh()
            number = int(BaseTest.driver.find_element_by_xpath("//div[contains(@class, 'pages')][1]/a[last()]/span").text)
            i = 1
            while i <= number:
                elem = WebDriverWait(BaseTest.driver, 10).until(
                    ec.presence_of_element_located((By.XPATH, "//a[contains(@href, 'page')]/span[text()=" + str(i) + "]"))
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
                        return new_person
                    j += 1
        assert False


