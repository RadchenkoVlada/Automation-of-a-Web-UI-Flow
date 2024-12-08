## Objective
- Use Selenium to automate a simple website flow.

## Tasks

### The Web UI flow
- Website: [https://www.saucedemo.com/](https://www.saucedemo.com/)
- Credentials:
    - Username: `standard_user`
    - Password: `secret_sauce`
- Automation Steps:
    1. Login to the Website
        - Navigate to the Sauce Demo homepage.
        - Locate the username and password input fields and enter information.
        - Click the **Login** button.
    2. Add a product to the Shopping Cart:
        - After logging in, you will see a list of products.
        - Select any product by clicking on its **Add to cart** button.
    3. Go to the Shopping Cart:
        - Click on the shopping cart icon.
        - Verify that the selected product is displayed in the cart.
    4. Proceed to Checkout:
        - Click the **Checkout** button on the cart page.
    5. Fill in the Delivery Information:
        - On the **Checkout: Your Information** page, fill in the required fields:
          - First Name
          - Last Name
          - Postal Code
        - Click the **Continue** button.
    6. Confirm the Order:
        - Review the order details on the Checkout Overview page.
        - Click the **Finish** button to complete the purchase.
    7. Verify the final Confirmation Message:
        - After finishing, you should be redirected to the Checkout Complete page.
        - Verify that the text **"Thank you for your order!"** is displayed.

### Implement the Automation Script
- Use Python (`pytest` and `selenium`) to write your automation script.
- Organize your code with functions or classes for better readability and reusability.
- Use explicit waits (`WebDriverWait`) to handle dynamic content loading.
- Add assertions to validate each critical step.
- Optionally:
    - Modify your script to run on different browsers (Chrome, Firefox, etc.).
    - Use a data file (e.g., CSV or JSON) to input multiple sets of data.
