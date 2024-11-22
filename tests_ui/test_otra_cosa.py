from playwright.sync_api import Playwright, sync_playwright, expect
from pom.home_page import HomePage


def test_entrar_al_automation_practice3(login_set_up):
    page = login_set_up
    home_page = HomePage(page)
    #expect(home_page.header_practice).to_be_visible()
    #expect(home_page.header_courses).to_be_visible()
