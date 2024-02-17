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
