import jwt
import os
import boto3
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWKClient
from jwt.exceptions import InvalidTokenError
import ssl
from dotenv import load_dotenv

load_dotenv()

COGNITO_REGION =  os.getenv("COGNITO_REGION")
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
COGNITO_CLIENT_ID =  os.getenv("COGNITO_CLIENT_ID")
COGNITO_JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/jwks.json"
ssl._create_default_https_context = ssl._create_unverified_context

cognito_client = boto3.client("cognito-idp", region_name=COGNITO_REGION)

app = FastAPI()
security = HTTPBearer()

jwks_client = PyJWKClient(COGNITO_JWKS_URL)

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token).key

        decoded_payload = jwt.decode(
            token,
            signing_key,
            algorithms=["RS256"],
            options={"verify_aud": False},
            issuer=f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"
        )
        
        client_id = decoded_payload.get("client_id")
        if client_id != COGNITO_CLIENT_ID:
            raise HTTPException(status_code=401, detail="Invalid audience (client_id)")

        return decoded_payload

    except jwt.exceptions.MissingRequiredClaimError as e:
        raise HTTPException(status_code=400, detail=f"Missing claim in token: {str(e)}")
    except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating token: {str(e)}")

@app.get("/login")
def login_test():
    test_username = "testuser@example.com"
    test_password = "NewTest@1234"

    try:
        response = cognito_client.initiate_auth(
            ClientId=COGNITO_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": test_username,
                "PASSWORD": test_password
            }
        )

        return {
            "id_token": response["AuthenticationResult"]["IdToken"],
            "access_token": response["AuthenticationResult"]["AccessToken"],
            "refresh_token": response["AuthenticationResult"]["RefreshToken"]
        }

    except cognito_client.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except cognito_client.exceptions.UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@app.get("/protected")
def protected_route(user: dict = Depends(verify_jwt_token)):
    return {"message": "You have access!", "user": user}

@app.get("/")
def protected_route():
    return {"message": "Unprotected root "}
