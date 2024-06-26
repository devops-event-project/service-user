from typing import  Dict, Optional
from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi import Request,status,HTTPException
from fastapi.security.utils import get_authorization_scheme_param

"""
This class, OAuth2PasswordBearerWithCookie, inherits from FastAPI's OAuth2 and 
overrides it to retrieve the access token from a cookie offering an authentication mechanism.
"""


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("access_token")  #changed to accept access token from httpOnly Cookie

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
              raise HTTPException(status_code=302, detail="Not authorized", headers = {"Location": "/user/login"} )
            else:
                return None
        return param