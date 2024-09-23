

class HomePage:
    def __init__(self, page):
        self.header_practice = page.get_by_role("link", name="Practice", exact=True)
        self.header_courses = page.get_by_role("link", name="Courses")
        self.username_box = page.get_by_label("Username")
        self.password_box = page.get_by_label("Password")
        self.submit_button = page.get_by_role("button", name="Submit")
        self.logout_button = page.get_by_role("link", name="Log out")

    def enter_username(self, username):
        self.username_box.fill(username)

    def enter_password(self, password):
        self.password_box.fill(password)

    def click_submit(self):
        self.submit_button.click()

    def click_logout(self):
        self.logout_button.click(timeout=2000)
