from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Testing the home page of the to-do app
        self.browser.get('http://localhost:8000')

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
        inputbox.send_keys('Buy cheese')
        # When the user hits enter, the page updates, and now the page lists
        # "1: Buy cheese" as an item in the to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # There is still a text box inviting the user to add another item.
        # The user enters "Buy ham"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy ham')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.check_for_row_in_list_table('1: Buy cheese')
        self.check_for_row_in_list_table('2: Buy ham')

        # There is still a text box inviting her to add another item. She enters
        # "Use cheese to make a sandwich"
        self.fail('Finish the test!')

        # The page updates again, and now displays both items on the list

        # The user wonders whether the site will remember the list. Then the user
        # sees that the site has generated a unique URL  -- there is some explanatory
        # text to that effect.

        # The user visits that URL - the to-do list is still there.

        # Satisfied, the user goes to sleep
if __name__ == '__main__':
    unittest.main(warnings='ignore')
