import time
import uuid  # Added for generating UUID in example
from typing import Dict
import jwt
from decouple import config

# Retrieve secret and algorithm from environment variables
JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


def token_response(access_token: str, refresh_token: str) -> Dict[str, str]:
    """
    Returns a dictionary with the access token and refresh token.
    """
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


def signJWT(user_id: uuid.UUID) -> Dict[str, str]:
    """
    Signs JWTs for the given user_id (UUID) with an access token 
    that expires in 10 minutes and a refresh token that expires in 7 days.
    """
    access_token_payload = {
        "user_id": str(user_id),  # Convert UUID to string
        "expires": time.time() + 600  # 10 minutes
    }
    print(f"Access Token Payload: {access_token_payload}")
    print(f"JWT_SECRET: {JWT_SECRET}")
    print(f"JWT_ALGORITHM: {JWT_ALGORITHM}")

    try:
        access_token = jwt.encode(
            access_token_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        refresh_token_payload = {
            "user_id": str(user_id),  # Convert UUID to string
            "expires": time.time() + 604800  # 7 days
        }
        refresh_token = jwt.encode(
            refresh_token_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    except Exception as e:
        print(f"Error encoding JWT: {e}")
        raise e

    return token_response(access_token, refresh_token)


def decodeJWT(token: str) -> dict:
    """
    Decodes a JWT. Returns the decoded token if it is valid and not expired.
    Returns None if the token is invalid or expired.
    """
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if decoded_token["expires"] >= time.time():
            return decoded_token
        else:
            return None
    except jwt.ExpiredSignatureError:
        return {"error": "Expired token"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
