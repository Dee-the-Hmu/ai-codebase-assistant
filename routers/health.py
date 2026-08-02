from fastapi import APIRouter

router = APIRouter()

"""
1. You can test that your server is alive.
2. Docker/AWS can use it to check whether your app is working.
3. It is useful in interviews because it shows production thinking.
"""

@router.get("/health")
def health_check():
    return{"status" : "ok"}