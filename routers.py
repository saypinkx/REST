from fastapi import APIRouter

router = APIRouter(prefix='/s')


@router.get('/s')
def hello():
    return 'hello'
