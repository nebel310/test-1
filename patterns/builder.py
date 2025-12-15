import asyncio
from typing import List, Optional
from abc import ABC, abstractmethod

class HTTPRequest:
    def __init__(self):
        self.url: str = ""
        self.method: str = "GET"
        self.headers: dict = {}
        self.params: dict = {}
        self.data: Optional[dict] = None
        self.timeout: int = 30
        self.verify_ssl: bool = True
    
    async def execute(self) -> dict:
        """Асинхронное выполнение HTTP запроса (имитация)"""
        print(f"Выполняем {self.method} запрос к {self.url}")
        await asyncio.sleep(0.3)
        
        return {
            "url": self.url,
            "method": self.method,
            "status_code": 200,
            "headers": self.headers,
            "params": self.params,
            "data": self.data,
            "timeout": self.timeout,
            "verify_ssl": self.verify_ssl,
            "response": {
                "success": True,
                "message": "Запрос выполнен успешно"
            }
        }
    
    def __str__(self):
        return f"HTTPRequest(url={self.url}, method={self.method}, headers={self.headers})"

class HTTPRequestBuilder(ABC):
    def __init__(self):
        self.request = HTTPRequest()
    
    @abstractmethod
    def set_url(self, url: str):
        pass
    
    @abstractmethod
    def set_method(self, method: str):
        pass
    
    def add_header(self, key: str, value: str):
        self.request.headers[key] = value
        return self
    
    def add_param(self, key: str, value: str):
        self.request.params[key] = value
        return self
    
    def set_data(self, data: dict):
        self.request.data = data
        return self
    
    def set_timeout(self, timeout: int):
        self.request.timeout = timeout
        return self
    
    def disable_ssl_verification(self):
        self.request.verify_ssl = False
        return self
    
    def build(self) -> HTTPRequest:
        return self.request

class JSONAPIRequestBuilder(HTTPRequestBuilder):
    def set_url(self, url: str):
        self.request.url = url
        return self
    
    def set_method(self, method: str = "GET"):
        self.request.method = method
        # Автоматически добавляем JSON заголовки
        self.add_header("Content-Type", "application/json")
        self.add_header("Accept", "application/json")
        return self

class FormDataRequestBuilder(HTTPRequestBuilder):
    def set_url(self, url: str):
        self.request.url = url
        return self
    
    def set_method(self, method: str = "POST"):
        self.request.method = method
        self.add_header("Content-Type", "application/x-www-form-urlencoded")
        return self

class GraphQLRequestBuilder(HTTPRequestBuilder):
    def set_url(self, url: str):
        self.request.url = url
        return self
    
    def set_method(self, method: str = "POST"):
        self.request.method = method
        self.add_header("Content-Type", "application/json")
        self.add_header("Accept", "application/json")
        return self
    
    def set_query(self, query: str, variables: dict = None):
        self.request.data = {
            "query": query,
            "variables": variables or {}
        }
        return self

class HTTPRequestDirector:
    @staticmethod
    async def create_json_api_request(
        url: str,
        method: str = "GET",
        api_key: str = None,
        data: dict = None
    ) -> HTTPRequest:
        builder = JSONAPIRequestBuilder()
        builder.set_url(url).set_method(method)
        
        if api_key:
            builder.add_header("Authorization", f"Bearer {api_key}")
        
        if data and method in ["POST", "PUT", "PATCH"]:
            builder.set_data(data)
        
        return builder.build()
    
    @staticmethod
    async def create_graphql_request(
        url: str,
        query: str,
        variables: dict = None,
        api_key: str = None
    ) -> HTTPRequest:
        builder = GraphQLRequestBuilder()
        builder.set_url(url).set_method("POST").set_query(query, variables)
        
        if api_key:
            builder.add_header("Authorization", f"Bearer {api_key}")
        
        return builder.build()

async def test_builder():
    json_request = await HTTPRequestDirector.create_json_api_request(
        url="https://api.example.com/users",
        method="GET",
        api_key="secret-token-123"
    )
    result1 = await json_request.execute()
    
    graphql_query = """
        query {
            users {
                id
                name
                email
            }
        }
    """
    graphql_request = await HTTPRequestDirector.create_graphql_request(
        url="https://api.example.com/graphql",
        query=graphql_query,
        api_key="secret-token-123"
    )
    result2 = await graphql_request.execute()
    
    builder = FormDataRequestBuilder()
    manual_request = (builder
        .set_url("https://api.example.com/login")
        .set_method("POST")
        .add_param("redirect", "dashboard")
        .set_data({"username": "user", "password": "pass"})
        .set_timeout(10)
        .disable_ssl_verification()
        .build())
    result3 = await manual_request.execute()
    
    return [result1, result2, result3]