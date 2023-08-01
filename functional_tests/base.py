from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from unittest import skip
import time

MAX_WAIT = 20
User = get_user_model()

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        # options = Options()
        # options.headless = True
        # self.browser = webdriver.Firefox(options=options)
        # self.browser.implicitly_wait(3)
        chrome_options = Options()
        chrome_options.add_argument('--dns-prefetch-disable')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('disable-gpu')
        self.browser = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
        self.browser.implicitly_wait(3)

        self.browser.get(self.live_server_url)

    def tearDown(self):  
        self.browser.quit()
    
    def wait(fn):
        def modified_fn(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if(time.time() - start_time > MAX_WAIT):
                        raise e
                    time.sleep(0.5)
        return modified_fn
    
    @wait
    def wait_for(self, fn):
        return fn()

    @wait
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')  
        self.assertIn(row_text, [row.text for row in rows])

    def check_comment_regarding_amount_of_list(self, comment_tag):
        comment = self.browser.find_element_by_tag_name('comment')
        self.assertIn(comment_tag, comment.get_attribute('cat'))
    
    def input_todo_item(self, todo_text):
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(todo_text)
        inputbox.send_keys(Keys.ENTER)
    
    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)
    
    def create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk 
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key, 
            path='/',
        ))