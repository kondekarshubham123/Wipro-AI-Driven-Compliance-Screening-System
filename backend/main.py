from fastapi import FastAPI, HTTPException, BackgroundTasks
from models.schemas import OrderRequest, ScreeningResponse, ComplianceStatus, ComplianceCheckResult
from typing import List
import uuid
from datetime import datetime

from agents.compliance_agent import compliance_agent
from utils.report_generator import report_generator

app = FastAPI(title="Wipro AI Compliance Screening System")

@app.get("/")
async def root():
    return {"message": "Compliance Screening System API is running"}

@app.post("/screen-order", response_model=ScreeningResponse)
async def screen_order(order: OrderRequest, background_tasks: BackgroundTasks):
    # Invoke the agentic workflow
    initial_state = {
        "order": order,
        "results": [],
        "overall_status": ComplianceStatus.PENDING,
        "summary": ""
    }
    
    final_output = await compliance_agent.ainvoke(initial_state)
    
    report_id = str(uuid.uuid4())
    
    response = ScreeningResponse(
        order_id=order.order_id,
        overall_status=final_output["overall_status"],
        checks=final_output["results"],
        report_id=report_id,
        timestamp=datetime.utcnow()
    )
    
    # Generate report in the background
    background_tasks.add_task(report_generator.generate_pdf, response)
    
    return response

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
