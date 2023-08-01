from .base import FunctionalTest


class MyListsTest(FunctionalTest):

    def test_not_logged_in_users_cant_add_list(self):
        self.client.logout()
        self.browser.get(self.live_server_url)

        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn("What's next?", navbar.text)

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'edith@example.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # Edith is a logged in user
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)