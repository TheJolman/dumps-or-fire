from fastapi import APIRouter

router = APIRouter()

@router.get("/things")
async def get_things():
    return [{"id": 1, "name": "thing1"}]
