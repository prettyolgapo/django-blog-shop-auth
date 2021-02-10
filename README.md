# django-blog-shop-auth
Django apps 3 in 1. Blog + Shop + Authentication

Django's project that is a company website. It contains 3 apps which are samples of Blog, Shop and Authentication

        Blog: List of posts, New post, Edit post, Search post.
        Shop: List of Products, Cart, Checkout, Search products
        Authentication:
                Django authentication framework: Login and Logout
                Example LoginForm

        Models are stored in the database PostreSQL.


Author: Olga Kondratenko aka Prettyolgapo 

Licence: BSD

Installation

	Get the code directory, create and activate virtual environment
		Get the code
			git clone https://github.com/prettyolgapo/django-blog-shop-auth.git
		Create your own virtual environment
                	cd django-blog-shop-auth
			python3 -m venv venv
			source venv/bin/activate
		1.Open an IDE or text editor you love or get familiar with, e.g. PyCharm, VisualStudio Code, SublimeTex, etc. 
		2.Open folder to import the directory django-blog-shop-auth into PyCharm
		3.Then open PyCharm terminal
		4.Your virtual environment is aldeady activated. If not: it’s time to activate virtual environtment in PyCharm 
			cd django-blog-shop-auth
			env/scripts/activate
		5. Install Django
			pip install django
		6.Generate a new secret key with, e.g. Djecrety
              
	Setting up a database server
		1.Open pgAdmin4
		2.Click server, and choose PostgreSQL version
		3.Then create our database. It's name is mysitedb
	       	4.Change user and password to your own in file settings.py 
		5.In PyCharm terminal install module for PostgreSQL database and migrate tables
	        	pip install psycopg2
	        	py manage.py makemigrations <app_label> (<app_label> are shop, blog)
	        	py manage.py migrate
		6.Add some data in tables using Django Admin
		7.Create a new superuser
			py manage.py createsuperuser
                
        Run project 
	        py manage.py runserver


Bugs

        Please Report if You find bug.


Tests

        Tests are written for the Shop and Blog apps. Tests located in the files tests.py.

        Run the tests:

                py manage.py test blog
                py manage.py test shop
