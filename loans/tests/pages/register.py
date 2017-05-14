
class RegisterPage():

    @staticmethod
    def complete_form(driver, first_name, last_name, email, password, phone_number):

        driver.find_element_by_id('input_first_name').send_keys(first_name)
        driver.find_element_by_id('input_last_name').send_keys(last_name)
        driver.find_element_by_id('input_email').send_keys(email)
        driver.find_element_by_id('input_password').send_keys(password)
        driver.find_element_by_id('input_phone_number').send_keys(phone_number)
        driver.find_element_by_id('submit').click()
