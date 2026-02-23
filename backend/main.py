from fastapi import FastAPI, HTTPException, BackgroundTasks
from models.schemas import OrderRequest, ScreeningResponse, ComplianceStatus, ComplianceCheckResult
from typing import List
import uuid
from datetime import datetime

app = FastAPI(title="Wipro AI Compliance Screening System")

@app.get("/")
async def root():
    return {"message": "Compliance Screening System API is running"}

@app.post("/screen-order", response_model=ScreeningResponse)
async def screen_order(order: OrderRequest):
    # This will be integrated with the Compliance Agent later
    # For now, return a pending response
    report_id = str(uuid.uuid4())
    
    return ScreeningResponse(
        order_id=order.order_id,
        overall_status=ComplianceStatus.PENDING,
        checks=[],
        report_id=report_id,
        timestamp=datetime.utcnow()
    )

@app.get("/status/{order_id}", response_model=ScreeningResponse)
async def get_screening_status(order_id: str):
    # Mock status retrieval
    return ScreeningResponse(
        order_id=order_id,
        overall_status=ComplianceStatus.PASSED,
        checks=[
            ComplianceCheckResult(
                check_name="Sanction Check",
                status=ComplianceStatus.PASSED,
                details="No matches found in trusted data sources."
            )
        ],
        timestamp=datetime.utcnow()
    )

@app.get("/report/{report_id}")
async def get_report(report_id: str):
    # Placeholder for PDF report retrieval
    return {"report_id": report_id, "url": f"/reports/{report_id}.pdf"}
