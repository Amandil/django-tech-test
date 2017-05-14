import unittest, os

from django.test import TestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test import LiveServerTestCase

from .pages.sign_in import SignInPage
from .pages.register import RegisterPage

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

        # We must end up on the authentication page
        self.assertEquals(TITLE_PREFIX + 'Sign In', self.driver.title);

        SignInPage.click_register_link(self.driver)

        # We must end up on the registration page
        self.assertEquals(TITLE_PREFIX + 'Register', self.driver.title);

        # Registering
        RegisterPage.complete_form(self.driver, 'John', 'Doe', 'john.doe@acme.com', 'correct-horse-battery-staple', '+44 7765 222 4567')

        # No alerts should appear
        error_message = self.get_element('error-message').text
        self.assertEquals('', error_message)

        # PhantomJS fails to follow redirects
        # Manually redirecting
        self.driver.get(self.live_server_url + "/")

        # We must end up back on the authentication page
        self.assertEquals(TITLE_PREFIX + 'Sign In', self.driver.title);

        # Signing in must work
        SignInPage.sign_in(self.driver, 'john.doe@acme.com', 'correct-horse-battery-staple')

        # No alerts should appear
        error_message = self.get_element('error-message').text
        self.assertEquals('', error_message)

        # PhantomJS fails to follow some redirects
        # Manually redirecting, next assertion will fail if logged in failed
        self.driver.get(self.live_server_url + "/dashboard")

        # User should be redirected to the homepage/dashboard once logged in
        self.assertEquals(TITLE_PREFIX + 'Homepage', self.driver.title);

    '''
    Users must not be able to access anything other than the sign in page unless
    they are signed in
    '''
    def test_access(self):
        pass

    # Shortcut for find_element_by_id
    def get_element(self, id):
        return self.driver.find_element_by_id(id)
