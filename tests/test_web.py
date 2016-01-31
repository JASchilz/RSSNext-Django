"""
Acceptance web tests for the RSSNext project
"""

from time import sleep
from random import randint

from selenium import webdriver

from django.contrib.sites.models import Site
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from allauth.socialaccount.models import SocialApp


class TestWeb(StaticLiveServerTestCase):
    """
    Acceptance web tests for the RSSNext project
    """

    feeds = [
        "http://rss.cnn.com/rss/cnn_topstories.rss",
        "http://rss.cnn.com/rss/cnn_us.rss"
        ]

    def setUp(self):  # pylint: disable=invalid-name
        """
        Runs before each test.

        :return None:
        """
        app = SocialApp.objects.create(provider='facebook',
                                       name='facebook',
                                       client_id='app123id',
                                       key='facebook',
                                       secret='dummy')
        app.sites.add(Site.objects.get_current())
        app.save()

        self.username = "u" + str(randint(100000, 999999)) + "@example.com"
        self.password = str(randint(100000, 999999))

        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

        super(TestWeb, self).setUp()

    def tearDown(self):  # pylint: disable=invalid-name
        """
        Runs after each test.

        :return None:
        """
        self.browser.close()

        super(TestWeb, self).tearDown()

    def url(self, path):
        """
        Appends a given url path onto the test server's host/port number.

        :param path:
        :return None:
        """
        return self.live_server_url + path

    @property
    def page_body_text(self):
        """
        Retrieves the body text of the current page.

        :return None:
        """
        return self.browser.find_element_by_css_selector("body").text

    def do_create_user(self):
        """
        Creates the user, supposing the home page is loaded.

        :return None:
        """

        self.browser.find_element_by_id("id_email").send_keys(self.username)
        self.browser.find_element_by_id("id_password1").send_keys(self.password)
        self.browser.find_element_by_id("id_password2").send_keys(self.password)

        self.browser.find_element_by_css_selector("#sign-up button[type='submit']").click()

    def do_login_user(self):
        """
        Logs the user in, supposing the home page is loaded.

        :return None:
        """

        self.browser.find_element_by_id("id_login").send_keys(self.username)
        self.browser.find_element_by_id("id_password").send_keys(self.password)

        self.browser.find_element_by_css_selector("#login button[type='submit']").click()

    def do_logout_user(self):
        """
        Logs the user out, supposing the account home is loaded.

        :return None:
        """

        self.browser.find_element_by_css_selector("li.dropdown.account").click()
        self.browser.find_element_by_css_selector("li.dropdown.account li.logout").click()

    def assert_at_login_page(self):
        """
        Asserts that the login page is currently loaded.

        :return None:
        """

        self.assertIn('RSSNext - One Click Takes You To Your Next Unread Item', self.browser.title)

    def assert_at_account_home(self):
        """
        Asserts that the account home is currently loaded.

        :return None:
        """
        self.assertIn('RSSNext Home', self.browser.title)

    def test_get_home(self):
        """
        By loading the path '', a visitor should arrive at the home/login page.

        :return None:
        """

        self.browser.get(self.url(''))
        self.assert_at_login_page()

    def test_create_user(self):
        """
        From the home page, a visitor shall be able to create an account and be
        delivered to the account home.

        :return None:
        """

        self.browser.get(self.url(''))
        self.assert_at_login_page()

        self.do_create_user()

        self.assert_at_account_home()

    def test_create_user_logout_login(self):
        """
        A visitor shall be able to create an account, log out, and then log
        in with the same credentials, and be delivered to the account home.

        :return None:
        """

        self.test_get_home()

        self.do_create_user()

        self.assert_at_account_home()

        self.do_logout_user()

        self.assert_at_login_page()

        self.do_login_user()

        self.assert_at_account_home()

    def test_add_feeds(self):
        """
        A logged in user shall be able to add feeds, and see them added to their
        control panel.

        :return None:
        """

        self.test_create_user()

        self.assert_at_account_home()

        feed_adder = self.browser.find_element_by_css_selector("#add-feed input[type=text]")
        feed_adder_submit = self.browser.find_element_by_css_selector("#add-feed button")

        feed_adder.send_keys(self.feeds[0])
        feed_adder_submit.click()

        sleep(1)

        feed_adder.send_keys(self.feeds[1])
        feed_adder_submit.click()

        sleep(4)

        self.assertIn('CNN.com - Top Stories', self.page_body_text)
        self.assertIn('CNN.com - U.S.', self.page_body_text)

        # After refreshing, the feeds should still be present in the user's
        # control panel.
        self.browser.refresh()

        self.assertIn('CNN.com - Top Stories', self.page_body_text)
        self.assertIn('CNN.com - U.S.', self.page_body_text)

    def test_remove_feed(self):
        """
        A logged in user shall be able to remove feeds that they have added to
        their control panel.

        :return None:
        """

        self.test_create_user()

        self.assert_at_account_home()

        feed_adder = self.browser.find_element_by_css_selector("#add-feed input[type=text]")
        feed_adder_submit = self.browser.find_element_by_css_selector("#add-feed button")

        feed_adder.send_keys(self.feeds[0])
        feed_adder_submit.click()

        sleep(1)

        feed_adder.send_keys(self.feeds[1])
        feed_adder_submit.click()

        sleep(4)

        self.assertIn('CNN.com - Top Stories', self.page_body_text)
        self.assertIn('CNN.com - U.S.', self.page_body_text)

        self.browser.\
            find_element_by_xpath("//td[contains(text(), 'CNN.com - Top Stories')]").\
            find_element_by_xpath('..').\
            find_element_by_partial_link_text('Delete').\
            click()

        sleep(1)

        self.assertNotIn('CNN.com - Top Stories', self.page_body_text)
        self.assertIn('CNN.com - U.S.', self.page_body_text)

    def test_create_users_with_same_login(self):
        """
        When two visitors attempt to create a user with the same login, the
        second shall be presented with an error.

        :return None:
        """

        self.browser.get(self.url(''))
        self.assert_at_login_page()

        self.do_create_user()

        self.assertIn('RSSNext Home', self.browser.title)

        self.do_logout_user()

        self.assert_at_login_page()

        self.do_create_user()

        self.assert_at_login_page()
        self.assertIn('A user is already registered with this e-mail address', self.page_body_text)

    def test_create_user_password_mismatch(self):
        """
        A visitor who creates a user must correctly repeat their choice of
        password.

        :return None:
        """

        self.browser.get(self.url(''))
        self.assert_at_login_page()

        self.browser.find_element_by_id("id_email").send_keys(self.username)
        self.browser.find_element_by_id("id_password1").send_keys(self.password)
        self.browser.find_element_by_id("id_password2").send_keys(str(randint(1000000, 9999999)))

        self.browser.find_element_by_css_selector("#sign-up button[type='submit']").click()

        self.assertIn('You must type the same password each time', self.page_body_text)
