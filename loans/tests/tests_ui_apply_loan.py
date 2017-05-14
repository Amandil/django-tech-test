import unittest, os

from django.test import TestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test import LiveServerTestCase

TITLE_PREFIX = 'GrowthStreet Loans - '

from .pages.sign_in import SignInPage
from .pages.register import RegisterPage
from .pages.add_business import AddBusinessPage

from loans.models import Business

class TestRegistration(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.PhantomJS()
        super(TestRegistration, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(TestRegistration, self).tearDown()

    '''
    Users must be able to add a business and apply for a loan
    '''
    def test_journey_apply_loan_new_bussiness(self):

        # Registering a new user
        self.driver.get(self.live_server_url + "/")
        SignInPage.click_register_link(self.driver)
        RegisterPage.complete_form(self.driver, 'John', 'Doe', 'john.doe@acme.com', 'correct-horse-battery-staple', '+44 7765 222 4567')

        # User should be logged in and dashboard should work right after registration
        self.driver.get(self.live_server_url + "/dashboard")

        self.assertEquals(TITLE_PREFIX + 'Homepage', self.driver.title);

        # Initially, no loans should be present
        loan_list_test = self.get_element("loan-list").text
        self.assertTrue("don't seem to have" in loan_list_test)

        # Starting to apply for a loan
        self.get_element('apply-loan').click()

        # We should end up on the first step of the application
        self.assertEquals(TITLE_PREFIX + 'Loan Application - Step 1', self.driver.title);

        # Initially, no businesses should exist
        loan_list_test = self.get_element("business-list").text
        self.assertTrue("don't seem to have" in loan_list_test)

        # Adding a business
        self.get_element('add-business').click()

        # We should end up on the add business page
        self.assertEquals(TITLE_PREFIX + 'Loan Application - Add Business', self.driver.title);

        # Completing the form
        crn = "09264172"
        AddBusinessPage.complete_form(self.driver, crn, 'ACME Inc.', 'Retail', 'Building and Number', 'Street', 'London', 'W8 5EH')

        # self.driver.get(self.live_server_url + "/loan_application/3/" + crn)

        # We should end up on the loan form page
        self.assertTrue(TITLE_PREFIX + 'Loan Application - Step 2', self.driver.title)


    # Shortcut for find_element_by_id
    def get_element(self, id):
        return self.driver.find_element_by_id(id)
