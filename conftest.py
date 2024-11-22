import pytest
from playwright.sync_api import Playwright
from pom.home_page import HomePage


# @pytest.fixture()
# def set_up(page):   # def set_up(playwright: Playwright):    NO LO NECESITO XQ PLAYWRIGHT YA VIENE CON PAGE (una fixture propia)
#     #browser = playwright.chromium.launch(headless=False)
#    #context = browser.new_context() #Si creo esto y no lo cierro se me quedan las ventanas abiertas. En la linea 10 puedo poner page en vez de browser y mutear linea 9 y 10 y sacar el teardown xq cierra sola.
#    #page = context.new_page()
#     page.goto("https://practicetestautomation.com/practice-test-login/")
#     yield page
#     page.close()
#
#
# @pytest.fixture()
# def login_set_up(set_up):      #Hago que la fixture este tenga a su vez la fixture anterior
#     page = set_up              #como el set_up anterior me retorna el page, aca se lo asigno a una variable (page) para usarla
#     home_page = HomePage(page)
#     home_page.enter_username("student")
#     home_page.enter_password("Password123")
#     home_page.click_submit()
#     page.wait_for_timeout(2000)
#     home_page.click_logout()
#
#     yield page


# ESTE EJEMPLO ES SIMILAR AL DE ARRIBA PERO CREO UN NUEVO CONTEXT, ES DECIR, ABRE UNA NUEVA TAB PERO YA ESTA LOGUEADO.
#LO DE ARRIBA ESTA BIEN, PERO SE LOGUEA CADA VEZ, PARA CADA TEST. ESTE ES UN NUEVO APPROACH DONDE SE ABRE UNA NUEVA TAB DONDE YA ESTA LOGUEADO.
@pytest.fixture(scope="session")
def context_creation(playwright):
    browser = playwright.chromium.launch()#(headless=False) #Probar context = browser.new_context(http_credentials={'username': 'admin', 'password': 'admin'})
    context = browser.new_context()
    page = context.new_page()  # open new tab
    page.goto("https://practicetestautomation.com/practice-test-login/")
    home_page = HomePage(page)
    home_page.enter_username("student")
    home_page.enter_password("Password123")
    home_page.click_submit()
    page.wait_for_load_state(timeout=10000) #dejo los 2 waits a proposito
    page.wait_for_timeout(2000)
    context.storage_state(path='state.json')   #Se crea solo un archivo que me guarda todas las cookies y tokens de la pagina, y despues los puedo usar. Me da un mejor test isolation.
    yield context


#@pytest.fixture()  #CREO DISTINTAS VENTANAS DE BROWSERS
# def login_set_up(context_creation, browser):   #Si uso esta opcion no hace falta que el context_creation tenga yield context
#     context = browser.new_context(storage_state='state.json')  #Al haber guardado el context en un archivo en la linea 43, ahora lo uso aca y en vez de abrir una nueva tab me abre una nueva pagina por cada test.
#     page = context.new_page()
#     page.goto("https://practicetestautomation.com")
#     page.wait_for_timeout(2000)
#     yield page
#     context.close()



# Otra opcion de esta ultima fixture. #CREO DISTINTAS INSTANCES DE BROWSERS, mejor que solo ventanas nuevas.
@pytest.fixture()
def login_set_up(context_creation, playwright):
    browser = playwright.chromium.launch()#(headless=False, slow_mo=400)
    context = browser.new_context(storage_state='state.json')  #Al haber guardado el context en un archivo en la linea 43, ahora lo uso aca y en vez de abrir una nueva tab me abre una nueva pagina por cada test.
    page = context.new_page()
    page.goto("https://practicetestautomation.com")
    page.wait_for_timeout(2000)
    yield page
    browser.close()
