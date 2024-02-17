# Library Manager

## Objective
This project simulates the function of issuing books to users from a library. The objective of this project is to keep track of the books in the library, and to keep track of the users that issue and return these books and what they are owed in late return fees. The project was made using flask and sqlalchemy for the api design, jwt tokens are used to authenticate the api calls, bcrypt to hash encrypt the users' passwords and pytest for unit testing. The project uses sqlite, but that can be easily changed from the configuration in the __init__.py file in the app directory. The project can create a user, a user can be a teacher with permission to do certain actions, or a student. The late fee rate also is different depending on the status of the user. Both students and teachers can create an account, login, change their name, rent or return a book, make any payments if they have late fees and logout. Teachers can also create books, change details of books, delete books and can use a function that simulates the passing of time. Finally the users have a one-to-many relationship with books.

## Dependencies
All the libraries that were used for this project are listed in the requirements.txt file.

## Unit test instructions
The project uses pytest for its unit tests. When in root directory use the `pytest` command to run the unit tests. There are 30 unit tests that test each api call for its success and failure responses.

## API Calls

### Create a user

Creates and returns a new users

* **URL** <br />
/Users

* **Method** <br />
POST

* **URL Params** <br />
None

* **Data Params** <br />
**Required:** <br />
```json
{
    "users":[
        {
            "name": "Moustafa",
            "email": "email@gmail.com",
            "password": "pass",
            "is_teacher": true
        },
        {
            "name": "Lily",
            "email": "lil@gmail.com",
            "password": "lil",
            "is_teacher": false
        }
    ]
}
```

* **Success Response** <br />
**Code:** 200 <br />
**Content:** `[
    {
        "email": "email@gmail.com",
        "is_teacher": true,
        "name": "Moustafa",
        "password": "pass"
    },
    {
        "email": "lil@gmail.com",
        "is_teacher": false,
        "name": "Lily",
        "password": "lil"
    }
]`

* **Error Response** <br />
  * **Code:** 400 <br />
  **Content:** `{"message": "Invalid input"}` <br />
  OR
  * **Code:** 409 <br />
  **Content:** `{"message": "Email already exists"}`
    
* **Sample Call:** <br />
```json
curl --location 'http://127.0.0.1:5000/Users' \
--header 'Content-Type: application/json' \
--data-raw '{
    "users":[
        {
            "name": "Moustafa",
            "email": "email@gmail.com",
            "password": "pass",
            "is_teacher": true
        },
        {
            "name": "Lily",
            "email": "lil@gmail.com",
            "password": "lil",
            "is_teacher": false
        }
    ]
}'
```

### Login as a user

Validates and creates a JWT token that can be used for protected api calls

* **URL** <br />
/login

* **Method** <br />
POST

* **URL Params** <br />
None

* **Data Params** <br />
**Required:** <br />
```json
{
  "email": "email@gmail.com",
  "password": "pass"
}
```

* **Success Response** <br />
**Code:** 200 <br />
**Content:** `{'message': f"Hello {name}, you are logged in!", 'token': {access_token}}`

* **Error Response**
  * **Code:** 400 <br />
  **Content:** `{"message": "Invalid password"}` or  `{"message": "Invalid input"}` <br />
  OR
  * **Code:** 404 <br />
  **Content:** `{"message": "User was not found"}`
    
* **Sample Call:** <br />
```json
curl --location 'http://127.0.0.1:5000/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "email@gmail.com",
    "password": "pass"
}'
```

### Change user information

A user changes their information

* **URL** <br />
/User

* **Method** <br />
PUT

* **URL Params** <br />
None

* **Data Params** <br />
```json
{
  "name": "Lily"
}
```

* **Success Response** <br />
**Code:** 200 <br />
**Content:** `{
    "balance": 0.0,
    "email": "email@gmail.com",
    "is teacher": true,
    "name": "Lily"
}`

* **Error Response**
  * **Code:** 400 <br />
  **Content:** `{"message": "Invalid input"}` <br />
    
