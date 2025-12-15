import asyncio
from abc import ABC, abstractmethod
from typing import List, Any

class AsyncIterator(ABC):
    @abstractmethod
    async def has_next(self) -> bool:
        pass
    
    @abstractmethod
    async def next(self) -> Any:
        pass

class TaskIterator(AsyncIterator):
    def __init__(self, tasks: List[str]):
        self._tasks = tasks
        self._position = 0
    
    async def has_next(self) -> bool:
        await asyncio.sleep(0.05)
        return self._position < len(self._tasks)
    
    async def next(self) -> Any:
        if not await self.has_next():
            raise StopAsyncIteration
        
        task = self._tasks[self._position]
        self._position += 1
        
        await asyncio.sleep(0.1)
        return task

class TaskCollection:
    def __init__(self):
        self._tasks = []
    
    def add_task(self, task: str):
        self._tasks.append(task)
    
    async def create_iterator(self) -> TaskIterator:
        return TaskIterator(self._tasks)

class PaginatedResults:
    def __init__(self, items: List[Any], page_size: int = 3):
        self.items = items
        self.page_size = page_size
        self.current_page = 0
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current_page * self.page_size >= len(self.items):
            raise StopAsyncIteration
        
        start_idx = self.current_page * self.page_size
        end_idx = start_idx + self.page_size
        page_items = self.items[start_idx:end_idx]
        
        self.current_page += 1
        await asyncio.sleep(0.1)
        
        return {
            "page": self.current_page,
            "items": page_items,
            "has_next": self.current_page * self.page_size < len(self.items)
        }