from models import UserInDB

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
        "admin": True
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
        "admin": False
    },
    "roberto": {
        "username": "roberto",
        "full_name": "Roberto Garcia",
        "email": "roberto@example.com",
        "hashed_password": "fakehashedsecret3",
        "disabled": False,
        "admin": True
    },
}

def get_user(username: str):
    if username in db:
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)

