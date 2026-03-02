import unittest
from abc import ABC
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

import unittest
from abc import ABC

# สมมติว่ามีการ import classes และ enums จากไฟล์ที่ผู้เรียนเขียน
# from smart_home import ConnectionType, ACMode, SmartDevice, SmartLight, SmartAC, Scene, SmartHomeApp

class TestSmartHomeStrictEncapsulation(unittest.TestCase):

    def setUp(self):
        # สร้างอุปกรณ์เพื่อใช้ในการทดสอบ
        self.light = SmartLight(name="Ceiling Light", brand="Philips", room="Living Room", connection_type=ConnectionType.WIFI)
        self.ac = SmartAC(name="Master AC", brand="Daikin", room="Bedroom", connection_type=ConnectionType.ZIGBEE, mode=ACMode.COOL)

    def test_abstract_class(self):
        # ทดสอบว่าไม่สามารถสร้าง Object จาก Abstract Class ได้
        with self.assertRaises(TypeError):
            device = SmartDevice(name="Test", brand="Test", room="Test", connection_type=ConnectionType.WIFI)
        self.assertTrue(issubclass(SmartDevice, ABC))

    def test_strict_encapsulation_all_private(self):
        # ทดสอบว่าตัวแปรทุกตัวถูกสร้างเป็น Private จริง (เข้าถึงตรงๆ ต้องพัง)
        with self.assertRaises(AttributeError):
            _ = self.light.__name
        with self.assertRaises(AttributeError):
            _ = self.light.__brand
        with self.assertRaises(AttributeError):
            _ = self.light.__room
        with self.assertRaises(AttributeError):
            _ = self.light.__connection_type
        with self.assertRaises(AttributeError):
            _ = self.ac.__mode

        # ทดสอบว่าสามารถอ่านค่าผ่าน @property ได้อย่างถูกต้อง
        self.assertEqual(self.light.name, "Ceiling Light")
        self.assertEqual(self.light.brand, "Philips")
        self.assertEqual(self.light.room, "Living Room")
        self.assertEqual(self.light.connection_type, ConnectionType.WIFI)
        self.assertEqual(self.ac.mode, ACMode.COOL)

    def test_temperature_encapsulation_and_validation(self):
        # ทดสอบ Property ของอุณหภูมิแอร์ (ค่าเริ่มต้นควรเป็น 25)
        self.assertEqual(self.ac.temperature, 25)

        # ทดสอบการตั้งค่าอุณหภูมิที่ถูกต้อง (16 - 30)
        self.ac.temperature = 24
        self.assertEqual(self.ac.temperature, 24)

        # ทดสอบการตั้งค่าที่ผิด (ต้อง Throw ValueError)
        with self.assertRaises(ValueError):
            self.ac.temperature = 10
            
        with self.assertRaises(ValueError):
            self.ac.temperature = 35

        # ค่าต้องไม่ถูกเปลี่ยนแปลงจากคำสั่งที่ Error
        self.assertEqual(self.ac.temperature, 24)

    def test_polymorphism(self):
        # ทดสอบการ Override Method และการคืนค่า
        light_result = self.light.turn_on()
        ac_result = self.ac.turn_on()

        # เช็คว่าข้อความมีข้อมูลที่ถูกต้อง (ดึงค่าจาก Enum มาแสดงผล)
        # หมายเหตุ: .name ของ Enum จะคืนค่าเป็น String เช่น "WIFI", "COOL"
        self.assertIn("Turning on Ceiling Light via WIFI", light_result)
        self.assertIn("Turning on Master AC via ZIGBEE in COOL mode at 25°C", ac_result)

    def test_scene_execution(self):
        # ทดสอบการทำงานของ Scene (Collections)
        evening_scene = Scene(name="Evening Relax")
        evening_scene.add_device(self.light)
        evening_scene.add_device(self.ac)

        results = evening_scene.execute()
        self.assertEqual(len(results), 2)
        self.assertIn("WIFI", results[0])
        self.assertIn("COOL mode", results[1])

    def test_smart_home_app_management(self):
        # ทดสอบระบบจัดการหลัก (App)
        app = SmartHomeApp()
        app.add_device(self.light)
        app.add_device(self.ac)

        # ทดสอบการค้นหาด้วยชื่อ (Search)
        search_result = app.search_by_name("Master")
        self.assertEqual(len(search_result), 1)
        self.assertEqual(search_result[0].name, "Master AC")

        # ทดสอบการดึงข้อมูลตามห้อง (Filter by Room)
        living_room_devices = app.get_devices_by_room("Living Room")
        self.assertEqual(len(living_room_devices), 1)
        self.assertEqual(living_room_devices[0].name, "Ceiling Light")

if __name__ == '__main__':
    unittest.main()