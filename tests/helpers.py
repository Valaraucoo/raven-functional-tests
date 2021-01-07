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


def dashboard_top_bar_testing(driver):

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
