from pydantic import BaseModel

class CertificateData(BaseModel):
    name:       str   # Recipient full name
    position:   str   # e.g. "1st", "2nd Runner Up"
    event:      str   # e.g. "100m Sprint", "Basketball"
    start_date: str   # e.g. "15 Jan 2025"
    end_date:   str   # e.g. "20 Jan 2025"