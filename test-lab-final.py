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
    
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

class SmartLight(SmartDevice):

    def turn_on(self):
        return f"Turning on [{self.name}] via [{self.connection_type}]"

    def turn_off(self):
        return f"Turning off [{self.name}] via [{self.connection_type}]"
    
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
            raise ValueError("Temperature must between 16 and 30")
        self.__temperature = temperature
        
    def turn_on(self):
        return f"Turning on [{self.name}] via [{self.connection_type.name}] in mode [{self.mode.name}] at [{self.temperature}]°C"
    
    def turn_off(self):
        return f"Turning off [{self.name}] via [{self.connection_type.name}] in mode [{self.mode.name}] at [{self.temperature}]°C"

class Scene:
    
    def __init__(self,name):
        self.__name = name
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
        # สร้างอุปกรณ์เพื่อเตรียมทดสอบ
        self.light = SmartLight(name="Ceiling Light", brand="Philips", room="Living Room", connection_type=ConnectionType.WIFI)
        self.ac = SmartAC(name="Master AC", brand="Daikin", room="Bedroom", connection_type=ConnectionType.ZIGBEE, mode=ACMode.COOL)

    def test_abstract_class_and_methods(self):
        # 1. ทดสอบว่าคลาสแม่เป็น Abstract Class จริง
        self.assertTrue(issubclass(SmartDevice, ABC))
        
        # 2. ต้องไม่สามารถสร้าง Object จากคลาสแม่ได้โดยตรง
        with self.assertRaises(TypeError):
            _ = SmartDevice(name="Test", brand="Test", room="Test", connection_type=ConnectionType.WIFI)

    def test_strict_encapsulation_all_private(self):
        # 3. ทดสอบว่าตัวแปรถูกซ่อนเป็น Private (__) จริง 
        # (ใน Python เมื่อใช้ __ ตัวแปรจะถูกซ่อน การพยายามเรียกตรงๆ ต้องเกิด AttributeError)
        with self.assertRaises(AttributeError):
            _ = self.light.__name
        with self.assertRaises(AttributeError):
            _ = self.light.__is_on
            
        # 4. ทดสอบว่าเข้าถึงข้อมูลผ่าน @property ได้ถูกต้อง
        self.assertEqual(self.light.name, "Ceiling Light")
        self.assertEqual(self.light.brand, "Philips")
        self.assertEqual(self.light.room, "Living Room")
        self.assertEqual(self.light.connection_type, ConnectionType.WIFI)
        self.assertFalse(self.light.is_on) # ค่าเริ่มต้นต้องเป็น False

    def test_ac_temperature_validation(self):
        # 5. ทดสอบการดึงค่าอุณหภูมิเริ่มต้น
        self.assertEqual(self.ac.temperature, 25)

        # 6. ทดสอบการตั้งค่า (Setter) ในช่วงที่ถูกต้อง
        self.ac.temperature = 24
        self.assertEqual(self.ac.temperature, 24)

        # 7. ทดสอบการโยน Error และตรวจสอบ "ข้อความแจ้งเตือน" ว่าตรงตามโจทย์เป๊ะหรือไม่
        with self.assertRaisesRegex(ValueError, "Temperature must be between 16 and 30"):
            self.ac.temperature = 10
            
        with self.assertRaisesRegex(ValueError, "Temperature must be between 16 and 30"):
            self.ac.temperature = 35

        # 8. ยืนยันว่าค่าอุณหภูมิไม่เปลี่ยนเมื่อใส่ค่าผิด
        self.assertEqual(self.ac.temperature, 24)

    def test_polymorphism_exact_string_match(self):
        # 9. ทดสอบ Polymorphism และฟอร์แมตข้อความที่ Return (ต้องตรงเป๊ะ)
        # หมายเหตุ: .name ของ Enum จะคืนค่าเช่น "WIFI" หรือ "COOL"
        expected_light_str = "Turning on Ceiling Light via WIFI"
        expected_ac_str = "Turning on Master AC via ZIGBEE in COOL mode at 25°C"
        
        self.assertEqual(self.light.turn_on(), expected_light_str)
        self.assertEqual(self.ac.turn_on(), expected_ac_str)

    def test_scene_execution(self):
        # 10. ทดสอบ Collections ระดับ Scene
        evening_scene = Scene() # สร้าง Scene
        evening_scene.add_device(self.light)
        evening_scene.add_device(self.ac)

        results = evening_scene.execute()
        
        # ตรวจสอบว่า Return ออกมาเป็น List ของ String ที่ถูกต้อง
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], "Turning on Ceiling Light via WIFI")
        self.assertEqual(results[1], "Turning on Master AC via ZIGBEE in COOL mode at 25°C")

    def test_smart_home_app_management(self):
        # 11. ทดสอบระบบจัดการระดับ App (การค้นหาและกรองข้อมูล)
        app = SmartHomeApp()
        app.add_device(self.light)
        app.add_device(self.ac)

        # ค้นหาด้วยชื่อ (Keyword)
        search_result = app.search_by_name("Master")
        self.assertEqual(len(search_result), 1)
        self.assertEqual(search_result[0].name, "Master AC")

        # กรองข้อมูลตามห้อง
        living_room_devices = app.get_devices_by_room("Living Room")
        self.assertEqual(len(living_room_devices), 1)
        self.assertEqual(living_room_devices[0].name, "Ceiling Light")

if __name__ == '__main__':
    unittest.main()