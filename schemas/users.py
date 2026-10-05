from pydantic import BaseModel, Field, model_validator

# creating a schema for how to add user in database.
# the "BaseModel" is a main pydantic class that program can understant it is a SCHEMA not a SIMPLE CLASS.
class userRegister (BaseModel):
    realname: str = Field(..., min_length=2, max_length=50)
    username: str = Field(..., min_length=2, max_length=30)
    password: str = Field(..., min_length=8, max_length=64)
    re_password: str

    # checking repassword so we make sure its not the same.
    @model_validator(mode='after')
    def password_match (self):
        if self.password != self.re_password:
            raise ValueError("passwords not match")
        return self

# here we say how to response data to user. we dont say its id and password.
class userResponse(BaseModel):
    realname: str
    username: str