from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, END
from models.schemas import OrderRequest, ComplianceStatus, ComplianceCheckResult, ScreeningResponse
from services.compliance_data import compliance_service
import operator
from datetime import datetime

class AgentState(TypedDict):
    order: OrderRequest
    results: Annotated[List[ComplianceCheckResult], operator.add]
    overall_status: ComplianceStatus
    summary: str

async def sanction_check_node(state: AgentState):
    order = state["order"]
    is_sanctioned = await compliance_service.check_sanctions(order.shipment.recipient_name)
    is_sanctioned_country = await compliance_service.check_country(order.shipment.recipient_country)
    
    status = ComplianceStatus.PASSED
    details = "No sanctions detected."
    
    if is_sanctioned or is_sanctioned_country:
        status = ComplianceStatus.VIOLATION_DETECTED
        details = "Recipient or destination country is on a sanction list."
        
    result = ComplianceCheckResult(
        check_name="Sanction Check",
        status=status,
        details=details,
        timestamp=datetime.utcnow()
    )
    return {"results": [result]}

async def legal_check_node(state: AgentState):
    order = state["order"]
    has_restricted_items = False
    details = "All items cleared legal check."
    
    for item in order.items:
        if await compliance_service.check_item_restriction(item.category):
            has_restricted_items = True
            details = f"Restricted item category detected: {item.category}"
            break
            
    status = ComplianceStatus.VIOLATION_DETECTED if has_restricted_items else ComplianceStatus.PASSED
    
    result = ComplianceCheckResult(
        check_name="Legal & Regulatory Check",
        status=status,
        details=details,
        timestamp=datetime.utcnow()
    )
    return {"results": [result]}

async def finalize_node(state: AgentState):
    results = state["results"]
    overall_status = ComplianceStatus.PASSED
    
    for res in results:
        if res.status == ComplianceStatus.VIOLATION_DETECTED:
            overall_status = ComplianceStatus.VIOLATION_DETECTED
            break
        elif res.status == ComplianceStatus.FLAGGED_FOR_REVIEW:
            overall_status = ComplianceStatus.FLAGGED_FOR_REVIEW
            
    return {"overall_status": overall_status}

# Define the graph
workflow = StateGraph(AgentState)

workflow.add_node("sanction_check", sanction_check_node)
workflow.add_node("legal_check", legal_check_node)
workflow.add_node("finalize", finalize_node)

workflow.set_entry_point("sanction_check")
workflow.add_edge("sanction_check", "legal_check")
workflow.add_edge("legal_check", "finalize")
workflow.add_edge("finalize", END)

compliance_agent = workflow.compile()
