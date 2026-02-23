from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime

class ComplianceStatus(str, Enum):
    PENDING = "PENDING"
    PASSED = "PASSED"
    VIOLATION_DETECTED = "VIOLATION_DETECTED"
    FLAGGED_FOR_REVIEW = "FLAGGED_FOR_REVIEW"

class OrderItem(BaseModel):
    name: str
    category: str
    quantity: int
    price: float

class OrderShipment(BaseModel):
    recipient_name: str
    recipient_address: str
    recipient_country: str

class OrderRequest(BaseModel):
    order_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    customer_id: str
    items: List[OrderItem]
    shipment: OrderShipment

class ComplianceCheckResult(BaseModel):
    check_name: str
    status: ComplianceStatus
    details: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ScreeningResponse(BaseModel):
    order_id: str
    overall_status: ComplianceStatus
    checks: List[ComplianceCheckResult]
    report_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class AuditReport(BaseModel):
    report_id: str
    order_id: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    content: str  # Markdown or HTML content
    pdf_url: Optional[str] = None
