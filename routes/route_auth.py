import bcrypt
from fastapi import APIRouter, Body, HTTPException, status

from db.mongo_connection import MongoDB
from models.user import User, UserLogin, UserRegister

router = APIRouter()


@router.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new User",
)
def signup(user: UserRegister = Body(...)):
    """
    Signup

    Registers a user in the app

    Parameters:
    - Request body:
        - user: UserRegister

    Returns:
    - User
    """
    db = MongoDB.get_instance()
    users_collection = db.users

    existing_user = users_collection.find_one({"email": user.email})

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already in use",
        )

    user_dict = user.dict()
    user_dict["user_id"] = str(user_dict["user_id"])
    user_dict["birth_date"] = str(user_dict["birth_date"])

    user_dict["password"] = bcrypt.hashpw(
        user_dict["password"].encode("utf-8"),
        bcrypt.gensalt(),
    )

    users_collection.insert_one(user_dict)
    return user_dict


@router.post(
    path="/login",
    response_model=User,
    summary="Login a User",
)
def login():
    pass
