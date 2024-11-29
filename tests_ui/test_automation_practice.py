import os

import allure
from playwright.sync_api import Playwright, sync_playwright, expect, Page
from pom.home_page import HomePage
import pytest


# try:
#     PASSWORD = os.environ["PASSWORD"]  #Si estoy corriendo el pipeline va a encontrar esta variable en los secrets de github
# except KeyError:                      #Si no esta me levanta un KerError
#     import utils.secret_config
#     PASSWORD = utils.secret_config.PASSWORD #Si lo corro local me reconoce esta variable


@pytest.mark.skip
@pytest.mark.smoke
@pytest.mark.regression
def test_entrar_al_automation_practice(login_set_up):  # El set_up es para que use la fixture
    page = login_set_up  # xq la fixture set_up me retorna page
    home_page = HomePage(page)
    # expect(home_page.header_practice).to_be_visible()
    # expect(home_page.header_courses).to_be_visible()


@pytest.mark.skip(reason="Not ready yet")
def test_entrar_al_automation_practice2(login_set_up):
    page = login_set_up
    home_page = HomePage(page)
    # expect(home_page.header_practice).to_be_visible()
    # expect(home_page.header_courses).to_be_visible()


@pytest.mark.parametrize("username, password", [("student", "Password123"), pytest.param("student", "PasswordZZZZZZZZZZ", marks=pytest.mark.xfail)], ids=["Login-Case1", "Login-Case2"])  # Se corren 2 tests. Se aclara que el 2do tiene que fallar xq el password es incorrecto.
#@allure.title("Se loguea con usuario {email} y contraseña {password}")
def test_parametrizando_pytest(set_up, username, password):
    page = set_up
    home_page = HomePage(page)
    allure.dynamic.parameter(name="username", value=username)
    allure.dynamic.parameter(name="password", value="*****")
    home_page.enter_username(username)
    home_page.enter_password(password)
    home_page.click_submit()
    page.wait_for_timeout(2000)
    home_page.click_logout()


PASSWORD = os.environ["PASSWORD"]  # Mejor estandar, me trae lo que tengo en el archivo .env (para usarlo antes pip install pytest_dotenv) si lo corro local. En cambio, si estoy corriendo el pipeline va a encontrar esta variable en los secrets de github. GREGAR EL ARCHIVO .env al gitignore!!!
# @pytest.mark.skip
def test_parametrizando2(set_up):
    page = set_up
    home_page = HomePage(page)
    home_page.enter_username("student")
    home_page.enter_password(PASSWORD)  # Password123
    home_page.click_submit()
    page.wait_for_timeout(2000)
    home_page.click_logout()


def test_berret():
    pass


def test_berret2():
    pass


def test_example_screenshot(set_up) -> None:
    page = set_up
    page.goto("https://www.google.com/")
    page.get_by_text("Argentina").click()
    expect(page.get_by_text("Argentina")).to_be_visible()


def test_berret3():
    pass


@allure.severity("minor")
def test_quality1():
    assert False


def test_quality2():
    assert False


@allure.description("Esta es una descripcion del test")
@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_quality3():
    assert True


def test_quality4():
    assert 1 == 1


@allure.title("Test Authentication")
@allure.description(
    "This test attempts to log into the website using a login and a password. Fails if any error happens. Note that this test does not test 2-Factor Authentication.")
@allure.tag("NewUI", "Essentials", "Authentication")
@allure.severity("critical")
@allure.label("owner", "John Doe")
@allure.link("https://dev.example.com/", name="Website")
@allure.issue("AUTH-123")
@allure.testcase("TMS-456")
def test_steps_en_allure(set_up):
    page = set_up
    home_page = HomePage(page)
    home_page.enter_username("student")
    home_page.enter_password("Password123")  # Password123
    with allure.step("Metiendo un paso en el test principal"):
        print("zaraza")
    home_page.click_submit()
    page.wait_for_timeout(2000)
    home_page.click_logout()


# todo: ver Visual comparisons  aca https://allurereport.org/docs/attachments/


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


#@pytest.mark.skip
def test_visual(page, assert_snapshot):
    page.goto("https://the-internet.herokuapp.com/download")
    assert_snapshot(page.screenshot(
        full_page=True))  # El full_page es opcional, me saca el screen de toda la pagina con el scrolleo hacia abajo
    """fail_fast=True .Es mas rapido, pero apenas encuentra un pixel que falla me falla el test."""
    # assert_snapshot(page.screenshot, fail_fast=True)
    """Si quiero que un elemento no sea considerado xq varia lo agrego a la mask, 
    que es la lista de los elementos que pueden variar"""
    # assert_snapshot(page.screenshot(mask=[locator1, locator2]))
    """Para que sea mas o menos estricto le pongo un threshold"""
    # assert_snapshot(page.screenshot(mask=[]), threshold=1) #Con el 1 va a pasar siempre, con 0.1 se pone mas estricto.


# To run
# pytest --headed --video=retain-on-failure --screenshot=only-on-failure --slowmo=400.

def test_download_files_and_attach_to_allure_report(page: Page):
    page.goto("https://the-internet.herokuapp.com/download")

    # Start waiting for the download
    with page.expect_download() as download_info:
        # Perform the action that initiates download
        page.locator("//a[text()='sample.pdf']").click()
    download = download_info.value

    working_directory_path = os.getcwd()
    pdf_path = os.path.join(working_directory_path, "test_data_for_download_files/sample.pdf")
    # Wait for the download process to complete and save the downloaded file somewhere
    download.save_as(pdf_path)
    assert os.path.exists(pdf_path), "El archivo PDF no fue descargado correctamente."
    #Attach PDF to the allure report
    allure.attach.file(
        pdf_path,
        name="Reporte Descargado",
        attachment_type=allure.attachment_type.PDF
    )

