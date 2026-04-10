from pydantic import BaseModel

class ClientCreate(BaseModel):
    name: str
    phone: str
    email: str
    status: str
