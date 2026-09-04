from fastapi import APIRouter

router = APIRouter(tags=["System"])


@router.get("/checksystem")
async def check_my_system():
    return {"message":"System checked Sucessfully"}
