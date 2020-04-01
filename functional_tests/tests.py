from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import os

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_for_one_user(self):
        # Testing the home page of the to-do app
        self.browser.get(self.live_server_url)

        # Make sure that the title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # The user is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # The user types "Buy cheese" into a text box
        # When the user hits enter, the page updates, and now the page lists
        # "1: Buy cheese" as an item in the to-do list
        inputbox.send_keys('Buy cheese')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy cheese')

        # There is still a text box inviting the user to add another item.
        # The user enters "Buy ham"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy ham')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again and shows both items on the list
        self.wait_for_row_in_list_table('2: Buy ham')
        self.wait_for_row_in_list_table('1: Buy cheese')

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.check_for_row_in_list_table('1: Buy cheese')
        self.check_for_row_in_list_table('2: Buy ham')

        # There is still a text box inviting her to add another item. She enters
        # "Use cheese to make a sandwich"
        self.fail('Finish the test!')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # User starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy tennis racket')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy tennis racket')

        # The user notices that the list has a unique URL.
        user1_list_url = self.browser.current_url
        self.assertRegex(user1_list_url, '/lists/.+')

        # User2 visits the site.
        ## New browser session is opened to make sure that
        ## User1 information isn't coming through from cookies
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # User2 visits the homepage, there is no sign of User1's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy cheese', page_text)
        self.assertNotIn('Buy ham', page_text)
        self.assertNotIn('Buy tennis racket', page_text)

        # User2 starts a new list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # User 2 gets a unique URL
        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, '/lists/.+')
        self.assertNotEqual(user2_list_url, user1_list_url)

        # Again, there is not trace of User1's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy tennis racket', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, both users go to sleep ZzzzZzzzzZzzz


    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise # -*- coding: utf-8 -*-
                time.sleep(0.5)
        # The page updates again, and now displays both items on the list

        # The user wonders whether the site will remember the list. Then the user
        # sees that the site has generated a unique URL  -- there is some explanatory
        # text to that effect.

        # The user visits that URL - the to-do list is still there.

        # Satisfied, the user goes to sleep
# if __name__ == '__main__':
#     unittest.main(warnings='ignore')
    def test_layout_and_styling(self):
        # User goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # The user notices that the input box is nicesly centred
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # The user starts a new list and sees that the input is nicely
        # centred there too.
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
        inputbox.location['x'] + inputbox.size['width'] / 2,
        512,
        delta=10
        )


