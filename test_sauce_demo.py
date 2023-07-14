from pytest import mark
from base_functions import BaseFunctions
from common_strings import *


@mark.regression
@mark.usefixtures("browser")
class TestSauceDemo(BaseFunctions):

    @mark.smoke
    def test_login_logout(self):
        """
        Tests a user can log in and out of the app
        """
        # Login as user
        self.sign_in(UserData.STANDARD_USER)

        # Logout of app
        self.press_button(InventoryPage.MENU_BUTTON, wait=True)
        self.press_button(InventoryPage.LOGOUT_BUTTON)

        # Assert user is logged out and back on login page
        assert self.check_for_element(LoginPage.LOGIN_BUTTON)
        assert self.driver.current_url == URLs.SAUCE_DEMO

    def test_cannot_login_with_locked_user(self):
        """
        Tests a user cannot log in with a locked user
        """
        # Login as user
        self.sign_in(UserData.LOCKED_OUT_USER)

        # Check user is not signed in and has correct error message
        assert self.check_for_element(LoginPage.ERROR_MESSAGE)
        assert self.assign_element(LoginPage.ERROR_MESSAGE).text == LoginPage.LOCKED_OUT_ERROR_MESSAGE

    def test_user_signing_credential_errors(self):
        """
        Tests a user must provide good credentials in order to log in
        """

        # Test Error message with no credentials
        self.press_button(LoginPage.LOGIN_BUTTON)
        assert self.check_for_element(LoginPage.ERROR_MESSAGE)
        assert self.assign_element(LoginPage.ERROR_MESSAGE).text == LoginPage.USERNAME_REQUIRED_MESSAGE

        # Test Error message with only username
        self.send_keys(LoginPage.USERNAME_FIELD, self.get_random_string())
        self.press_button(LoginPage.LOGIN_BUTTON)
        assert self.check_for_element(LoginPage.ERROR_MESSAGE)
        assert self.assign_element(LoginPage.ERROR_MESSAGE).text == LoginPage.PASSWORD_REQUIRED_MESSAGE

        # Test Error message with bad username & password
        self.send_keys(LoginPage.PASSWORD_FIELD, self.get_random_string())
        self.press_button(LoginPage.LOGIN_BUTTON)
        assert self.check_for_element(LoginPage.ERROR_MESSAGE)
        assert self.assign_element(LoginPage.ERROR_MESSAGE).text == LoginPage.USERNAME_PASSWORD_MISMATCH_MESSAGE

    @mark.smoke
    def test_buy_item(self):
        """
        Tests a user can add an item to the cart and buy it
        """
        # Login as user
        self.sign_in(UserData.STANDARD_USER)

        # Add item to cart
        self.press_button(InventoryPage.ADD_BACKPACK_TO_CART)
        assert self.assign_element(InventoryPage.SHOPPING_CART_CONTAINER).text == "1"

        # Open cart and check we have the right itme
        self.press_button(InventoryPage.SHOPPING_CART_CONTAINER)
        assert self.assign_element(CartPage.INVENTORY_ITEM_NAME).text == InventoryPage.SAUCE_LABS_BACKPACK

        # Continue to finalize purchase
        self.press_button(CartPage.CHECKOUT_BUTTON)
        self.send_keys(CartPage.FIRST_NAME_FIELD, self.get_random_string())
        self.send_keys(CartPage.LAST_NAME_FIELD, self.get_random_string())
        self.send_keys(CartPage.ZIP_FIELD, self.get_random_string())
        self.press_button(CartPage.CONTINUE_BUTTON)
        self.press_button(CartPage.FINISH_BUTTON)

        # Assert completion
        assert self.check_for_element(CartPage.CONFIRMATION_CONTAINER)
        
    def test_social_media_links(self):
        """
        Tests the social media links route correctly
        """
        # Login as user
        self.sign_in(UserData.STANDARD_USER)

        # Switch to desired window handle
        def check_window_handle(url):
            for handle in self.driver.window_handles:
                self.driver.switch_to.window(handle)
                if self.driver.current_url == url or url in self.driver.current_url:
                    return
            raise Exception(f"{url} is not opened on any tab")
        
        # Open Twitter Link
        self.press_button(FooterPage.SOCIAL_TWITTER, wait=True)
        check_window_handle(FooterPage.TWITTER_URL)
        assert self.driver.current_url == FooterPage.TWITTER_URL

        # Open Facebook
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.press_button(FooterPage.SOCIAL_FACEBOOK, wait=True)
        check_window_handle(FooterPage.FACEBOOK_URL)
        assert self.driver.current_url == FooterPage.FACEBOOK_URL

        # Open LinkedIn
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.press_button(FooterPage.SOCIAL_LINKEDIN, wait=True)
        check_window_handle(FooterPage.LINKEDIN_URL)
        assert FooterPage.LINKEDIN_URL in self.driver.current_url

    def test_sort_products(self):
        """
        Verifies products can be sorted in a certain order
        """
        # Login as user
        self.sign_in(UserData.STANDARD_USER)
        
        # Sort products by A to Z
        self.press_button(InventoryPage.SORT_CONTAINER)
        self.press_button(InventoryPage.A_TO_Z_OPTION)
        item_names = self.assign_elements(InventoryPage.INVENTORY_ITEM_NAME)
        for i in range(0, len(item_names)-1):
            assert item_names[i].get_attribute('innerText') < item_names[i+1].get_attribute('innerText')

        # Sort products by A to Z
        self.press_button(InventoryPage.SORT_CONTAINER)
        self.press_button(InventoryPage.Z_TO_A_OPTION)
        item_names = self.assign_elements(InventoryPage.INVENTORY_ITEM_NAME)
        for i in range(0, len(item_names)-1):
            assert item_names[i].get_attribute('innerText') > item_names[i+1].get_attribute('innerText')

        # Sort products by low to high
        self.press_button(InventoryPage.SORT_CONTAINER)
        self.press_button(InventoryPage.LOW_TO_HIGH_PRICE_OPTION)
        item_prices = self.assign_elements(InventoryPage.INVENTORY_ITEM_PRICE)
        for i in range(0, len(item_prices)-1):
            assert float(item_prices[i].get_attribute('innerText')[1:])\
                   <= float(item_prices[i+1].get_attribute('innerText')[1:])

        # Sort products by high to low
        self.press_button(InventoryPage.SORT_CONTAINER)
        self.press_button(InventoryPage.HIGH_TO_LOW_PRICE_OPTION)
        item_prices = self.assign_elements(InventoryPage.INVENTORY_ITEM_PRICE)
        for i in range(0, len(item_prices)-1):
            assert float(item_prices[i].get_attribute('innerText')[1:])\
                   >= float(item_prices[i+1].get_attribute('innerText')[1:])