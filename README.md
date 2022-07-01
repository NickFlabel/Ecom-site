1.	The goal of the project
The goal of this project is to develop e-com website (hereinafter – Website). The owner of the shop can upload the products on the Website, to manage its cost, view placed orders on said products by the customers. The Web Site provides the means to make payment for the order as well as the system of adding/subtracting customer bonuses. 

2. The description of the project
The system consists of the main functional blocks:
1)	Registration, authentication and authorization;
2)	CRUD functions;
3)	Placing order functions;
4)	Order payment functions;
5)	Bonus addition/subtraction functions;
6)	Order tracking function.

2.1.	Types of users
Website allows for four types of users:
1)	The owner of the Website;
2)	The employee;
3)	Registered customer;
4)	Unregistered customer.

2.2.	Registration
Registration depends on the type of user:
The registration of the owner is executed during the installation of the Website. Name and password are mandatory fields.
The owner of the Website performs the registration of the employee in the administration interface of Website. Name and password are mandatory fields.
Registration of the customer can be performed in two different ways. The first way is registration by employee by entering the new customer’s phone number, email and password. The second way is registration by the customer himself using the Website interface. 

2.3.	Authentication of the different types of users
Authentication is performed using the Web Site interface. For authentication the user should enter his login and password.

2.4.	Website functions for customer
Registered customer have access to the following functions:
1) Access to the personal web page, which contains the following information: the number of bonuses, order history, bonuses history, ability to change personal info;
2) Access to the cart, ability to add and subtract the products to and from the cart;
3) Ability to place the order on the Website with the possibility of payment.

2.5.	 Website functions for employees.
The employees have access to the following functions:
1) Order tracking
2) Changing the status of the order (fulfillment of the order)
3) Adding and subtracting bonuses by entering the phone number of the customer

2.6.	 Website functions for the owner of the Website
The owner of the web site has access to the same functions as the employee as well as:
1) The ability to add, view, update and delete the employee profiles
2) The ability to add, view, update and delete the products placed on the Web Site

2.7.	Main Page Functions
The main page of the Web Site serves simultaneously as the list of all products registered in the database. Each segment represents one product and allow the user to add this product to the cart, open the details page.

2.8.	 Details page functions
Details page allows viewing the product and all additional data concerning this product as well as allowing for the same functions the user has on the main page. 

2.9.	Cart Page Functions
The cart allows deleting/subtracting/adding the number of products in the cart as well as opening the checkout page.

2.10.	Employee page functions
The users of “employee” or “owner” type can only access to the employee page. The page is divided to three blocks. First block allows tracking opened orders, which are connected to the shop of this employee. The second block allows adding and subtracting bonuses from the customer’s account by entering the phone number. The third block allows for displaying the order info.

3. Technology stack:
For the development of the Web Site the usage of the following technologies are proposed:
•	Backend:
	Python3;
  Django REST Framework;
	Django Web Framework;
	PostgreSQL (on deploy).
•	Frontend:
	Bootstratp;
  JavaScript;
  Rest.js

The link to the deployed prototype: http://flaviusbelisarius.pythonanywhere.com/

Login/Password to see full functionality as a worker of the cafe:
Login: TestUserWorker
Password: tEsTuSeR1
