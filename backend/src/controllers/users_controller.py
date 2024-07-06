import bcrypt
import uuid
from datetime import datetime, timedelta
from src.models.users_model import Users
from src.schemas.user_schema import UserOutput
from core.helpers.response_helper import ResponseData
from core.auth.token import signJWT
from src.models.refresh_token_model import RefreshToken


def create(session, data) -> ResponseData:
    try:
        # Check if the email or phone already exists
        user_check = session.query(Users).filter(
            Users.username == data.username).first()

        if user_check is not None:
            response = ResponseData(
                status_code=400, message="Username must unique.", data=None)
            return response

        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(data.password.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Create the new user record
        current_time = datetime.now()
        user = Users(
            user_id=uuid.uuid4(),
            username=data.username,
            password=hashed_password,
            email=data.email,
            created_at=current_time
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        response = ResponseData(
            status_code=200, message="Registration success.", data=None)
        return response
    except Exception as e:
        session.rollback()
        response = ResponseData(
            status_code=500, message="An error occurred during registration..", data=str(e))
        return response


def signin(session, data) -> ResponseData:
    # Check userdata
    user = session.query(Users).filter(
        Users.username == data.username and Users.password == data.password).first()

    if user is not None:
        # Generate token
        token = signJWT(user.user_id)
        # Check refresh token data
        refresh_token = session.query(RefreshToken).filter(
            RefreshToken.user_id == user.user_id).first()

        # Set current time
        current_time = datetime.now()
        if refresh_token is not None:
            refresh_token.token = token["refresh_token"]
            refresh_token.expired_at = current_time + timedelta(days=7)
        else:
            refresh_token = RefreshToken(
                user_id=user.user_id, token=token["refresh_token"], expired_at=current_time + timedelta(days=7), created_at=current_time)
            session.add(refresh_token)

        session.commit()
        session.refresh(refresh_token)

        response = ResponseData(
            status_code=200, message='Login success', data={"token": token})
        return response

    response = ResponseData(
        status_code=404, message='Your email or password is incorrect')
    return response


def get_all_users(skip, limit, session) -> ResponseData:
    try:
        users = None

        users = session.query(Users).offset(skip).limit(limit).all()

        if users is not None:

            formatted_users = [
                {
                    "user_id": user.user_id,
                    "username": user.username,
                    # Assuming created_at is a datetime field
                    "created_at": user.created_at.isoformat() if user.created_at else None
                }
                for user in users
            ]
            response = ResponseData(
                status_code=200, message="Get user list success.", data=formatted_users)
            return response

        response = ResponseData(
            status_code=404, message="No user data found.", data=None)
        return response
    except Exception as e:
        response = ResponseData(
            status_code=500, message="An error occurred during get all users data process", data=str(e))
        return response