* **Sample Call:** <br />
```json
curl --location --request PUT 'http://127.0.0.1:5000/User' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwODE3ODI1MSwianRpIjoiNDMyNTgzODAtNDJkYS00YTdlLTg3MjktMzI5MzhiMTk2MTJhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImVtYWlsQGdtYWlsLmNvbSIsIm5iZiI6MTcwODE3ODI1MSwiY3NyZiI6ImUzYTVmYzRiLTQ1NzItNGI0Yi05ZWUyLWY1OTA0YTA1OTA3OSIsImV4cCI6MTcwODE3ODg1MX0.FiYSL2zd4hU3BuiX6RFy5v3P4ZjJkE0QdWvlx39Dju4' \
--data '{
  "name": "Lily"
}
'
```

### Delete user

A user deletes their account

* **URL** <br />
/User

* **Method** <br />
DELETE

* **URL Params** <br />
None

* **Data Params** <br />
None

* **Success Response** <br />
**Code:** 200 <br />
**Content:** `{'message': 'User deleted'}`

* **Error Response**
  * **Code:** 400 <br />
  **Content:** `{"message": "Invalid input"}` <br />
  OR
  * **Code:** 404 <br />
  **Content:** `{"message": "User was not found"}`
    
* **Sample Call:** <br />
```json
curl --location --request DELETE 'http://127.0.0.1:5000/User' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwODE4MDQwMywianRpIjoiZGEwYWM0NjUtODU3MS00NTAxLTk3N2QtZGIwNTQ2NGY4Yzg5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImxpbEBnbWFpbC5jb20iLCJuYmYiOjE3MDgxODA0MDMsImNzcmYiOiI0YjNmYTUwNi1hNWQzLTRjODYtYjM3Ny0xMjAwZjFlZWI3YWMiLCJleHAiOjE3MDgxODEwMDN9.aIRnQBEMuGdVAplgCKVwSn00ohBtu2Ew1AgQF6a-Tsg'
```

### Logout

A user logs out of their account

* **URL** <br />
/logout

* **Method** <br />
DELETE

* **URL Params** <br />
None

* **Data Params** <br />
None

* **Success Response** <br />
**Code:** 200 <br />
**Content:** `{'message': 'logged out'}`

* **Sample Call:** <br />
```json
curl --location --request DELETE 'http://127.0.0.1:5000/logout' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwODE4MDQ2NCwianRpIjoiNWM0YzFjZjgtZTdmZi00ZGM5LTlhY2QtNDg0M2RhYmM3ZDhiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImVtYWlsQGdtYWlsLmNvbSIsIm5iZiI6MTcwODE4MDQ2NCwiY3NyZiI6ImIwN2RiZWIwLWM1ZDYtNDNiNC05MTJhLTU3MDkzZTllODJiNyIsImV4cCI6MTcwODE4MTA2NH0.O-wL2bcZ5MwbYDsgG9pjf9IRVDrwdjjDJitwa0P29VY'
```

### User rents a book

A user rents/issues a book from the library

* **URL** <br />
/User/Book/<int: bookId>

* **Method** <br />
POST

* **URL Params** <br />
None

* **Data Params** <br />
None

* **Success Response** <br />
**Code:** 200 <br />
**Content:** `{
    "author": "Laugh author",
    "category": "Comedy",
    "days rented": 0,
    "name": "Laugh book",
    "userEmail": "email@gmail.com"
}`

* **Error Response**
  * **Code:** 401 <br />
  **Content:** `{"message": "Book already issued to another user"}` <br />
  OR
  * **Code:** 404 <br />
  **Content:** `{"message": "book was not found"}`
    
* **Sample Call:** <br />
```json
curl --location --request POST 'http://127.0.0.1:5000/User/Book/2' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwODE4MDY2OCwianRpIjoiZTQ4ZjkzM2QtNWNlMy00MjdmLThlZmYtYWEyZTVlYmNmZmIzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImVtYWlsQGdtYWlsLmNvbSIsIm5iZiI6MTcwODE4MDY2OCwiY3NyZiI6IjMzZTAzYTYyLWY1MWEtNDM2Zi1iNzViLWQ2YmNlZjVlZjIyYSIsImV4cCI6MTcwODE4MTI2OH0.pppQoL2wa2k8SorK6usiWYNJ2VyVJA9BByc1TOWcJp8'
```

### User returns a book

A user returns a book to the library

* **URL** <br />
/User/Book/<int: bookId>

* **Method** <br />
POST

* **URL Params** <br />
None

