from typing import List, Dict
import json

class ComplianceDataService:
    def __init__(self):
        # Mocking trusted compliance data (Sanction Lists, etc.)
        self.sanctioned_entities = ["Alpha Corp", "Global Syndicate", "Dark Trade"]
        self.sanctioned_countries = ["Sanctionia", "Outlands"]
        self.restricted_categories = ["Military Hardware", "Dual-Use Chemicals"]

    async def check_sanctions(self, entity_name: str) -> bool:
        return any(sanctioned in entity_name for sanctioned in self.sanctioned_entities)

    async def check_country(self, country: str) -> bool:
        return country in self.sanctioned_countries

    async def check_item_restriction(self, category: str) -> bool:
        return category in self.restricted_categories

compliance_service = ComplianceDataService()
