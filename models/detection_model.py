from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, Dict, Any


class DetectionBase(BaseModel):
    url: HttpUrl
    model: Optional[str] = None


class DetectionCreate(DetectionBase):
    pass


class DetectionCreateDatabase(DetectionBase):
    status: str = "pending"
    secret: str = None
    created_by: Optional[str] = Field(None, description="User who created the detection")


class DetectionRead(DetectionBase):
    uuid: str
    status: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    created_by: Optional[str] = Field(None, description="User who created the detection")


class DetectionUpdate(BaseModel):
    uuid: str
    secret: str
    status: Optional[str] = None
    model: str
    result: Optional[Dict[str, Any]] = None
