from typing import Optional
from prometheus_client import Counter
from fastapi import HTTPException, Header, Request
from app.src.services.metrics import AUTH_REQUEST

# Dependency function to check for 'token' in headers
def verify_token(request: Request, token: Optional[str] = Header(None)):
    """
    curl -X GET "http://localhost:8080/get_user/1" -H "token: your-expected-token"
    """
    if token == "MasterKey":
        user = "Jacob Barasch"  # Replace with actual user identification logic
        request.state.user = user  # Store user in request state
        AUTH_REQUEST.labels(user=user, route=request.scope['path']).inc()  # Increment the metric with the user and route labels
        return user
    else:
        request.state.user = 'failure'
        AUTH_REQUEST.labels(user='failure', route=request.scope['path']).inc()
        raise HTTPException(status_code=403, detail="Invalid token or token missing")