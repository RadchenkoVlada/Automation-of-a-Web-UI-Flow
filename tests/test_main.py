from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import pytest


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
    product_titles = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    actual_inventory_items = [ element.text for element in product_titles ]
    assert expected_data == actual_inventory_items


def test_saucedemo(driver):
    # Log in with valid credentials
    username_field = driver.find_element(By.ID, "user-name")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username_field.send_keys("standard_user")  # Use a valid username
    password_field.send_keys("secret_sauce")  # Use the correct password
    login_button.click()

    # Verify the presence of each expected product on the "https://www.saucedemo.com/inventory.html" page

    expected_inventory_items = [ "Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt",
                                 "Sauce Labs Fleece Jacket", "Sauce Labs Onesie", "Test.allTheThings() T-Shirt (Red)" ]
    verify_inventory_item_name(driver, expected_inventory_items)

    # Add to cart
    add_to_cart_button = driver.find_element(By.CSS_SELECTOR, "#add-to-cart-sauce-labs-bolt-t-shirt")
    add_to_cart_button.click()

    # Go to cart
    shopping_cart_link = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    shopping_cart_link.click()

    # Search for added item
    item = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    assert len(item) == 1
    assert item[0].text == "Sauce Labs Bolt T-Shirt"

    # Go to checkout
    checkout_button = driver.find_element(By.ID, "checkout")
    checkout_button.click()

    # Fill in Checkout Information
    first_name_field = driver.find_element(By.ID, "first-name")
    last_name_field = driver.find_element(By.ID, "last-name")
    postal_code_field = driver.find_element(By.ID, "postal-code")

    first_name_field.send_keys("aaaa")
    last_name_field.send_keys("bbbb")
    postal_code_field.send_keys("1234")

    # Press Continue button on checkout information page
    continue_button = driver.find_element(By.ID, "continue")
    continue_button.click()

    # Get and verify information on "Checkout: Overview" page
    title_checkout_page = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#header_container > div.header_secondary_container > span"))
    ).text
    assert "Checkout: Overview" in title_checkout_page
    verify_inventory_item_name(driver, ["Sauce Labs Bolt T-Shirt"])

    # Press Finish button on checkout overview page
    finish_button = driver.find_element(By.ID, "finish")
    finish_button.click()

    # Verify completion page and label
    thank_you_el = driver.find_element(By.CLASS_NAME, "complete-header")
    assert thank_you_el.text == "Thank you for your order!"
