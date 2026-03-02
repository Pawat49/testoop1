import unittest
from abc import ABC,abstractmethod
from enum import Enum
# สมมติว่ามีการ import classes และ enums ต่างๆ จากไฟล์ที่คุณเขียน
# from smart_home import ConnectionType, ACMode, SmartDevice, SmartLight, SmartAC, Scene

class ConnectionType(Enum):
    WIFI = 1
    ZIGBEE = 2
    BLUTOOTH = 3

class ACMode(Enum):
    COOL = 4
    DRY = 5
    FAN = 6

class SmartDevice(ABC):
    def __init__(self,name,brand,room,connection_type):
        self.__name = name
        self.__brand = brand
        self.__room = room
        self.__connection_type = connection_type
        self.__is_on = False
        
    @property
    def name(self):
        return self.__name
    
    @property
    def brand(self):
        return self.__brand    
    
    @property
    def room(self):
        return self.__room
    
    @property
    def connection_type(self):
        return self.__connection_type
    
    @property
    def is_on(self):
        return self.__is_on
    
    @is_on.setter
    def is_on(self,is_on):
        self.__is_on = is_on
    
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

class SmartLight(SmartDevice):

    def turn_on(self):
        self.is_on = True
        return f"Turning on {self.name} via {self.connection_type.name}"

    def turn_off(self):
        self.is_on = False
        return f"Turning off {self.name} via {self.connection_type.name}"
    
class SmartAC(SmartDevice):

    def __init__(self, name, brand, room, connection_type,mode,temperature=25):
        super().__init__(name, brand, room, connection_type)
        self.__mode = mode
        self.__temperature = temperature

    @property
    def mode(self):
        return self.__mode
    
    @property
    def temperature(self):
        return self.__temperature
    
    @temperature.setter
    def temperature(self,temperature):
        if (temperature < 16) or (temperature > 30):
            raise ValueError("Temperature must be between 16 and 30")
        self.__temperature = temperature
        
    def turn_on(self):
        self.is_on = True
        return f"Turning on {self.name} via {self.connection_type.name} in {self.mode.name} mode at {self.temperature}°C"
    
    def turn_off(self):
        self.is_on = False
        return f"Turning off {self.name} via {self.connection_type.name} in {self.mode.name} mode at {self.temperature}°C"

class Scene:
    
    def __init__(self):
        self.__device = []

    def add_device(self,device):
        self.__device.append(device)

    def execute(self):
        device_list = []
        for device in self.__device:
            device_list.append(device.turn_on())
        return device_list

class SmartHomeApp:
    
    def __init__(self):
        self.__device = []

    def search_by_name(self,name):
        for device in self.__device:
            if device.name == name:
                return device
        return None
    
    def get_device_by_room(self,room):
        for device in self.__device:
            if device.room == room:
                return device
        return None

    def add_device(self,device):
        self.__device.append(device)

# สมมติว่ามีการ import classes และ enums จากไฟล์ที่ผู้เรียนเขียน
# from smart_home import ConnectionType, ACMode, SmartDevice, SmartLight, SmartAC, Scene, SmartHomeApp

class TestSmartHomeStrictOOP(unittest.TestCase):

    def setUp(self):
        self.light = SmartLight(name="Ceiling Light", brand="Philips", room="Living Room", connection_type=ConnectionType.WIFI)
        self.ac = SmartAC(name="Master AC", brand="Daikin", room="Bedroom", connection_type=ConnectionType.ZIGBEE, mode=ACMode.COOL)

    # ... (Test อื่นๆ ด้านบนเหมือนเดิม) ...

    def test_smart_home_app_management(self):
        app = SmartHomeApp()
        
        # สมมติว่ามีฟังก์ชันเพิ่มอุปกรณ์
        # (คุณอาจใช้ชื่ออื่น เช่น register_device ให้ปรับให้ตรงกับโค้ดคุณนะครับ)
        app.add_device(self.light)
        app.add_device(self.ac)

        # --- 1. ทดสอบกรณี: ค้นหา "เจอ" ---
        search_result = app.search_by_name("Master")
        
        # ดักจับ TypeError: เช็คก่อนเลยว่าค่าที่คืนมาต้องเป็น List นะ ห้ามเป็น None
        self.assertIsInstance(search_result, list, "Error: เจอข้อมูล แต่ไม่ได้คืนค่ากลับมาเป็น List")
        self.assertEqual(len(search_result), 1)
        self.assertEqual(search_result[0].name, "Master AC")

        # --- 2. ทดสอบกรณี: ค้นหา "ไม่เจอ" (ต้องเป็น None) ---
        not_found_search = app.search_by_name("Unknown Device")
        
        # ตัวนี้คือตัวเช็ค None ครับ ถ้าคุณคืนมาเป็น [] มันจะขึ้น Error ข้อความด้านหลัง
        self.assertIsNone(not_found_search, "Error: ค้นหาไม่เจอข้อมูล ต้อง Return เป็น None เท่านั้น (ห้ามเป็นลิสต์ว่าง)")

        # ทำแบบเดียวกันกับ get_devices_by_room
        not_found_room = app.get_devices_by_room("Kitchen")
        self.assertIsNone(not_found_room, "Error: ค้นหาห้องไม่เจอ ต้อง Return เป็น None เท่านั้น")
if __name__ == '__main__':
    unittest.main()