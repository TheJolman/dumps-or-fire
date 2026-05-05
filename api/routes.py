from fastapi import APIRouter

router = APIRouter()


@router.get("/popularity")
async def get_things():
    return [{"popularity": 80,}]
