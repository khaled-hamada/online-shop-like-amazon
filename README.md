to use this application
1. clone the code to your local machine
2. create a virtual env. and install the requirements.txt 
using pip install -r requirements.txt
3. create a .env file in the same directory as settings.py and grab env variables from it, you can follow this link
https://alicecampkin.medium.com/how-to-set-up-environment-variables-in-django-f3c4db78c55f

**run celery on windows**
celery -A myshop worker -l info --pool=solo
------------------------
Online Shop Like Amazon 
-------------------------

This Project will be build upon these 3 chapters of Django 3 by example book ch 7,8,9
More details soon ..

----------------------------------------
**ch7** 
1. create shop categories and products
2. create custom shopping cart and attach it to sessions
3. implement a custom context processor to attach user cart to all req.
4. create orders system to allow users to place orders
5. use celery to run async. tasks with rabbitMQ and flower

----------------------------------
**ch8**
1. Create Payment System
2. Integrate braintree third parity API for handliing payments
3. Create custom admin views and actions
4. create an action to allow stuff users to both a) export orders data to csv file
5. Intgrate weasyPrint lib to generate pdf files from orders data
6. send order details an pdf files to users using emails
-------------------
**ch9**
1. populate db base with fake data using faker lib. so it can help us in building the recommendation system
2. create a copoun system like the one at udemy and apply to to orders from shopping
 cart to creating orders through sessions
3. ...
