import pytest
from playwright.sync_api import Playwright

import utils.secret_config
from pom.home_page import HomePage


@pytest.fixture()
def set_up(browser):       # def set_up(playwright: Playwright):    NO LO NECESITO XQ PLAYWRIGHT YA VIENE CON PAGE (una fixture propia)
    #browser = playwright.chromium.launch(headless=False)
    context = browser.new_context() #Si creo esto y no lo cierro se me quedan las ventanas abiertas. En la linea 10 puedo poner page en vez de browser y mutear linea 9 y 10 y sacar el teardown xq cierra sola.
    page = context.new_page()
    page.goto("https://practicetestautomation.com/practice-test-login/")
    yield page
    page.close()


@pytest.fixture()
def login_set_up(set_up):      #Hago que la fixture este tenga a su vez la fixture anterior
    page = set_up              #somo el set_up anterior me retorna el page, aca se lo asigno a una variable (page) para usarla
    home_page = HomePage(page)
    home_page.enter_username("student")
    home_page.enter_password(utils.secret_config.PASSWORD)
    home_page.click_submit()
    page.wait_for_timeout(2000)
    home_page.click_logout()

    yield page

