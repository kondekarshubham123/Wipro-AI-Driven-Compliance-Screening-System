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
    name: str = Field(..., description="Name of the item")
    category: str = Field(..., description="Category for compliance checking (e.g., Electronics, Military Hardware)")
    quantity: int = Field(..., ge=1, description="Quantity of items")
    price: float = Field(..., gt=0, description="Price per unit")

class OrderShipment(BaseModel):
    recipient_name: str = Field(..., description="Full name of the recipient")
    recipient_address: str = Field(..., description="Shipping address")
    recipient_country: str = Field(..., description="Destination country for sanction checks")

class OrderRequest(BaseModel):
    order_id: str = Field(..., description="Unique order identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Order placement timestamp")
    customer_id: str = Field(..., description="Identifier for the customer")
    items: List[OrderItem] = Field(..., description="List of items in the order")
    shipment: OrderShipment = Field(..., description="Shipping information")

class ComplianceCheckResult(BaseModel):
    check_name: str = Field(..., description="Name of the compliance check performed")
    status: ComplianceStatus = Field(..., description="Result status of the specific check")
    details: str = Field(..., description="Detailed findings or reasoning for the status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Time the check was completed")

class ScreeningResponse(BaseModel):
    order_id: str = Field(..., description="Unique order identifier")
    overall_status: ComplianceStatus = Field(..., description="Final compliance decision for the order")
    checks: List[ComplianceCheckResult] = Field(..., description="Breakdown of individual compliance checks")
    report_id: Optional[str] = Field(None, description="UUID for the generated audit report")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Time the screening was concluded")

class AuditReport(BaseModel):
    report_id: str = Field(..., description="Unique identifier for the report")
    order_id: str = Field(..., description="Related order identifier")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Time the report was generated")
    content: str = Field(..., description="Content of the report in HTML/Markdown format")
    pdf_url: Optional[str] = Field(None, description="Path or URL to the generated PDF")
