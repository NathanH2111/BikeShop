# BikeShop
## Summary (Purpose): 

A website for users to purchase both custom and prebuilt bikes. Managers can log in to add and remove the bikes available to users.  

## Goals:  

Have a secure method for users to purchase custom or prebuilt bikes 

Have Authentication secured so that a customer cannot access manager pages 

Have Website be aesthetically pleasing as well as easy to navigate for the end user 

Users can login with their username and password 

Managers can log in, edit, and create products to be sold on the website 

Users can also create accounts using their username and password of choice 

Users should be able to view the products listed on the website 

Once logged in, the user can select and purchase products using multiple types of payment types 

Users can view all previous purchases they made 

Users can buy products with credit, debit, and Bitcoin 

## Functional Requirements: 

### Registration Page 

The registration page will require an email address 

Actual Adress Required 

Password must be between 8 and 20 characters contain upper and lowercase letters and have at least one symbol and will be hashed and salted using Bcrypt before being stored to the DB 

### Login Page 

Users will enter their email and password on the login page and reCAPTCHA verification 

If the user does not exist or the password/username is not entered correctly, the webpage will throw an error to the tune of “Incorrect username or password”  

### Have list of premade bike options stored on a separate table 

Each bike will be able to have custom color (via a hex code rgb Selector) and size (small medium or large) 

Bikes will be divided into two sub sections (Street or Mountain) 

Manager will be able to upload new bikes via a webpage that only users with the administrator role can access 

### Allow a user to custom make a bike based on rim size, # of gears, and mountain or street style. 

All custom bikes will have the option of either 26- or 29-inch rims 

Each bike will have the option of a 9 or 21 speed transmission 

Each bike can be made either with a street style frame or an off-road style frame 

## Non-functional Requirements: 

Secure passwords using Bcrypt to hash and salt the passwords 

Secure any personal data using Symetrics / Asymmetric encryption 

Have authorization so that we only need to have one login page 

Ability to add new bikes without changing the code. 

Internet 

Computer 

Electricity 

Internet Browser 

Keyboard 

Mouse 

Monitor

## Conclusion (includes time frame to finish project): 

The project will be a complete and functioning web application that allows customers to order and build bikes while also allowing admins to list additional bikes to be sold. Project should be completed and operating within four weeks.  