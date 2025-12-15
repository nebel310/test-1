import asyncio
import json
import xml.etree.ElementTree as ET
from typing import Dict, Any

class LegacyXMLService:
    async def get_data_xml(self) -> str:
        await asyncio.sleep(0.3)
        return """
        <user>
            <id>123</id>
            <name>John Doe</name>
            <email>john@example.com</email>
            <age>30</age>
            <active>true</active>
        </user>
        """
    
    async def save_data_xml(self, xml_data: str) -> str:
        await asyncio.sleep(0.2)
        return f"Данные сохранены: {xml_data}"

class ModernJSONService:
    async def get_data_json(self) -> Dict[str, Any]:
        pass
    
    async def save_data_json(self, json_data: Dict[str, Any]) -> str:
        pass

class XMLToJSONAdapter(ModernJSONService):
    def __init__(self, legacy_service: LegacyXMLService):
        self._legacy_service = legacy_service
    
    async def get_data_json(self) -> Dict[str, Any]:
        xml_data = await self._legacy_service.get_data_xml()
        root = ET.fromstring(xml_data)
        result = {}
        
        for child in root:
            text = child.text
            if text.lower() == 'true':
                result[child.tag] = True
            elif text.lower() == 'false':
                result[child.tag] = False
            elif text.isdigit():
                result[child.tag] = int(text)
            else:
                result[child.tag] = text
        
        return result
    
    async def save_data_json(self, json_data: Dict[str, Any]) -> str:
        root = ET.Element("user")
        
        for key, value in json_data.items():
            child = ET.SubElement(root, key)
            child.text = str(value)
        
        xml_data = ET.tostring(root, encoding='unicode')
        return await self._legacy_service.save_data_xml(xml_data)

class ModernClient:
    def __init__(self, service: ModernJSONService):
        self._service = service
    
    async def process_user_data(self) -> Dict[str, Any]:
        data = await self._service.get_data_json()
        data["processed"] = True
        data["timestamp"] = "2024-01-01T12:00:00"
        
        save_result = await self._service.save_data_json(data)
        
        return {
            "data": data,
            "save_result": save_result
        }

class ThirdPartyAPIAdapter:
    async def fetch_weather(self, city: str) -> Dict[str, Any]:
        await asyncio.sleep(0.4)
        
        if city == "Moscow":
            return {
                "город": "Москва",
                "температура": 20,
                "влажность": 65,
                "описание": "ясно"
            }
        elif city == "London":
            return {
                "city": "London",
                "temp": 15,
                "humidity": 80,
                "description": "cloudy"
            }
        else:
            return {
                "location": city,
                "temperature": 25,
                "conditions": "sunny"
            }
    
    async def get_unified_weather(self, city: str) -> Dict[str, Any]:
        raw_data = await self.fetch_weather(city)
        
        unified_data = {
            "city": raw_data.get("город") or raw_data.get("city") or raw_data.get("location"),
            "temperature": raw_data.get("температура") or raw_data.get("temp") or raw_data.get("temperature"),
            "humidity": raw_data.get("влажность") or raw_data.get("humidity"),
            "description": raw_data.get("описание") or raw_data.get("description") or raw_data.get("conditions"),
            "units": {
                "temperature": "C",
                "humidity": "%"
            }
        }
        
        return unified_data