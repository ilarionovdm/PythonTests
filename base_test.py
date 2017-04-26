from selenium import webdriver


class BaseTest:

    driver = None

    @classmethod
    def setup_class(cls):
        BaseTest.driver = webdriver.Chrome(executable_path="core/chromedriver.exe")
        BaseTest.driver.get("http://at.pflb.ru/matrixboard2")
        BaseTest.driver.implicitly_wait(10)
        BaseTest.driver.maximize_window()

    @classmethod
    def teardown_class(cls):
        BaseTest.driver.close()
