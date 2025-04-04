import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from decouple import config



JWT_KEY = config("JWT_KEY")


class AuthJwtCsrf():
    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret_key = JWT_KEY

    def generate_hashed_pw(self,password) -> str:
        return self.pwd_ctx.hash(password)
    
    def verify_pw(self, plain_pw, hashed_pw) -> bool:
        return self.pwd_ctx.verify(plain_pw, hashed_pw)
    
    def encode_jwt(self, email) -> str:
        payload = {
            "exp": datetime.utcnow() + timedelta(days=1),
            "sub": email,
            "iat": datetime.utcnow()#issued at
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")
    
    def decode_jwt(self, token) -> str:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")