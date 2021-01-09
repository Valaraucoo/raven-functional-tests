from helpers import *
from random import choice


class TestCourseScreen:

    def test_teacher_course_screen(self, driver):

        login(driver, 'teacher0@raven.test', 'teacher')

        course_screen_testing(driver, False)

    def test_student_course_screen(self, driver):

        login(driver, 'student1@raven.test', 'student')

        course_screen_testing(driver, True)

    def test_course_list_filtering(self, driver):

        login(driver, 'teacher0@raven.test', 'teacher')

        driver.get(BASE_URL + 'courses/')

        # collecting data about courses
        courses_data = get_courses_data(driver)
        courses_data_keys = list(courses_data.keys())

        selected_values = {'Course_name': choice(courses_data_keys),
                           'Teacher': choice(courses_data[choice(courses_data_keys)]['Teachers'])[1],
                           'Exam': courses_data[choice(courses_data_keys)]['Exam'],
                           'Language': courses_data[choice(courses_data_keys)]['Language']}

        selected_values['Language'] = 'Angielski' if selected_values['Language'] == 'EN' else 'Polski'

        course_name_input = driver.find_element_by_name('name')
        teacher_input = driver.find_element_by_name('teacher')
        exam_select = driver.find_element_by_name('has_exam')
        language_select = driver.find_element_by_xpath('//div[@class="mb-4 border-b"]/div[3]/div/div/select')

        filter_button = driver.find_element_by_xpath("//*[contains(text(), 'Filtruj')]")
        reset_button = driver.find_element_by_xpath("//*[contains(text(), 'Resetuj')]")

        # filtering
        course_name_input.send_keys(selected_values['Course_name'])
        filter_button.click()

        filtered_courses = list(get_courses_data(driver).keys())
        other_courses = list(set(courses_data_keys) - set(get_courses_data(driver).keys()))

        for course in filtered_courses:
            assert selected_values['Course_name'] in course

        for course in other_courses:
            assert selected_values['Course_name'] not in course

        reset_button.click()
        teacher_input.send_keys(selected_values['Teacher'])
        filter_button.click()

        filtered_courses = list(get_courses_data(driver).keys())
        other_courses = list(set(courses_data_keys) - set(get_courses_data(driver).keys()))

        for course in filtered_courses:
            assert any([(selected_values['Teacher'] in courses_data[course]['Teachers'][i][1])
                        for i in range(len(courses_data[course]['Teachers']))])

        for course in other_courses:
            assert any([(selected_values['Teacher'] not in courses_data[course]['Teachers'][i][1])
                        for i in range(len(courses_data[course]['Teachers']))])

        reset_button.click()
        exam_select.find_element_by_xpath(f'./option[text()="{selected_values["Exam"]}"]').click()
        filter_button.click()

        filtered_courses = list(get_courses_data(driver).keys())
        other_courses = list(set(courses_data_keys) - set(get_courses_data(driver).keys()))

        for course in filtered_courses:
            assert selected_values['Exam'] in courses_data[course]['Exam']

        for course in other_courses:
            assert selected_values['Exam'] not in courses_data[course]['Exam']

        reset_button.click()
        language_select.find_element_by_xpath(f'./option[text()="{selected_values["Language"]}"]').click()
        filter_button.click()

        filtered_courses = list(get_courses_data(driver).keys())
        other_courses = list(set(courses_data_keys) - set(get_courses_data(driver).keys()))

        for course in filtered_courses:
            assert selected_values['Language'] in courses_data[course]['Language']

        for course in other_courses:
            assert selected_values['Language'] not in courses_data[course]['Language']
