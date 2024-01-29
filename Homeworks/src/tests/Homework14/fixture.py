import pytest
from selenium import webdriver

from Homeworks.src.main.Homework14.cart_page import CartPage
from Homeworks.src.main.Homework14.config import user_name, user_password
from Homeworks.src.main.Homework14.demoblaze_page import DemoBlazePage
from Homeworks.src.main.Homework14.item_page import ItemPage


@pytest.fixture(scope="class")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="class")
def demo_blaze_page(driver):
    page = DemoBlazePage(driver)
    page.open_url()
    yield page


@pytest.fixture(scope="class")
def item_page(driver):
    page = ItemPage(driver)
    yield page


@pytest.fixture(scope="class")
def cart_page(driver):
    page = CartPage(driver)
    yield page


@pytest.fixture(scope="class")
def login(demo_blaze_page):
    demo_blaze_page.click_login_button()
    demo_blaze_page.setup_login_and_password(user_name, user_password)