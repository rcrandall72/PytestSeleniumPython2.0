# PytestSeleniumPython

### Description: Runs python selenium tests using pytest. A report is generated in report.html where the results can be reviewed. There is a python file `generate_report.py` that can be run to show a result of the test run.
I.e.
Test Summary:
1 passed, 0 failed, 0 skipped
20.36 seconds

There is a .yml file which will run the tests automatically on a ubuntu environment through Github Actions. The following report is sent to slack.
![slack example](https://github.com/rcrandall72/PytestSeleniumPython2.0/assets/78037488/8c998205-9e6c-44a7-826f-4d9dd70ee92d)


Tests are done on https://www.saucedemo.com/

Two test suites exist:
  - Smoke
    -- Login/Logout & Buy Item
  - Regression
    -- All Test Cases

Can login/logout: 
  - Verifies a user can log in and logout
 
Cannot log in with locked user:
  - Verifies a user cannot log in if their account is locked
  
 Can see login credential errors:
  - Verifies a user sees an error if they are missing their username or password. Also verifies the error message appears if the username/password are incorrect.
  
 Can buy item:
  - Verifies a user can buy an item (add to cart) and finalize their purchase
 
 Can view social media links:
  - Verifies a user can view and route to all social media links (Twitter, Facebook, LinkedIn)
 
 Can sort products:
  - Verifies a user can sort products in the list from A to Z, Z to A, and by Price (high to low & low to high)

# **Installation:**
- Install pip and python3
- Run `pip install -r requirements.txt`
- Run as command line `pytest --browser "chrome"` (or firefox/safari)
