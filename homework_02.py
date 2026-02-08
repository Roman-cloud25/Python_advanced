from pydantic import BaseModel, Field, EmailStr, model_validator, ValidationError


class Address(BaseModel):
    city: str = Field(..., min_length=2)
    street: str = Field(..., min_length=3)
    house_number: int = Field(..., gt=0)


class User(BaseModel):
    name: str = Field(..., min_length=2, pattern="^[A-Za-z ]+$")
    age: int = Field(..., ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @model_validator(mode='after')
    def check_employed_age(self):
        if self.is_employed and not (18 <= self.age <= 65):
            raise ValueError("Employed user must be between 18 and 65 years old")
        return self


def process_registration(json_input: str):
    try:
        user = User.model_validate_json(json_input)
        return user.model_dump_json(indent=4)
    except ValidationError as e:
        return f"Validation error:\n{e.json(indent=4)}"


valid_json = """{
    "name": "Roman",
    "age": 42,
    "email": "roman.s@gmail.com",
    "is_employed": true,
    "address": {
        "city": "Berlin",
        "street": "Alexanderplatz",
        "house_number": 10
    }
}"""

invalid_age_json = """{
    "name": "Roman",
    "age": 70,
    "email": "roman.s@gmail.com",
    "is_employed": true,
    "address": {
        "city": "Berlin",
        "street": "Alexanderplatz",
        "house_number": 10
    }
}"""

invalid_name_json = """{
    "name": "R1",
    "age": 17,
    "email": "oe@example",
    "is_employed": false,
    "address": {
        "city": "B",
        "street": "St",
        "house_number": -5
    }
}"""

if __name__ == "__main__":
    print("VALID CASE:\n", process_registration(valid_json))
    print("\nINVALID AGE:\n", process_registration(invalid_age_json))
    print("\nINVALID FIELDS:\n", process_registration(invalid_name_json))
