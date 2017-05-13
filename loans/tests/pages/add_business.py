from selenium.webdriver.support.select import Select

class AddBusinessPage():

    @staticmethod
    def complete_form(driver, crn, business_name, sector, address_1, address_2, city, postcode):
        driver.find_element_by_id('input_crn').send_keys(crn)
        driver.find_element_by_id('input_name').send_keys(business_name)
        sector_select = Select(driver.find_element_by_id('input_sector'))
        sector_select.select_by_visible_text(sector)
        driver.find_element_by_id('input_address_1').send_keys(address_1)
        driver.find_element_by_id('input_address_2').send_keys(address_2)
        driver.find_element_by_id('input_city').send_keys(city)
        driver.find_element_by_id('input_postcode').send_keys(postcode)
        driver.find_element_by_id('submit').click()
