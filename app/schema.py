from pydantic import BaseModel

class CertificateData(BaseModel):
    name: str
    position: str
    sport: str
    date: str