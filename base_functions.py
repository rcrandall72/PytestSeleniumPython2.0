import string
import random
from time import sleep
import logging
from pytest import mark

from common_strings import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException


@mark.usefixtures("browser")
class BaseFunctions:

    logging.basicConfig(
        filename="testrun.log",
        level=logging.DEBUG,
        format='%(name)s - %(levelname)s - %(message)s'
    )

    @staticmethod
    def log(func):
        def wrapper(*args, **kwargs):
            # Log method name and parameters
            logging.debug(f"{func.__name__}({args}, {kwargs})")
        return wrapper

    @log
    def sign_in(self, email):
        """
        Signs the user in based on the email passed in
        :param email: The email of the user
        """
        # Login
        self.send_keys(LoginPage.USERNAME_FIELD, email)
        self.send_keys(LoginPage.PASSWORD_FIELD, UserData.PASSWORD)
        self.press_button(LoginPage.LOGIN_BUTTON)

    @log
    def press_button(self, button_id, button_type=By.ID, iteration=0,
                     text="", timeout=30, child_path="", wait=False) -> str:
        """
        Presses the button based on the id passed in
        :param button_id: The id of the button to press
        :param button_type: The type of the button to press
        :param iteration: The iteration of the button to press
        :param text: The text of the button to press
        :param timeout: The time to wait to find the button
        :param child_path: The child path of the field element
        :param wait: If True, waits a second after clicking
        :return: text
        """

        # Auto-set button type if list
        if isinstance(button_id, list):
            button_id = "//" + button_id[0] + "[@" + button_id[1] + "='" + button_id[2] + "']" + child_path
            button_type = By.XPATH

        try:
            button_to_press = WebDriverWait(self.driver, timeout).until(
                ec.presence_of_all_elements_located((button_type, button_id)))
        except TimeoutException:
            raise Exception(f"Unable to find element: {button_id}")
        else:
            if text:  # Find by text
                text_list = []
                for button in button_to_press:
                    if button.text == text:
                        text_list.append(button)
                text_list[iteration].click()
            else:  # Find by iteration
                button_to_press[iteration].click()

            if wait:
                sleep(5)
            return text

    @log
    def send_keys(self, field_id, text, field_type=By.ID, iteration=0, timeout=30, child_path="") -> str:
        """
        Presses the button based on the id passed in
        :param field_id: The id of the field to send keys to
        :param text: The text to send to the field
        :param field_type: The type of the field to send keys to
        :param iteration: The iteration of the field to send keys to
        :param timeout: The time to wait to find the field
        :param child_path: The child path of the field element
        :return: text
        """

        # Auto-set field type if list
        if isinstance(field_id, list):
            field_id = "//" + field_id[0] + "[@" + field_id[1] + "='" + field_id[2] + "']" + child_path
            field_type = By.XPATH

        try:
            field = WebDriverWait(self.driver, timeout).until(
                ec.presence_of_all_elements_located((field_type, field_id)))
        except TimeoutException:
            raise Exception(f"Unable to find element: {field_id}")
        else:
            field[iteration].send_keys(text)
            return text

    @log
    def check_for_element(self, element_id, element_type=By.ID, child_path="", timeout=5, text="") -> bool:
        """

        :param element_id:
        :param element_type:
        :param child_path:
        :param timeout:
        :param text:
        :return:
        """

        # Auto-set field type if list
        if isinstance(element_id, list):
            element_id = "//" + element_id[0] + "[@" + element_id[1] + "='" + element_id[2] + "']" + child_path
            element_type = By.XPATH

        try:
            elements = WebDriverWait(self.driver, timeout).until(
                ec.presence_of_all_elements_located((element_type, element_id)))
            if text:
                for element in elements:
                    if element.text == text:
                        return True
                return False
            else:
                return True
        except TimeoutException:
            return False

    @log
    def assign_element(self, element_id, element_type=By.ID, child_path="", timeout=5, text="", iteration=0):
        """
        Assigns the element based on the id and type given

        :param element_id: The id of the element to assign
        :param element_type: The type of the element to assign
        :param child_path: The child path of the element to assign
        :param timeout: The timeout to find the element to assign
        :param text: The text of the element to find
        :param iteration: The iteration of the element to assign
        :return: element
        """

        # Auto-set field type if list
        if isinstance(element_id, list):
            element_id = "//" + element_id[0] + "[@" + element_id[1] + "='" + element_id[2] + "']" + child_path
            element_type = By.XPATH

        try:
            elements = WebDriverWait(self.driver, timeout).until(
                ec.presence_of_all_elements_located((element_type, element_id)))
        except TimeoutException:
            raise Exception(f"Unable to assign element: {element_id}")
        else:
            if text:  # Find by text
                text_list = []
                for element in elements:
                    if element.text == text:
                        text_list.append(element)
                return text_list[iteration]
            else:  # Find by iteration
                return elements[iteration]

    @log
    def assign_elements(self, element_id, element_type=By.ID, child_path="", timeout=5, text=""):
        """
        Assigns the elements based on the id and type given

        :param element_id: The id of the elements to assign
        :param element_type: The type of the elements to assign
        :param child_path: The child path of the elements to assign
        :param timeout: The timeout to find the elements to assign
        :param text: The text of the elements to find
        :return: elements
        """

        # Auto-set field type if list
        if isinstance(element_id, list):
            element_id = "//" + element_id[0] + "[@" + element_id[1] + "='" + element_id[2] + "']" + child_path
            element_type = By.XPATH

        try:
            elements = WebDriverWait(self.driver, timeout).until(
                ec.presence_of_all_elements_located((element_type, element_id)))
        except TimeoutException:
            raise Exception(f"Unable to assign element: {element_id}")
        else:
            if text:  # Find by text
                text_list = []
                for element in elements:
                    if element.text == text:
                        text_list.append(element)
                return text_list
            else:
                return elements

    @staticmethod
    @log
    def get_random_string(length=5) -> str:
        """
        Returns a random string with the length provided
        :return: str
        """

        return ''.join(random.choices(string.ascii_lowercase, k=length))
