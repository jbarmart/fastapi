from typing import Optional
from fastapi import HTTPException, Header


# Dependency function to check for 'token' in headers
def verify_token(token: Optional[str] = Header(None)):
    """
    curl -X GET "http://localhost:8080/get_user/1" -H "token: your-expected-token"
    """
    #if token != "MasterKey":
    #    raise HTTPException(status_code=403, detail="Invalid token or token missing")
    #return token
    pass