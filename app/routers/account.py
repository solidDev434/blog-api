from fastapi import APIRouter, status
from app.schemas.account_schema import SignupDto

router = APIRouter(prefix="/account", tags=["Authentication"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def create_new_user(payload: SignupDto):
    return {"payload": payload}
