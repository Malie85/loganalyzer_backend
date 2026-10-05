from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from routes.register import register_router

#runnig the FAST API
app = FastAPI()

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