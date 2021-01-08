import time


BASE_URL = 'http://127.0.0.1:8080/'


def login(driver, email='admin@admin.com', password='admin'):
    driver.get(BASE_URL)
    assert driver.current_url == BASE_URL + 'login/'

    # waiting for animation
    time.sleep(2)

    email_input = driver.find_element_by_id('id_email')
    password_input = driver.find_element_by_id('id_password')
    login_btn = driver.find_element_by_css_selector('button')

    email_input.send_keys(email)
    password_input.send_keys(password)

    login_btn.click()
    assert driver.current_url == BASE_URL


def dashboard_central_bar_testing(driver, links):

    for name in links.keys():
        grid = driver.find_element_by_xpath('//div[@class="grid grid-cols-12 gap-4"]')
        assert name in grid.get_attribute('innerHTML')

        element = grid.find_element_by_xpath('//*[text()[contains(., "' + name + '")]]')
        driver.execute_script("arguments[0].click();", element)
        assert driver.current_url == BASE_URL + links[name] + '/'
        driver.get(BASE_URL)


def top_bar_testing(driver):

    url = driver.current_url

    edit = driver.find_element_by_xpath('//i[@class="fas fa-cog"]')
    driver.execute_script("arguments[0].click();", edit)
    assert driver.current_url == BASE_URL + 'profile/edit/'

    driver.get(url)

    notices = driver.find_element_by_xpath('//i[@class="far fa-bell"]')
    driver.execute_script("arguments[0].click();", notices)
    assert driver.current_url == BASE_URL + 'notices/'

    links = {'Mój profil': 'profile/', 'Edytuj profil': 'profile/edit/'}

    for link in links.keys():
        user_menu_button = driver.find_element_by_id('profile-img')
        driver.execute_script("arguments[0].click();", user_menu_button)
        user_menu = driver.find_element_by_id('profile-info')
        element = user_menu.find_element_by_xpath('//*[text()[contains(., "' + link + '")]]')
        driver.execute_script("arguments[0].click();", element)
        assert driver.current_url == BASE_URL + links[link]
        driver.get(url)


def sidebar_testing(driver, is_student):

    url = driver.current_url
    links = {'Strona Główna': '', 'Plan zajęć': 'schedule/', 'Kursy': 'courses/', 'Ogłoszenia': 'notices/'}

    if is_student:
        links.update({'Zadania': 'assignments/', 'Oceny': 'marks/'})

    for link in links:
        sidebar_button = driver.find_element_by_id('openbtn')
        driver.execute_script("arguments[0].click();", sidebar_button)
        sidebar = driver.find_element_by_id('mySidebar')

        assert link in sidebar.get_attribute('innerHTML')

        element = sidebar.find_element_by_xpath('//*[text()[contains(., "' + link + '")]]')
        driver.execute_script("arguments[0].click();", element)
        assert driver.current_url == BASE_URL + links[link]
        driver.get(url)

    for link in ['Mój profil', 'Wyloguj']:

        # finding sidebar
        sidebar_button = driver.find_element_by_id('openbtn')
        driver.execute_script("arguments[0].click();", sidebar_button)
        sidebar = driver.find_element_by_id('mySidebar')

        # finding my account button
        my_account_button = sidebar.find_element_by_xpath('//*[text()[contains(., "Moje konto")]]')
        driver.execute_script("arguments[0].click();", my_account_button)
        my_account = sidebar.find_element_by_xpath('//*[text()[contains(., "Moje konto")]]')

        # checking buttons from dropdown menu of my account
        element = my_account.find_element_by_xpath('//*[text()[contains(., "' + link + '")]]')
        driver.execute_script("arguments[0].click();", element)
        if link == 'Mój profil':
            driver.get(url)


