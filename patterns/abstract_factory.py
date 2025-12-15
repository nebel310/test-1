import asyncio
from abc import ABC, abstractmethod
from enum import Enum

class OSType(Enum):
    WINDOWS = "windows"
    LINUX = "linux"
    MACOS = "macos"

class Button(ABC):
    @abstractmethod
    async def render(self) -> dict:
        pass

class Checkbox(ABC):
    @abstractmethod
    async def render(self) -> dict:
        pass

class TextField(ABC):
    @abstractmethod
    async def render(self) -> dict:
        pass

class WindowsButton(Button):
    async def render(self) -> dict:
        await asyncio.sleep(0.1)
        return {
            "os": "Windows",
            "type": "button",
            "style": "Windows 11 style",
            "color": "blue",
            "border": "rounded corners"
        }

class WindowsCheckbox(Checkbox):
    async def render(self) -> dict:
        await asyncio.sleep(0.1)
        return {
            "os": "Windows",
            "type": "checkbox",
            "style": "Windows checkbox",
            "animation": "smooth toggle"
        }

class WindowsTextField(TextField):
    async def render(self) -> dict:
        await asyncio.sleep(0.1)
        return {
            "os": "Windows",
            "type": "text field",
            "style": "Windows input",
            "placeholder": "Enter text..."
        }

class LinuxButton(Button):
    async def render(self) -> dict:
        await asyncio.sleep(0.1)
        return {
            "os": "Linux",
            "type": "button",
            "style": "GTK style",
            "color": "gray",
            "border": "sharp corners"
        }

class LinuxCheckbox(Checkbox):
    async def render(self) -> dict:
        await asyncio.sleep(0.1)
        return {
            "os": "Linux",
            "type": "checkbox",
            "style": "Linux checkbox",
            "animation": "instant toggle"
        }

class LinuxTextField(TextField):
    async def render(self) -> dict:
        await asyncio.sleep(0.1)
        return {
            "os": "Linux",
            "type": "text field",
            "style": "Linux input",
            "placeholder": "Type here..."
        }

class MacOSButton(Button):
    async def render(self) -> dict:
        await asyncio.sleep(0.1)
        return {
            "os": "macOS",
            "type": "button",
            "style": "Apple style",
            "color": "white",
            "border": "rounded with shadow"
        }

class MacOSCheckbox(Checkbox):
    async def render(self) -> dict:
        await asyncio.sleep(0.1)
        return {
            "os": "macOS",
            "type": "checkbox",
            "style": "macOS checkbox",
            "animation": "smooth fade"
        }

class MacOSTextField(TextField):
    async def render(self) -> dict:
        await asyncio.sleep(0.1)
        return {
            "os": "macOS",
            "type": "text field",
            "style": "macOS input",
            "placeholder": "Search..."
        }

class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass
    
    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass
    
    @abstractmethod
    def create_text_field(self) -> TextField:
        pass

class WindowsUIFactory(UIFactory):
    def create_button(self) -> Button:
        return WindowsButton()
    
    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()
    
    def create_text_field(self) -> TextField:
        return WindowsTextField()

class LinuxUIFactory(UIFactory):
    def create_button(self) -> Button:
        return LinuxButton()
    
    def create_checkbox(self) -> Checkbox:
        return LinuxCheckbox()
    
    def create_text_field(self) -> TextField:
        return LinuxTextField()

class MacOSUIFactory(UIFactory):
    def create_button(self) -> Button:
        return MacOSButton()
    
    def create_checkbox(self) -> Checkbox:
        return MacOSCheckbox()
    
    def create_text_field(self) -> TextField:
        return MacOSTextField()

class UIFactoryProducer:
    @staticmethod
    def get_factory(os_type: OSType) -> UIFactory:
        if os_type == OSType.WINDOWS:
            return WindowsUIFactory()
        elif os_type == OSType.LINUX:
            return LinuxUIFactory()
        elif os_type == OSType.MACOS:
            return MacOSUIFactory()
        else:
            raise ValueError(f"Неизвестный тип ОС: {os_type}")

async def test_abstract_factory(os_type: OSType):
    factory = UIFactoryProducer.get_factory(os_type)
    
    button = factory.create_button()
    checkbox = factory.create_checkbox()
    text_field = factory.create_text_field()

    button_result = await button.render()
    checkbox_result = await checkbox.render()
    text_field_result = await text_field.render()
    
    return {
        "os": os_type.value,
        "components": [button_result, checkbox_result, text_field_result]
    }