from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class ComplianceDecision(BaseModel):
    is_violation: bool = Field(description="True if a compliance violation is detected")
    reason: str = Field(description="Detailed explanation for the decision")
    severity: str = Field(description="HIGH, MEDIUM, or LOW")

class ComplianceDataService:
    def __init__(self):
        # Using models/gemini-2.5-flash which is confirmed supported by the provided key
        self.llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", temperature=0)
        self.parser = PydanticOutputParser(pydantic_object=ComplianceDecision)

    async def check_compliance_dynamic(self, order_context: str, check_type: str) -> ComplianceDecision:
        """
        Dynamically checks compliance using Google Gemini reasoning. 
        Falls back to deterministic rules if AI is unavailable.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a senior compliance officer. Analyze the context against international regulations "
                       "(OFAC, EU, UN sanctions, and legal item restrictions). "
                       "Provide a clear decision on whether the order constitutes a violation.\n"
                       "{format_instructions}"),
            ("user", "Check Type: {check_type}\nOrder Context: {order_context}")
        ])

        chain = prompt | self.llm | self.parser
        
        try:
            result = await chain.ainvoke({
                "check_type": check_type,
                "order_context": order_context,
                "format_instructions": self.parser.get_format_instructions()
            })
            return result
        except Exception as e:
            # Fallback logic for demo purposes
            reason = f"Gemini AI Engine temporarily unavailable ({str(e)}). Falling back to deterministic rules: "
            is_violation = False
            
            trigger_words = ["sanction", "sanctionia", "alpha corp", "military", "hardware", "weapon"]
            if any(word in order_context.lower() for word in trigger_words):
                is_violation = True
                reason += "Matched known high-risk keywords in order context."
            else:
                reason += "No immediate high-risk indicators found via fallback rules."
                
            return ComplianceDecision(
                is_violation=is_violation,
                reason=reason,
                severity="HIGH" if is_violation else "LOW"
            )

    async def check_sanctions(self, recipient_name: str, country: str) -> ComplianceDecision:
        context = f"Recipient Name: {recipient_name}, Destination Country: {country}"
        return await self.check_compliance_dynamic(context, "Sanction List Check")

    async def check_item_restriction(self, category: str, item_name: str) -> ComplianceDecision:
        context = f"Item Category: {category}, Item Name: {item_name}"
        return await self.check_compliance_dynamic(context, "Legal & Regulatory Item Restriction Check")

compliance_service = ComplianceDataService()
