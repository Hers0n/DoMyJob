
# Connect to Sofi
def connectSofi(webdriver, user):

    browser = webdriver.Chrome('/Users/Herson/Projects/new/chromedriver')
    browser.get('http://sofi.india.endurance.com/')

    username = browser.find_element_by_name('email')
    username.send_keys(user.usernameStr)

    password = browser.find_element_by_name('password')
    password.send_keys(user.passwordStr)

    nextButton = browser.find_element_by_id('loginBtn')
    nextButton.click()

    # Using Get Phrases button
    # searchTask = browser.find_element_by_id('searchBox')
    # searchTask.send_keys("taskid:" + task)
    # searchTask.send_keys(Keys.ENTER)

    return browser
