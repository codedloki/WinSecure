from pydantic import BaseModel


class Host(BaseModel):
    name: str
    ip_address: str
    mac_address: str
