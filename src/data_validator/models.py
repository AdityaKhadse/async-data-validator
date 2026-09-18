from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRecordInput(BaseModel):
    id: str = Field(..., min_length=1, description="Unique primary key for the record")
    name: str = Field(..., min_length=2, description="Full name of user")
    email: EmailStr = Field(..., description="Valid standard RFC email address")
    age: int = Field(..., ge=18, le=120, description="Age must be between 18 and 120")
    signup_date: datetime = Field(..., description="ISO 8601 formatted datetime")
    balance: float = Field(default=0.0, ge=0.0, description="Account balance cannot be negative")

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Name cannot consist solely of whitespace.")
        return cleaned.title()


class ValidationSummary(BaseModel):
    total_processed: int = 0
    successful_records: list[UserRecordInput] = []
    failed_records: list[dict[str, str]] = []
    duration_seconds: float = 0.0