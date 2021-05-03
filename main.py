import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import getpass


def facebook_login():
    email_or_number = input('Enter email or phone number: ')
    # password = input('Enter your password: ')
    password = getpass.getpass('Enter your password: ')

    # email or phone number for login.
    login_email_or_number = driver.find_element_by_id('email')
    login_email_or_number.send_keys(email_or_number)

    # password for that email - phone number
    login_password = driver.find_element_by_id('pass')
    login_password.send_keys(password)

    # pressing on login button
    login_button = driver.find_element_by_xpath('//button[@name="login"]')
    login_button.click()
    print('Processing...')
    time.sleep(10)

    current_url = driver.current_url

    if current_url.endswith('?next'):
        print('Login successful')
        ask_otp()
    else:
        print('fail to login\nInvalid email/phoneNumber or password\nTry again')
        facebook_login()


def ask_otp():
    print('We have send you an otp to desired phone number')
    resend_otp = driver.find_element_by_xpath("//a[@role='button']")
    resend_otp.click()

    click_resend_otp = driver.find_element_by_xpath("//a[contains(text(),'Text')]")
    click_resend_otp.click()

    otp = int(input('Enter opt: '))
    close_icon = driver.find_element_by_xpath("//a[@title='Close']")
    close_icon.click()

    otp_input = driver.find_element_by_xpath("//input[@name='approvals_code']")
    otp_input.send_keys(otp)
    otp_input.send_keys(Keys.ENTER)

    otp_failed = False
    while not otp_failed:
        try:
            driver.find_element_by_xpath("//span[@data-xui-error]")
            present = True
        except NoSuchElementException:
            present = False

        if not present:
            print('Valid otp')
            otp_failed = True
            save_password()
        else:
            print('Invalid otp')
            otp = int(input('Enter opt: '))
            otp_input = driver.find_element_by_xpath("//input[@name='approvals_code']")
            otp_input.send_keys(otp)
            otp_input.send_keys(Keys.ENTER)


def save_password():
    save_pass()
    print('Completed')

    url = driver.current_url
    if url.endswith('?next'):
        login_to_facebook()


def login_to_facebook():
    review_recent_login_continue = driver.find_element_by_xpath("//button[@value='Continue']")
    review_recent_login_continue.click()

    sure_to_login = input('Are you sure to login[Y/N]: ')
    if sure_to_login.lower() == 'y':
        this_was_me = driver.find_element_by_xpath("//button[@value='This Was Me']")
        this_was_me.click()
        print('Few steps to go.')
    else:
        not_me = driver.find_element_by_xpath('//button[@value="This Wasn\'t Me"]')
        not_me.click()

    save_pass()

    print('You have successfully logged in to your facebook account')


def save_pass():
    save_or_not = input('Do you want to save to password [Y/N]: ')
    if save_or_not.lower() == 'y':
        save_xpath = driver.find_element_by_xpath("//input[@value='save_device']")
        save_xpath.click()
        print('You password has been saved in browser')
    else:
        dont_save_xpath = driver.find_element_by_xpath("//input[@value='dont_save']")
        dont_save_xpath.click()
        print("We haven't save your password in browser")

    continue_button = driver.find_element_by_xpath("//button[@value='Continue']")
    continue_button.click()


if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path='C:\\Users\\acer\\chromedriver.exe')
    driver.get('https://facebook.com')

    facebook_login()
