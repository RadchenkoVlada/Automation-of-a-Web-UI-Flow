from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pytest

TIMEOUT = 10


@pytest.fixture
def driver():
    d = webdriver.Remote("http://browser:4444", options=webdriver.ChromeOptions())
    d.get("https://www.saucedemo.com")
    yield d
    # Close the browser entirely
    d.quit()


def verify_inventory_item_name(driver, expected_data: list):
    """
    Verify the presence of each expected product on the "https://www.saucedemo.com/inventory.html" page
    """
    WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_name")))
    product_titles = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    actual_inventory_items = [ element.text for element in product_titles ]
    assert expected_data == actual_inventory_items


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, TIMEOUT)


class LoginPage(BasePage):
    def login(self):
        # Log in with valid credentials
        username_field = self.wait.until(EC.presence_of_element_located((By.ID, "user-name")))
        password_field = self.wait.until(EC.presence_of_element_located((By.ID, "password")))
        login_button = self.wait.until(EC.presence_of_element_located((By.ID, "login-button")))

        username_field.send_keys("standard_user")  # Use the correct username and password
        password_field.send_keys("secret_sauce")
        login_button.click()


class CartPage(BasePage):
    def checkout(self):
        checkout_button = self.wait.until(EC.presence_of_element_located((By.ID, "checkout")))
        checkout_button.click()

    def verify_added_item(self):
        verify_inventory_item_name(self.driver, ["Sauce Labs Bolt T-Shirt"])


class CheckoutOverview(BasePage):
    def verify(self):
        # Get and verify information on "Checkout: Overview" page
        title_checkout_page = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#header_container > div.header_secondary_container > span"))
        ).text
        assert "Checkout: Overview" in title_checkout_page
        verify_inventory_item_name(self.driver, ["Sauce Labs Bolt T-Shirt"])

        self._verify_element_by_selector(selector="#checkout_summary_container > div > div.cart_list > div.cart_item > div.cart_quantity",
                                 expected="1")
        self._verify_element_by_selector(selector="#checkout_summary_container > div > div.cart_list > div.cart_item > div.cart_item_label > div.item_pricebar > div",
                                 expected="$15.99")

    def _verify_element_by_selector(self, selector, expected):
        el = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        assert el.text == expected

    def finish(self):
        finish_button = self.wait.until(EC.presence_of_element_located((By.ID, "finish")))
        finish_button.click()


class CheckoutInfoPage(BasePage):
    def fill_in_checkout_information(self):
        self.wait.until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("aaaa")
        self.wait.until(EC.presence_of_element_located((By.ID, "last-name"))).send_keys("bbbb")
        self.wait.until(EC.presence_of_element_located((By.ID, "postal-code"))).send_keys("1234")

    def continue_button(self):
        continue_button = self.wait.until(EC.presence_of_element_located((By.ID, "continue")))
        continue_button.click()


class AllProductsPage(BasePage):
    def verify_items(self):
        """
        Verify the presence of each expected product on the "https://www.saucedemo.com/inventory.html" page
        """
        expected_inventory_items = [ "Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt",
                                     "Sauce Labs Fleece Jacket", "Sauce Labs Onesie",
                                     "Test.allTheThings() T-Shirt (Red)" ]
        verify_inventory_item_name(self.driver, expected_inventory_items)

    def add_to_cart(self):
        add_to_cart_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#add-to-cart-sauce-labs-bolt-t-shirt")))
        add_to_cart_button.click()

    def go_to_cart(self):
        shopping_cart_link = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#shopping_cart_container > a")))
        shopping_cart_link.click()


def test_saucedemo(driver):
    # Login page
    login_page = LoginPage(driver)
    login_page.login()

    # All products page
    all_products_page = AllProductsPage(driver)
    all_products_page.verify_items()
    all_products_page.add_to_cart()
    all_products_page.go_to_cart()

    # Cart page
    cart_page = CartPage(driver)
    cart_page.verify_added_item()
    cart_page.checkout()

    # Checkout information page
    checkout_info_page = CheckoutInfoPage(driver)
    checkout_info_page.fill_in_checkout_information()
    checkout_info_page.continue_button()

    # Checkout overview page
    checkout_overview_page = CheckoutOverview(driver)
    checkout_overview_page.verify()
    checkout_overview_page.finish()

    # Verify Сompletion page and label
    thank_you_el = WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, "complete-header")))
    assert thank_you_el.text == "Thank you for your order!"
