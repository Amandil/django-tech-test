import unittest, os

from django.test import TestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test import LiveServerTestCase

TITLE_PREFIX = 'GrowthStreet Loans - '

class TestRegistration(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.PhantomJS()
        super(TestRegistration, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(TestRegistration, self).tearDown()

    '''
    Users must be able to register and sign in
    '''
    def test_journey_register(self):

        self.driver.get(self.live_server_url + "/")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "link_register"))
        )

        # We must end up on the authentication page
        self.assertEquals(TITLE_PREFIX + 'Sign In', self.driver.title);

        # Clicking on registration link
        self.get_element('link_register').click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "input_first_name"))
        )

        # We must end up on the registration page
        self.assertEquals(TITLE_PREFIX + 'Register', self.driver.title);

        # Registering
        self.get_element('input_first_name').send_keys('John')
        self.get_element('input_last_name').send_keys('Doe')
        self.get_element('input_email').send_keys('john.doe@acme.com')
        self.get_element('input_password').send_keys('correct-horse-battery-staple')
        self.get_element('input_phone_number').send_keys('+44 7765 222 4567')
        self.get_element('submit').click()

        # No alerts should appear
        error_message = self.get_element('error-message').text
        self.assertEquals('', error_message)

        # PhantomJS fails to follow redirects
        # Manually redirecting
        self.driver.get(self.live_server_url + "/")

        # We must end up back on the authentication page
        self.assertEquals(TITLE_PREFIX + 'Sign In', self.driver.title);

        # Signing in must work
        self.get_element('input_email').send_keys('john.doe@acme.com')
        self.get_element('input_password').send_keys('correct-horse-battery-staple')
        self.get_element('submit').click()

        # No alerts should appear
        error_message = self.get_element('error-message').text
        self.assertEquals('', error_message)

        # PhantomJS fails to follow redirects
        # Manually redirecting
        # self.driver.get(self.live_server_url + "/")

        # User should be redirected to the homepage/dashboard once logged in
        # self.assertEquals(TITLE_PREFIX + 'Homepage', self.driver.title);

    '''
    Users must not be able to access anything other than the sign in page unless
    they are signed in
    '''
    def test_access(self):
        pass

    # Shortcut for find_element_by_id
    def get_element(self, id):
        return self.driver.find_element_by_id(id)
