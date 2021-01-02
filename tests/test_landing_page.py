import time


class TestLandingPageLoading:
    BASE_URL = 'http://127.0.0.1:8080/'

    def test_get_base_url(self, driver):
        driver.get(self.BASE_URL)

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

        support_link = driver.find_element_by_css_selector('a[href*="support"]')
        assert 'Support' in support_link.get_attribute('innerHTML')

    def test_login_to_dashboard(self, driver):
        driver.get(self.BASE_URL)
        assert driver.current_url == self.BASE_URL + 'login/'

        # waiting for animation
        time.sleep(2)

        email_input = driver.find_element_by_id('id_email')
        password_input = driver.find_element_by_id('id_password')
        login_btn = driver.find_element_by_css_selector('button')

        email_input.send_keys('admin@admin.com')
        password_input.send_keys('admin')

        login_btn.click()
        assert driver.current_url == self.BASE_URL
