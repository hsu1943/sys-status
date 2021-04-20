from fastapi import APIRouter
from utils import response
from data_handler import *

router = APIRouter()


@router.get("/", tags=["status"])
async def index(gap: int = 900, limit: int = 10):
    data = get_data(gap, limit)
    return response.resp_200(data=data)
