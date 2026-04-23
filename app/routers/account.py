from fastapi import APIRouter, status

router = APIRouter(prefix="/account", tags=["Authentication"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def create_new_user():
    return {"message": "User successfully created"}
