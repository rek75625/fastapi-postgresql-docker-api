from pydantic import BaseModel, EmailStr,Field

class Students(BaseModel):
    id : str = Field(..., examples=["S001"])
    name : str = Field(...,min_length=2,max_length=50)
    age : int = Field(...,gt=0,le=50)
    course : str = Field(...,max_length=50)
    marks : int = Field(...,ge=2,le=50)
    email : str = EmailStr
    