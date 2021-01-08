from helpers import *


class TestCourseScreen:

    def test_teacher_course_screen(self, driver):

        login(driver, 'teacher0@raven.test', 'teacher')

        course_screen_testing(driver, False)

    def test_student_course_screen(self, driver):

        # login(driver, 'student1@raven.test', 'student')

        course_screen_testing(driver, True)
