import allure


class HomePage:
    def __init__(self, page):
        self.page = page
        self.header_practice = page.get_by_role("link", name="Practice", exact=True)
        self.header_courses = page.get_by_role("link", name="Courses")
        self.username_box = page.get_by_label("Username")
        self.password_box = page.get_by_label("Password")
        self.submit_button = page.get_by_role("button", name="Submit")
        self.logout_button = page.get_by_role("link", name="Log out")

    @allure.step("Entrar nombre de usuario")
    def enter_username(self, username):
        self.username_box.fill(username)
        #allure.attach(self.page.screenshot(), name="username_entry_screenshot", attachment_type=allure.attachment_type.PNG)

    #@allure.step("Entrar password")
    def enter_password(self, password):
        #allure.dynamic.parameter(name="password", value="***", excluded=True)
        #allure.dynamic.parameter(name="password", value=password, mode=allure.parameter_mode.MASKED)
        with allure.step("Entrando el password con context step"):
            self.password_box.fill(password)
            with allure.step("A ver si hago un sub step aca"):
                print("Esto va en un substep")

    #@allure.step("Submitear el login")
    def click_submit(self):
        with allure.step("Clickeando submit con context step"):
            self.submit_button.click()

    @allure.step("Desloguearse")
    def click_logout(self):
        self.logout_button.click(timeout=2000)
