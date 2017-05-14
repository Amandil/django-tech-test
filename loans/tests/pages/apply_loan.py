
class ApplyLoanPage():

    @staticmethod
    def complete_form(driver, amount, deadline, reason):
        # The ID cannot be used as the element is regenerated
        # The new element will not have the ID of the original
        # -- Will just use default amount for now --
        # driver.find_element_by_class_name("ws-number").send_keys(amount)
        driver.find_element_by_id('input_deadline').send_keys(deadline)
        driver.find_element_by_id('input_reason').send_keys(reason)
        driver.find_element_by_id('submit').click()
