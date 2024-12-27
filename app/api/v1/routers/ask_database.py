from fastapi import APIRouter



router = APIRouter()

@router.get("/ask_database/query")
async def ask_database():
    return {"message": "Hello World"}