import unittest, os

from django.test import TestCase

from selenium import webdriver

ENDPOINT = os.environ['LOANS_URL']
TITLE_PREFIX = 'GrowthStreet Loans - '

class TestRegistration(TestCase):

    def setUp(self):
        self.driver = webdriver.PhantomJS()

    def test_journey_register(self):
        self.driver.get(ENDPOINT + "/admin")

        # We must end up on the authentication page
        self.assertEquals(TITLE_PREFIX + 'Sign In', self.driver.title);

        # Clicking on registration link
        self.get_element('link_register').click()

        # We must end up on the registration page
        self.assertEquals(TITLE_PREFIX + 'Register', self.driver.title);

        # Registering
        self.get_element('input_first_name').send_keys('John')
        self.get_element('input_last_name').send_keys('Doe')
        self.get_element('input_email').send_keys('john.doe@acme.com')
        self.get_element('input_password').send_keys('correct-horse-battery-staple')
        self.get_element('input_phone_number').send_keys('+44 7765 222 4567')
        self.get_element('submit').click()

        # We must end up back on the authentication page
        self.assertEquals(TITLE_PREFIX + 'Sign In', self.driver.title);

    def test_login(self):
        pass

    def test_access(self):
        pass

    # Shortcut for find_element_by_id
    def get_element(self, id):
        return self.driver.find_element_by_id(id)
