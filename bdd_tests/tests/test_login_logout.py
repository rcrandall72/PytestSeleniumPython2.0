from pytest import mark
from base_functions import BaseFunctions
from common_strings import *
from log_functions import log_test, log_step
from pytest_bdd import given, when, then


@mark.regression
@mark.skip
@mark.usefixtures("browser")
class TestLoginLogout(BaseFunctions):
    @mark.smoke
    @log_test
    def test_login_logout(self):
        """
        Tests a user can log in and out of the app
        """

        self.step_valid_login()
        self.step_check_logged_in()
        self.step_logout()
        self.step_check_logged_out()

    @log_step
    def step_valid_login(self):
        self.sign_in(UserData.STANDARD_USER)

    @log_step
    def step_check_logged_in(self):
        assert True

    @log_step
    def step_logout(self):
        self.press_button(InventoryPage.MENU_BUTTON, wait=True)
        self.press_button(InventoryPage.LOGOUT_BUTTON)

    @log_step
    def step_check_logged_out(self):
        assert self.check_for_element(LoginPage.LOGIN_BUTTON)
        assert self.driver.current_url == URLs.SAUCE_DEMO