* **Data Params** <br />
None

* **Success Response** <br />
**Code:** 200 <br />
**Content:** `{"message": "book returned"}`

* **Error Response**
  * **Code:** 401 <br />
  **Content:** `{"message": "Book already not issued to the user"}` <br />
  OR
  * **Code:** 404 <br />
  **Content:** `{"message": "book was not found"}`
    
* **Sample Call:** <br />
```json
curl --location --request DELETE 'http://127.0.0.1:5000/User/Book/2' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwODE4MDY2OCwianRpIjoiZTQ4ZjkzM2QtNWNlMy00MjdmLThlZmYtYWEyZTVlYmNmZmIzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImVtYWlsQGdtYWlsLmNvbSIsIm5iZiI6MTcwODE4MDY2OCwiY3NyZiI6IjMzZTAzYTYyLWY1MWEtNDM2Zi1iNzViLWQ2YmNlZjVlZjIyYSIsImV4cCI6MTcwODE4MTI2OH0.pppQoL2wa2k8SorK6usiWYNJ2VyVJA9BByc1TOWcJp8'
```

### User makes payment

A user makes a payment for their late fees

* **URL** <br />
/User

* **Method** <br />
POST

* **URL Params** <br />
None

* **Data Params** <br />
**Required:** `{"payment": 3.0}`

* **Success Response** <br />
**Code:** 200 <br />
**Content:** `{"message": "Payment completed, your new balance is 7.0"}`

* **Error Response**
  * **Code:** 400 <br />
  **Content:** `{"message": "Invalid input"}` <br />
    
* **Sample Call:** <br />
```json
curl --location 'http://127.0.0.1:5000/User' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwODE4MDY2OCwianRpIjoiZTQ4ZjkzM2QtNWNlMy00MjdmLThlZmYtYWEyZTVlYmNmZmIzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImVtYWlsQGdtYWlsLmNvbSIsIm5iZiI6MTcwODE4MDY2OCwiY3NyZiI6IjMzZTAzYTYyLWY1MWEtNDM2Zi1iNzViLWQ2YmNlZjVlZjIyYSIsImV4cCI6MTcwODE4MTI2OH0.pppQoL2wa2k8SorK6usiWYNJ2VyVJA9BByc1TOWcJp8' \
--data '{
    "payment": 3.0
}'
```

### Teacher passes time

A teacher passes time for the library system

* **URL** <br />
/User

* **Method** <br />
GET

* **URL Params** <br />
**Required:** `time=[number of days to pass]`

* **Data Params** <br />
None

* **Success Response** <br />
**Code:** 200 <br />
**Content:** `{"message": "Time passed by 10"}`

* **Error Response**
  * **Code:** 400 <br />
  **Content:** `{"message": "Invalid input"}` <br />
    
* **Sample Call:** <br />
```json
curl --location 'http://127.0.0.1:5000/User?time=10' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwODE4MDY2OCwianRpIjoiZTQ4ZjkzM2QtNWNlMy00MjdmLThlZmYtYWEyZTVlYmNmZmIzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImVtYWlsQGdtYWlsLmNvbSIsIm5iZiI6MTcwODE4MDY2OCwiY3NyZiI6IjMzZTAzYTYyLWY1MWEtNDM2Zi1iNzViLWQ2YmNlZjVlZjIyYSIsImV4cCI6MTcwODE4MTI2OH0.pppQoL2wa2k8SorK6usiWYNJ2VyVJA9BByc1TOWcJp8'
```

### Teacher creates books

A teacher creates books to be added to the library

* **URL** <br />
/Books

* **Method** <br />
POST

* **URL Params** <br />
None

* **Data Params** <br />
**Required:** `{
    "books":[
        {
            "name": "Scary book",
            "category": "Horror",
            "author": "Scary author"
        },
        {
            "name": "Laugh book",
            "category": "Comedy",
            "author": "Laugh author"
        }
    ]
}`

* **Success Response** <br />
**Code:** 200 <br />
**Content:** `[
    {
        "author": "Scary author",
        "bookId": 1,
        "category": "Horror",
        "days rented": 0,
        "name": "Scary book",
        "user": null
    },
    {
        "author": "Laugh author",
        "bookId": 2,
        "category": "Comedy",
        "days rented": 0,
        "name": "Laugh book",
        "user": null
    }
]`

