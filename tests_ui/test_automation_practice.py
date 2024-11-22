import os

from playwright.sync_api import Playwright, sync_playwright, expect
from pom.home_page import HomePage
import pytest


PASSWORD = os.environ["PASSWORD"]    #Mejor estandar, me trae lo que tengo en el archivo .env si es local. #Si estoy corriendo el pipeline va a encontrar esta variable en los secrets de github


# try:
#     PASSWORD = os.environ["PASSWORD"]  #Si estoy corriendo el pipeline va a encontrar esta variable en los secrets de github
# except KeyError:                      #Si no esta me levanta un KerError
#     import utils.secret_config
#     PASSWORD = utils.secret_config.PASSWORD #Si lo corro local me reconoce esta variable




@pytest.mark.smoke
@pytest.mark.regression
def test_entrar_al_automation_practice(login_set_up):       #El set_up es para que use la fixture
    page = login_set_up                     #xq la fixture set_up me retorna page
    home_page = HomePage(page)
    #expect(home_page.header_practice).to_be_visible()
    #expect(home_page.header_courses).to_be_visible()


# @pytest.mark.skip(reason="Not ready yet")
def test_entrar_al_automation_practice2(login_set_up):
    page = login_set_up
    home_page = HomePage(page)
    #expect(home_page.header_practice).to_be_visible()
    #expect(home_page.header_courses).to_be_visible()

# @pytest.mark.parametrize("email, password", [("student", "Password123" ), pytest.param("student", "PasswordZZZZZZZZZZ", marks=pytest.mark.xfail)]) #Se corren 2 tests. Se aclara que el 2do tiene que fallar xq el password es incorrecto.
# def test_parametrizando(set_up, email, password):
#     page = set_up
#     home_page = HomePage(page)
#     home_page.enter_username(email)
#     home_page.enter_password(password)
#     home_page.click_submit()
#     page.wait_for_timeout(2000)
#     home_page.click_logout()

@pytest.mark.skip
def test_parametrizando2(set_up):
    page = set_up
    home_page = HomePage(page)
    home_page.enter_username("student")
    home_page.enter_password(PASSWORD)   #Password123
    home_page.click_submit()
    page.wait_for_timeout(2000)
    home_page.click_logout()

# @pytest.mark.parametrize("email", ["student", pytest.param("studentZZZ", marks=pytest.mark.xfail)]) #envio 2 mails, 1 correcto y 1 incorrecto. Con el incorrecto debe fallar
# @pytest.mark.parametrize("password", ["Password123", pytest.param("PasswordZZZ", marks=pytest.mark.xfail)])  #envio 2 passwords, 1 correcto y 1 incorrecto. Con el incorrecto debe fallar
# def test_parametrizando_combinado(set_up, email, password):
#     """Este test al usar 2 parametrizaciones, se combinan,
#     por lo que va a correr 4 tests."""
#     page = set_up
#     home_page = HomePage(page)
#     home_page.enter_username(email)
#     home_page.enter_password(password)
#     home_page.click_submit()
#     page.wait_for_timeout(2000)
#     home_page.click_logout()


@pytest.mark.skip
def test_visual(page, assert_snapshot):
    page.goto("https://ambito.com.ar")
    assert_snapshot(page.screenshot(full_page=True)) #El full_page es opcional, me saca el screen de toda la pagina con el scrolleo hacia abajo
    """fail_fast=True .Es mas rapido, pero apenas encuentra un pixel que falla me falla el test."""
    #assert_snapshot(page.screenshot, fail_fast=True)
    """Si quiero que un elemento no sea considerado xq varia lo agrego a la mask, 
    que es la lista de los elementos que pueden variar"""
    #assert_snapshot(page.screenshot(mask=[locator1, locator2]))
    """Para que sea mas o menos estricto le pongo un threshold"""
    #assert_snapshot(page.screenshot(mask=[]), threshold=1) #Con el 1 va a pasar siempre, con 0.1 se pone mas estricto.




# To run
# pytest --headed --video=retain-on-failure --screenshot=only-on-failure --slowmo=400.