def course_screen_testing(driver, is_student):

    driver.get(BASE_URL + 'courses/')

    time.sleep(.5)
    course_button = driver.find_element_by_xpath('//h4[@class="text-lg leading-6 font-medium text-gray-900 '
                                                 'transition-all duration-200 hover:text-gray-600"]') \
        .find_element_by_tag_name('a')
    driver.execute_script("arguments[0].click();", course_button)

    url = driver.current_url

    if is_student:
        links = {'Ogłoszenia': ['notices', 'Ogłoszenia'],
                 'Moje oceny': ['my-marks', 'Moje oceny'],
                 'Dołącz do grupy': ['groups', 'Dołącz do grupy']}
    else:
        links = {'Ogłoszenia': ['notices', 'Ogłoszenia', 'Tytuł ogłoszenia', 'Ogłoszenie', 'Dodaj ogłoszenie'],
                 'Edytuj kurs': ['edit', 'Edytuj', 'Nazwa kursu', 'Opis kursu', 'Zapisz zmiany', 'Dodaj ocene'],
                 'Zarządzaj grupami': ['groups', 'Dołącz do grupy', 'Dodaj grupę'],
                 'Oceny': ['total-marks', 'Wykaz ocen', 'FILTRUJ WYSTAWIONE OCENY', 'Wstaw']}

    for name in links.keys():
        manage_bar = driver.find_element_by_xpath('//div[@class="flex mt-4 mb-4"]')
        assert name in driver.page_source

        element = manage_bar.find_element_by_xpath('//*[text()[contains(., "' + name + '")]]')
        driver.execute_script("arguments[0].click();", element)
        assert driver.current_url == url + links[name][0] + '/'
        for i in range(1, len(links[name])):
            assert links[name][i] in driver.page_source
        driver.get(url)

    # head teacher link testing
    para = driver.find_element_by_xpath('//p[@class="text-sm text-gray-600"]')
    head_teacher = para.find_element_by_tag_name('a')
    driver.execute_script("arguments[0].click();", head_teacher)

    assert (BASE_URL + 'profile/') in driver.current_url
    driver.get(url)

    # teacher link testing
    teachers = driver.find_element_by_xpath('//p[@class="mt-1 text-sm text-gray-600"]')
    teacher = teachers.find_element_by_tag_name('a')
    driver.execute_script("arguments[0].click();", teacher)

    assert (BASE_URL + 'profile/') in driver.current_url
    driver.get(url)

    elements = ['Tematyka:', 'Opis:', 'Materialy i pliki:', 'Link do wydarzenia:']

    if not is_student:
        elements.append('Edytuj')

    lecture_count = len(driver.find_element_by_xpath('//div[@class="max-w-full mx-auto bg-white rounded-lg overflow-hidden shadow-lg"]/div[2]').find_elements_by_tag_name('div'))
    if lecture_count != 0:
        lecture = driver.find_element_by_xpath('//div[@class="px-4 py-4 mx-2"][1]/div[1]/div[2]/h4/a')
        driver.execute_script("arguments[0].click();", lecture)

        assert BASE_URL + 'courses/lecture/' in driver.current_url
        for element in elements:
            assert element in driver.find_element_by_id('dashboard_content').get_attribute('innerHTML')
        driver.get(url)

    labs_count = len(driver.find_element_by_xpath('//div[@class="max-w-full mx-auto bg-white rounded-lg overflow-hidden shadow-lg"]/div[3]').find_elements_by_tag_name('div'))

    if labs_count != 0:
        laboratory = driver.find_element_by_xpath('//div[@class="px-4 py-4 mx-2"][2]/div[1]/div[2]/h4/a')
        driver.execute_script("arguments[0].click();", laboratory)

        laboratory = elements
        laboratory.extend(['Poprzednie laboratorium:', 'Dodaj zadanie'])
        assert BASE_URL + 'courses/laboratory/' in driver.current_url
        for element in laboratory:
            assert element in driver.find_element_by_id('dashboard_content').get_attribute('innerHTML')
        driver.get(url)

    top_bar_testing(driver)
    sidebar_testing(driver, is_student)