* **Error Response**
  * **Code:** 400 <br />
  **Content:** `{"message": "Invalid input"}` <br />
  OR
  **Code:** 403 <br />
  **Content:** `{"message": "You do not have permission for this action"}` <br />
    
* **Sample Call:** <br />
```json
curl --location 'http://127.0.0.1:5000/Books' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwODE4MDY2OCwianRpIjoiZTQ4ZjkzM2QtNWNlMy00MjdmLThlZmYtYWEyZTVlYmNmZmIzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImVtYWlsQGdtYWlsLmNvbSIsIm5iZiI6MTcwODE4MDY2OCwiY3NyZiI6IjMzZTAzYTYyLWY1MWEtNDM2Zi1iNzViLWQ2YmNlZjVlZjIyYSIsImV4cCI6MTcwODE4MTI2OH0.pppQoL2wa2k8SorK6usiWYNJ2VyVJA9BByc1TOWcJp8' \
--data '{
    "books":[
        {
            "name": "Scary book",
            "category": "Horror",
            "author": "Scary author"
        },
        {
            "name": "Laugh book",
            "category": "Comedy",
            "author": "Laugh author"
        }
    ]
}'
```

### Teacher deletes a book

A teacher deletes a book from the library

* **URL** <br />
/User/Book/<int: bookId>

* **Method** <br />
DELETE

* **URL Params** <br />
None

* **Data Params** <br />
None

* **Success Response** <br />
**Code:** 200 <br />
**Content:** `{"message": "Book deleted"}`

* **Error Response**
  * **Code:** 401 <br />
  **Content:** `{"message": "Book already not issued to the user"}` <br />
  OR
  * **Code:** 404 <br />
  **Content:** `{"message": "book was not found"}` <br />
  OR
  * **Code:** 403 <br />
  **Content:** `{"message": "you do not have permission for this action"}` <br />
    
* **Sample Call:** <br />
```json
curl --location --request DELETE 'http://127.0.0.1:5000/Book/1' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwODE4MTc1NCwianRpIjoiODA3Zjc4OGMtYTAzZC00MGJlLWJkNTItOWU1ZjY5YWQ1Njk5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImVtYWlsQGdtYWlsLmNvbSIsIm5iZiI6MTcwODE4MTc1NCwiY3NyZiI6IjM3MDIzYTRmLTg1NGYtNDE1MC04MDdhLTlhZThjODYzY2NkZiIsImV4cCI6MTcwODE4MjM1NH0.ewpF8pOs5vqHXDY9PzU7aflP0yeeLuMC3mxx9p-LLTI'
```

### Teacher changes a book

A teacher changes book details

* **URL** <br />
/User/Book/<int: bookId>

* **Method** <br />
PUT

* **URL Params** <br />
None

* **Data Params** <br />
None

* **Success Response** <br />
**Code:** 200 <br />
**Content:** `{
    "author": "Comedy author",
    "bookId": 2,
    "category": "Comedy",
    "days rented": 20,
    "name": "Comedy book"
}`

* **Error Response**
  * **Code:** 401 <br />
  **Content:** `{"message": "Book already not issued to the user"}` <br />
  OR
  * **Code:** 404 <br />
  **Content:** `{"message": "book was not found"}` <br />
  OR
  * **Code:** 403 <br />
  **Content:** `{"message": "you do not have permission for this action"}` <br />
    
* **Sample Call:** <br />
```json
curl --location --request PUT 'http://127.0.0.1:5000/Book/2' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwODE4MTc1NCwianRpIjoiODA3Zjc4OGMtYTAzZC00MGJlLWJkNTItOWU1ZjY5YWQ1Njk5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImVtYWlsQGdtYWlsLmNvbSIsIm5iZiI6MTcwODE4MTc1NCwiY3NyZiI6IjM3MDIzYTRmLTg1NGYtNDE1MC04MDdhLTlhZThjODYzY2NkZiIsImV4cCI6MTcwODE4MjM1NH0.ewpF8pOs5vqHXDY9PzU7aflP0yeeLuMC3mxx9p-LLTI' \
--data '{
    "author": "Comedy author",
    "category": "Comedy",
    "name": "Comedy book"
}'
```
