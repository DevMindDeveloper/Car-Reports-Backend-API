## imports
import jwt
from fastapi import Request, HTTPException

from app.web import app
from app.config import CarReportCredential

## Decorator to protect routes
def token_required(request: Request):

    token = None

    ## check token
    if 'x-access-token' in request.headers:
        token = request.headers['x-access-token']
    if not token:
        return {'message': 'Token is missing!'}, 401

    ## decode and check the expiration of token
    try:
        data = jwt.decode(token, CarReportCredential.APP_SECRET_KEY, algorithms=["HS256"])
        current_user_id = data['user_id']

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code = 401, detail="Token has expired!")
    except Exception as e:
        raise HTTPException(status_code = 401, detail=f"Token is invalid!, error: {str(e)}")

    ## return to requested process
    return current_user_id
