from pydantic import BaseModel, EmailStr,Field,field_validator,computed_field



class Students(BaseModel):
    id : str = Field(..., examples=["S001"])
    name : str = Field(...,min_length=2,max_length=50)
    age : int = Field(...,gt=0,le=50)
    course : str = Field(...,max_length=50)
    marks : int = Field(...,ge=2,le=50)
    email : EmailStr = Field(...)

    @field_validator("name")
    @classmethod
    def nameChecker(cls,value):
        if not value.replace(" ","").isalpha():
            raise ValueError("Name must be contain alphabets and spaces only")
        
        return value.title()
    
    @computed_field
    @property
    def grade(self)->str:
        if self.marks >= 90:
            return "A+"
        elif self.marks >= 80:
            return "A"
        elif self.marks >= 70:
            return "B"
        elif self.marks >= 60:
            return "C"
        else:
            return "F"


class StudentUpdate(BaseModel):
    name : str| None = Field(None,min_length=2,max_length=50)
    age : int| None = Field(None,gt=0,le=50)
    course : str| None = Field(None,max_length=50)
    marks : int| None = Field(None,ge=2,le=100)
    email : EmailStr| None = None
    
    @field_validator("name")
    @classmethod
    def nameChecker(cls,value):
        if value is not None and not value.replace(" ","").isalpha():
            raise ValueError("Name must be contain alphabets and spaces only")
        
        return value.title() if value is not None else value