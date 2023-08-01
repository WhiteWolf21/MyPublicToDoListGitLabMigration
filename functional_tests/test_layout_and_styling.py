from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from unittest import skip
import time

class LayoutAndStylingTest(FunctionalTest):

    def test_display_hello_world_and_name(self):
        self.assertIn('User', self.browser.title)  
        self.assertIn('Hello World', self.browser.page_source)
        self.assertIn('User', self.browser.page_source)

        headername = self.browser.find_element_by_css_selector('#header-name')
        self.assertIn('User', headername.text)

        footername = self.browser.find_element_by_css_selector('#footer-name')
        self.assertIn('User', footername.text)

    def test_header_font(self):
        h1_element = self.browser.find_element_by_tag_name('h1')
        h1_font = h1_element.value_of_css_property('font-family')
        h1_weight = h1_element.value_of_css_property('font-weight')

        time.sleep(5)

        self.assertEqual(h1_weight, '700')
        self.assertEqual(h1_font, "Merriweather")

    def test_body_font(self):
        body_elem = self.browser.find_element_by_tag_name('body')
        body_font = body_elem.value_of_css_property('font-family')

        time.sleep(5)
        
        self.assertEqual(body_font, "Muli")
