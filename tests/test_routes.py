from tests.conftest import client

## User tests
def test_create_user(client):
    userData = create_multiple_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    assert response.status_code == 200

def test_create_user_invalid_input(client):
    userData = create_invalid_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    assert response.status_code == 400

def test_create_existing_user(client):
    userData = create_repeat_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    assert response.status_code == 409

def test_get_users(client):
    response = client.get("http://127.0.0.1:5000/Users")
    assert response.status_code == 200

def test_update_user(client, teacher_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {teacher_token}"}
    response = client.put("http://127.0.0.1:5000/User", json = {"name": "lily"}, headers=headers)
    assert response.status_code == 200

def test_invalid_update_user(client, teacher_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {teacher_token}"}
    response = client.put("http://127.0.0.1:5000/User", json = {"pass": "lily"}, headers=headers)
    assert response.status_code == 400

def test_rent_book(client, teacher_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {teacher_token}"}
    bookData = create_book_data()
    response = client.post("http://127.0.0.1:5000/Books", json=bookData, headers=headers)
    response = client.post("http://127.0.0.1:5000/User/Book/1", headers=headers)
    assert response.status_code == 200

def test_missing_rent_book(client, teacher_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {teacher_token}"}
    bookData = create_book_data()
    response = client.post("http://127.0.0.1:5000/Books", json=bookData, headers=headers)
    response = client.post("http://127.0.0.1:5000/User/Book/3", headers=headers)
    assert response.status_code == 404

def test_return_book(client, teacher_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {teacher_token}"}
    bookData = create_book_data()
    response = client.post("http://127.0.0.1:5000/Books", json=bookData, headers=headers)
    response = client.post("http://127.0.0.1:5000/User/Book/1", headers=headers)
    response = client.delete("http://127.0.0.1:5000/User/Book/1", headers=headers)
    assert response.status_code == 200

def test_non_existing_return_book(client, teacher_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {teacher_token}"}
    bookData = create_book_data()
    response = client.post("http://127.0.0.1:5000/Books", json=bookData, headers=headers)
    response = client.delete("http://127.0.0.1:5000/User/Book/1", headers=headers)
    assert response.status_code == 401

def test_missing_return_book(client, teacher_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {teacher_token}"}
    response = client.delete("http://127.0.0.1:5000/User/Book/5", headers=headers)
    assert response.status_code == 404

def test_pass_time(client, teacher_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {teacher_token}"}
    response = client.get("http://127.0.0.1:5000/User?time=10", headers=headers)
    assert response.status_code == 200

def test_invalid_pass_time(client, teacher_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {teacher_token}"}
    response = client.get("http://127.0.0.1:5000/User",  headers=headers)
    assert response.status_code == 400

def test_student_pass_time(client, student_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {student_token}"}
    response = client.get("http://127.0.0.1:5000/User?time=10", headers=headers)
    assert response.status_code == 403

def test_delete_user(client, teacher_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {teacher_token}"}
    response = client.delete("http://127.0.0.1:5000/User", headers=headers)
    assert response.status_code == 200

def test_login(client):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    response = client.post("http://127.0.0.1:5000/login", json={"email": "email@gmail.com", "password": "pass"})
    assert response.status_code == 200

def test_invalid_login(client):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    response = client.post("http://127.0.0.1:5000/login", json={"password": "pass"})
    assert response.status_code == 400

def test_login(client):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    response = client.post("http://127.0.0.1:5000/login", json={"email": "m@gmail.com", "password": "pass"})
    assert response.status_code == 404

def test_payment(client, teacher_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {teacher_token}"}
    bookData = create_book_data()
    response = client.post("http://127.0.0.1:5000/Books", json=bookData, headers=headers)
    response = client.post("http://127.0.0.1:5000/User/Book/1", headers=headers)
    response = client.get("http://127.0.0.1:5000/User?time=10", headers=headers)
    response = client.post("http://127.0.0.1:5000/User", json={"payment": 1}, headers=headers)
    assert response.status_code == 200

def test_invalid_payment(client, teacher_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {teacher_token}"}
    bookData = create_book_data()
    response = client.post("http://127.0.0.1:5000/Books", json=bookData, headers=headers)
    response = client.post("http://127.0.0.1:5000/User/Book/1", headers=headers)
    response = client.get("http://127.0.0.1:5000/User?time=10", headers=headers)
    response = client.post("http://127.0.0.1:5000/User", json={"pay": 1}, headers=headers)
    assert response.status_code == 400


## book tests
def test_create_book(client, teacher_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {teacher_token}"}
    bookData = create_book_data()
    response = client.post("http://127.0.0.1:5000/Books", json=bookData, headers=headers)
    assert response.status_code == 200

def test_invalid_create_book(client, teacher_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {teacher_token}"}
    bookData = create_invalid_book_data()
    response = client.post("http://127.0.0.1:5000/Books", json=bookData, headers=headers)
    assert response.status_code == 400

def test_student_create_book(client, student_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {student_token}"}
    bookData = create_book_data()
    response = client.post("http://127.0.0.1:5000/Books", json=bookData, headers=headers)
    assert response.status_code == 403

def test_get_books(client):
    response = client.get("http://127.0.0.1:5000/Books")
    assert response.status_code == 200

def test_update_book(client, teacher_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {teacher_token}"}
    bookData = create_book_data()
    response = client.post("http://127.0.0.1:5000/Books", json=bookData, headers=headers)
    response = client.put("http://127.0.0.1:5000/Book/1", json = {'name': 'Comedy book', 'category': 'Comedy', 'author': 'Scary author'}, headers=headers)
    assert response.status_code == 200

def test_delete_book(client, teacher_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {teacher_token}"}
    bookData = create_book_data()
    response = client.post("http://127.0.0.1:5000/Books", json=bookData, headers=headers)
    response = client.delete("http://127.0.0.1:5000/Book/1", headers=headers)
    assert response.status_code == 200

def test_missing_delete_book(client, teacher_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {teacher_token}"}
    response = client.delete("http://127.0.0.1:5000/Book/1", headers=headers)
    assert response.status_code == 404

def test_student_delete_book(client, student_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {student_token}"}
    bookData = create_book_data()
    response = client.post("http://127.0.0.1:5000/Books", json=bookData, headers=headers)
    response = client.delete("http://127.0.0.1:5000/Book/1", headers=headers)
    assert response.status_code == 403

def test_update_book(client, teacher_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {teacher_token}"}
    bookData = create_book_data()
    response = client.post("http://127.0.0.1:5000/Books", json=bookData, headers=headers)
    response= client.put("http://127.0.0.1:5000/Book/1", json={"name": "funny book", "category": "not funny", "author": "comedy author"}, headers=headers)
    assert response.status_code == 200

def test_invalid_update_book(client, teacher_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {teacher_token}"}
    bookData = create_book_data()
    response = client.post("http://127.0.0.1:5000/Books", json=bookData, headers=headers)
    response= client.put("http://127.0.0.1:5000/Book/1", json={"category": "not funny", "author": "comedy author"}, headers=headers)
    assert response.status_code == 400

def test_student_update_book(client, student_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {student_token}"}
    bookData = create_book_data()
    response = client.post("http://127.0.0.1:5000/Books", json=bookData, headers=headers)
    response= client.put("http://127.0.0.1:5000/Book/1", json={"name": "funny book", "category": "not funny", "author": "comedy author"}, headers=headers)
    assert response.status_code == 403

def test_missing_update_book(client, teacher_token):
    userData = create_user_data()
    response = client.post("http://127.0.0.1:5000/Users", json=userData)
    headers = {"Authorization" : f"Bearer {teacher_token}"}
    response= client.put("http://127.0.0.1:5000/Book/1", json={"name": "funny book", "category": "not funny", "author": "comedy author"}, headers=headers)
    assert response.status_code == 404

## helper functions
def create_user_data():
    return {"users": [{
        'name': 'Moustafa', 
        'email': 'email@gmail.com', 
        'password': 'pass', 
        'is_teacher': True
    }]}

def create_multiple_user_data():
    return {"users": [{
        'name': 'Moustafa', 
        'email': 'email@gmail.com', 
        'password': 'pass', 
        'is_teacher': True
    },
    {
        'name': 'Yousef', 
        'email': 'joe@gmail.com', 
        'password': 'joe', 
        'is_teacher': False
    }]}

def create_invalid_user_data():
    return {"users": [{
        'password': 'pass', 
        'is_teacher': True
    }]}

def create_repeat_user_data():
    return {"users": [{
        'name': 'Moustafa', 
        'email': 'email@gmail.com', 
        'password': 'pass', 
        'is_teacher': True
    },
    {
       'name': 'Moustafa', 
        'email': 'email@gmail.com', 
        'password': 'pass', 
        'is_teacher': True 
    }]}

def create_book_data():
    return {"books": [{
    'name': 'Scary book', 
    'category': 'Horror', 
    'author': 'Scary author'
    }]}  

def create_multiple_book_data():
    return {"books": [{
    'name': 'Scary book', 
    'category': 'Horror', 
    'author': 'Scary author'
    },
    {
    'name': 'Laugh book', 
    'category': 'Comedy', 
    'author': 'Laugh author'
    }]} 

def create_invalid_book_data():
    return {"books": [{
    'name': 'Scary book', 
    'author': 'Scary author'
    }]}
