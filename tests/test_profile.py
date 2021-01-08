import random
import string

from helpers import *


class TestProfile:

    def test_profile_loading(self, driver):

        login(driver, "teacher0@raven.test", "teacher")

        driver.get(BASE_URL + 'profile/')

        elements = ['Edytuj mój profil', 'Nauczyciel akademicki', 'Bieżące Kursy', 'O mnie:', 'Informacje dodatkowe:']
        for element in elements:
            assert element in driver.page_source

        courses_count = len(driver.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr'))

        if courses_count != 0:
            course = driver.find_element_by_xpath('//tbody/tr[1]/td[1]/a')
            driver.execute_script("arguments[0].click();", course)

            # check course link and rendering
            course_elements = ['Główny prowadzący', 'Prowadzący', 'Ogłoszenia', 'Edytuj kurs', 'Zarządzaj grupami',
                               'Dostępne wykłady', 'Dostępne laboratoria']

            assert BASE_URL + 'courses/' in driver.current_url
            for element in course_elements:
                assert element in driver.page_source

            driver.get(BASE_URL + 'profile/')

            # check teacher's link and his site rendering
            teacher = driver.find_element_by_xpath('//tbody/tr[1]/td[3]/a')
            driver.execute_script("arguments[0].click();", teacher)

            profile_elements = ['O mnie:', 'Informacje dodatkowe', 'Nauczyciel akademicki']
            assert BASE_URL + 'profile/' in driver.current_url
            for element in profile_elements:
                assert element in driver.page_source

    def test_profile_editing(self, driver):

        login(driver, "teacher0@raven.test", "teacher")

        driver.get(BASE_URL + 'profile/edit/')

        data = {'first_name': '', 'last_name': '', 'address': '', 'description': ''}

        for field in data.keys():
            data[field] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

        for name in data.keys():
            field = driver.find_element_by_name(name)
            field.clear()
            field.send_keys(data[name])

        button = driver.find_element_by_xpath('//form[@method="POST"][2]/button')
        button.click()

        driver.get(BASE_URL + 'profile/')

        for key in data.keys():
            assert data[key] in driver.page_source
