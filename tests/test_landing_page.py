from helpers import *


class TestLandingPageLoading:

    def test_get_base_url(self, driver):

        driver.get(BASE_URL)

        # waiting for animation
        time.sleep(2)

        button_login = driver.find_element_by_css_selector('button')
        assert 'Zaloguj się' in button_login.get_attribute('innerHTML')

        button_modal = driver.find_element_by_id('modal-trigger')
        assert 'Czy jesteś w tym serwisie po raz pierwszy?' in button_modal.get_attribute('innerHTML')

        button_modal.click()

        button_modal_close = driver.find_element_by_id('modal-trigger2')
        assert 'Cancel' in button_modal_close.get_attribute('innerHTML')
        button_modal_close.click()

        support_link = driver.find_element_by_xpath('//*[text()[contains(., "Support")]]')
        driver.execute_script("arguments[0].click();", support_link)
        assert 'Witamy w supporcie!' in driver.find_element_by_tag_name('h2').get_attribute('innerHTML')

    def test_login_to_dashboard(self, driver):

        login()
