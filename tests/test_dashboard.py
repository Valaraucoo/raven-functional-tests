from helpers import *


class TestDashboard:

    def test_admin_login(self, driver):
        login(driver)

        driver.get(BASE_URL + 'admin/')

        site_title = driver.find_element_by_tag_name('a')
        assert 'Django administration' in site_title.get_attribute('innerHTML')

        header = driver.find_element_by_id('content').find_element_by_tag_name('h1')
        assert 'Site administration' in header.get_attribute('innerHTML')

    def test_teacher_dashboard(self, driver):
        login(driver, 'teacher0@raven.test', 'teacher')

        boxes = {'Mój profil': 'profile', 'Moje Kursy': 'courses', 'Plan zajęć': 'schedule'}
        dashboard_central_bar_testing(driver, boxes)

        announcements = driver.find_element_by_xpath('//h4[@class="flex items-center pt-4 text-lg leading-6 font-medium text-gray-900 mb-2"]')
        assert 'Ostatnie ogłoszenia' in announcements.get_attribute('innerHTML')

        incoming = driver.find_element_by_xpath('//div[@class="flex flex-wrap "]')
        assert 'Nadchodzące wykłady' in incoming.get_attribute('innerHTML')
        assert 'Nadchodzące laboratoria' in incoming.get_attribute('innerHTML')

        dashboard_top_bar_testing(driver)

        sites = {'Strona Główna': '', 'Plan zajęć': 'schedule/', 'Kursy': 'courses/', 'Ogłoszenia': 'notices/'}
        sidebar_testing(driver, sites)

    def test_student_dashboard(self, driver):

        login(driver, 'student0@raven.test', 'student')

        boxes = {'Mój profil': 'profile', 'Moje Kursy': 'courses', 'Moje oceny': 'marks', 'Plan zajęć': 'schedule'}
        dashboard_central_bar_testing(driver, boxes)

        div1 = driver.find_element_by_xpath('//div[@class="flex flex-wrap mt-4 mb-4 "]')
        assert 'Najnowsze oceny' in div1.get_attribute('innerHTML')
        assert 'Oceny' in div1.get_attribute('innerHTML')

        div2 = driver.find_element_by_xpath('//div[@class="flex "]')
        assert 'Ostatnie ogłoszenia' in div2.get_attribute('innerHTML')
        assert 'Najnowsze zadania' in div2.get_attribute('innerHTML')

        div3 = driver.find_element_by_xpath('//div[@class="flex flex-wrap "]')
        assert 'Nadchodzące wykłady' in div3.get_attribute('innerHTML')
        assert 'Nadchodzące laboratoria' in div3.get_attribute('innerHTML')

        dashboard_top_bar_testing(driver)

        sites = {'Strona Główna': '', 'Plan zajęć': 'schedule/', 'Kursy': 'courses/', 'Ogłoszenia': 'notices/', 'Zadania': 'assignments/', 'Oceny': 'marks/'}
        sidebar_testing(driver, sites)
