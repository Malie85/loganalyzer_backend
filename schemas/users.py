from pydantic import BaseModel, Field, model_validator, field_validator

# creating a schema for how to add user in database.
# the "BaseModel" is a main pydantic class that program can understant it is a SCHEMA not a SIMPLE CLASS.
class userRegister (BaseModel):

    # in real name just english characters and space is allowed.
    # we use Field for length validator because it send correct error massege itself. but in checking character it can not send correct error message so we cant use pattern and markdown. we use field validator.
    # we give the stuffs to field_validator and it check it by the below function and reise the correct error.
    # if you want to know how this errors handled , check the main.py there i wrote the error handler.
    realname: str = Field(..., min_length=2, max_length=50)
    @field_validator("realname")
    @classmethod
    def validate_realname(cls, value):
        # all() means if all is true, true but if there is just one false, return false --> all(true, true, true) = true      and        all(true, false, true) = false
        if not all(c.isascii() and c.isalpha() or c == " " for c in value):
            raise ValueError(
                "Name must contain English letters only."
            )
        return value
    
    username: str = Field(..., min_length=2, max_length=30)
    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        if not all(c.isascii() and c != " " for c in value):
            raise ValueError("Username must contain English and special characters without space.")
        return value
    
    password: str = Field(..., min_length=8, max_length=64)
    re_password: str
    @model_validator(mode='after')
    def password_match (self):
        if self.password != self.re_password:
            raise ValueError("passwords not match")
        return self

# here we say how to response data to user. we dont say its id and password.
class userResponse(BaseModel):
    realname: str
    username: str


class userLogin(BaseModel):
    username: str = Field(...,min_length=2, max_length=30)
    password: str = Field(...,min_length=8, max_length=64)

class userLoginResponse(BaseModel):
    message: str
    user: userResponse

