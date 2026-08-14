from flask import Blueprint

health_router = Blueprint(
    "health",
    __name__,
    url_prefix="/health"
)

@health_router.get("")
def health():
    return {"status" : "ok"}, 200