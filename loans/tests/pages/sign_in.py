
class SignInPage():

    @staticmethod
    def click_register_link(driver):

        # Clicking on registration link
        driver.find_element_by_id('link_register').click()

    @staticmethod
    def sign_in(driver, username, password):

        driver.find_element_by_id('input_email').send_keys(username)
        driver.find_element_by_id('input_password').send_keys(password)
        driver.find_element_by_id('submit').click()
