from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.body_limit import RequestBodyLimitMiddleware

from routes.register import register_router
from routes.auth import Login_Router
from routes.me import me
from routes.logout import logout_router
from routes.upload import upload_router
from db.database import engine
from models import users as users_model

# what is this?????? search later...............
MAX_FILE_SIZE = 50 * 1024 * 1024
MAX_REQUEST_SIZE = MAX_FILE_SIZE + 1 * 1024 * 1024
#runnig the FAST API
app = FastAPI(
    middleware=[
        Middleware(
            RequestBodyLimitMiddleware,
            max_body_size=MAX_REQUEST_SIZE,
        )
    ]
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ...........................
# creating tables in database
users_model.Base.metadata.create_all(bind=engine)


# here we make an error handler function
# we do not want to response the whole things to user beacause it includes password or id.
# so we use this to send just important stuffs to make a pretty error.
# we said to fastapi : if an exeption from requestvalodation happened, handel it by the below function
@app.exception_handler(RequestValidationError)
# in fisrt parameter, fastapi give the information of sended request to function.
# in secound parameter, give the errors information to function
async def validation_error_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = []

    # adding just loc and msg of each errors to a dictionery
    for error in exc.errors():
        errors.append({
            "field": error["loc"],
            "message": error["msg"]
        })

    # then response it
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "details": errors
        }
    )

# including ROUTES
app.include_router(register_router)
app.include_router(Login_Router)
app.include_router(me)
app.include_router(logout_router)
app.include_router(upload_router)