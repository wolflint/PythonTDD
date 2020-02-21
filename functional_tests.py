from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Testing the home page of the to-do app
        self.browser.get('http://localhost:8000')

        # Make sure that the title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # The user is invited to enter a to-do item straight away

        # The user types "Buy cheese" into a text box

        # When the user hits enter, the page updates, and now the page lists
        # "1: Buy cheese" as an item in the to-do list

        # There is still a text box inviting her to add another item. She enters
        # "Use cheese to make a sandwich"

        # The page updates again, and now displays both items on the list

        # The user wonders whether the site will remember the list. Then the user
        # sees that the site has generated a unique URL  -- there is some explanatory
        # text to that effect.

        # The user visits that URL - the to-do list is still there.

        # Satisfied, the user goes to sleep
if __name__ == '__main__':
    unittest.main(warnings='ignore')
