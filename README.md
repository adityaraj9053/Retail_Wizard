Retail Wizard: A Comprehensive Retail Shop Point Of Sale Management System

Description
Retail Wizard is a retail shop management system designed for small businesses. It provides features such as product catalogue management, shopping cart functionality, transaction processing, and detailed reporting to streamline business operations.

Prerequisites
1. Python 3.6 or higher installed on your system.
2. Required Python libraries:
   pandas
   openpyxl
   qrcode
   Pillow
   fpdf
   matplotlib
   bcrypt
   pyautogui
3. SQLite database file (`grocery.db`) should be present in the project directory.
4. Standard Libraries (included with Python, no installation needed):
   json
   sqlite3
   tkinter
   os
   sys
   subprocess
   time
   unittest

Installation
1. Download the project files to your local machine.
2. Ensure all required Python libraries are installed. Use the following command to install these libraries: 
   pip install pandas openpyxl qrcode Pillow fpdf matplotlib bcrypt pyautogui


How to Run the Application
1. Navigate to the project directory in your terminal.
2. Run the SignUp.py application file.
3. The sign up window of the Retail Wizard application will open and just register to our product.
4. Login through your credentials.
5. Main window will appear click product catalogue button and just load the excel file : Updated_Product_Catalogue and select the desired products and tap Send to Main Window.
6. Just add customer's name and phone number on top left corner of the main window and tap Checkout & Pay button.
7. Now just tap the Pay button and you can select the desired payment method cash or upi.
8. You can even cancel payment at any time in between.

How to Access Reports
1. Click the Reports button in the main window.
2. Select the desired report (e.g., Transaction Report, Stock Report).
3. The selected report will open in a new window.

-----------------------------------------------------------------------------------------

Features
1.Product Catalogue:
Manage product details such as category, brand, price, and stock availability.
Load product data from an Excel file.

2.Shopping Cart:
Add and delete products in the cart.
Calculate total price.

3.Transaction Processing:
Record customer details and transaction data.
Export invoice data to a JSON file.

4.Reports:
Access detailed reports such as:
  Profit & Loss Report
  Stock Report
  Sales Report
  Transaction Report

5.Checkout and Payment: 
Complete transactions and proceed to payment.

-----------------------------------------------------------------------------------------

Troubleshooting:
If the application fails to open, ensure all dependencies are installed and the `grocery.db` file is present in the project directory.
For database-related errors, verify that the required tables (`grocery`, `transactions`, `selected_product`) exist in the database.


