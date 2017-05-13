## Development


### Assumptions made on given requirements
* The only unique aspect about a business will be its CRN
* Have not added a minimum length validation on Loan reason. Assumption is that loan request will not be accepted without a proper reason.
* No minimum loan duration specified. Assumed one month.
* No maximum loan duration specified. Assumed 2 years.
* We are not recording the date when a loan was requested

### Design choices
* All 8 character CRNs are supported (English + Welsh + Scottish)
* A business only has one owner
* An owner can have several businesses
* International phone numbers are accepted although default field format is 'GB'
* Used money field to store loan amount with default currency set to GBP. No functional reason here, just seemed like a cleaner solution.
* Money field is validated against decimals due to a bug in 'moneyd' package. Default currency is GBP so it still validates correctly.
* Postcode is UK-only and validated using regex. Could validate against a postcode database but its not ideal for businesses set up in newly-erected buildings (might result in loss of customers if a valid postcode is not accepted).

### Not done
* Tests are not data-driven and have hard-coded values.
* Did not use Django REST framework, API is simple and not resource-oriented 

## Overview

Growth Street is building a platform to allow growing businesses to borrow money at affordable rates. Our ability to make the entire process efficient on our web platform will be critical in offering the lowest rates to our customers.

#### The Task

Build a Django app for borrowers to register and request a loan. You will need to collect the following information:

* The borrower's name, email, and telephone number.
* The borrower's business' name, address, registered company number (8 digit number), and business sector (pick from Retail, Professional Services, Food & Drink, or Entertainment).
* The amount the borrower wishes to borrow in GBP (between £10000 and £100000), for how long (number of days), and a reason for the loan (text description).
* This information should be stored in the database via appropriate models, and accessible to an admin in the standard Django Admin tool.

#### Notes

You are encouraged to use 3rd party libraries and the built-in framework tools when it makes sense (for example "django-registration-redux" or "django-allauth" to help handle registering a new user)
While the final product should have an interface via a web browser, there is no need for styles or anything beyond functional HTML

#### Delivery

Fork this repository, make your additions, and then submit a pull request with your submission. If you haven't previously, please contact us with your CV at jobs@growthstreet.co.uk as well.
