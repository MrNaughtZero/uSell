# uSell 

uSell lets you create an online store in minutes, and be selling your product straight away.

uSell aims at providing a service for sellers to sell a single item in bulk who want a more professional online presence, but don't want the bulk and cost of full-scale CMS like SquareSpace or Shopify.

## Coming in V2

* Admin Dashboard
* Custom HTML Emails
* Ticket Support System
* Custom Domains
* Feedback System
* Themes
* Crypto Payments
* PayPal Payments
* New Design Including Mobile

## Setup

To setup uSell, first you will need to clone this repository. Once cloned, you need to set the following environmental variables:

* DB_PATH - the full path to your database. Example: mysql://username:password@host/databasename
* STRIPE_API_KEY - your stripe apy key for express account. Registration will be required on stripe.com
* SITE_URL - your domain url. Example: https://usell.store
* CLOUDINARY_URL - Full URL with API key for CLOUDINARY. Can be accesed from the Cloudinary Console

Next, you need to change your public key for stripe inside app/static/scripts/main.js : Line 278

## How to file a bug

1. Go to our [Issue Tracker](https://github.com/MrNaughtZero/usell/issues) on GitHub
2. Search for existing issues using the search field at the top of the page
3. File a new issue including as many details as much, including how to reproduce the bug.