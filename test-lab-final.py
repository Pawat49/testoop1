import unittest
from abc import ABC

# สมมติว่ามีการ import classes และ enums ต่างๆ จากไฟล์ที่คุณเขียน
# from smart_home import ConnectionType, ACMode, SmartDevice, SmartLight, SmartAC, Scene

class TestSmartHomePythonicOOP(unittest.TestCase):

    def setUp(self):
        self.light = SmartLight(name="Ceiling Light", brand="Philips", room="Living Room", connection_type=ConnectionType.WIFI)
        self.ac = SmartAC(name="Master AC", brand="Daikin", room="Bedroom", connection_type=ConnectionType.ZIGBEE, mode=ACMode.COOL)

    def test_abstract_class(self):
        with self.assertRaises(TypeError):
            device = SmartDevice(name="Test", brand="Test", room="Test", connection_type=ConnectionType.WIFI)
        self.assertTrue(issubclass(SmartDevice, ABC))

    def test_encapsulation_with_property(self):
        # ทดสอบการเรียก Get ผ่าน @property (เรียกเหมือนตัวแปร ไม่ต้องมีวงเล็บ)
        self.assertFalse(self.light.is_on)
        self.assertEqual(self.ac.temperature, 25)

        # ทดสอบการเรียก Set ผ่าน @property.setter (ตั้งค่าอุณหภูมิที่ถูกต้อง)
        self.ac.temperature = 24
        self.assertEqual(self.ac.temperature, 24)

        # ค่าต่ำหรือสูงเกินไป ต้องเกิด ValueError ตามที่ดักไว้ใน setter
        with self.assertRaises(ValueError):
            self.ac.temperature = 10
            
        with self.assertRaises(ValueError):
            self.ac.temperature = 35

        # ตรวจสอบว่าค่าอุณหภูมิยังคงเป็น 24 (ไม่ถูกเปลี่ยนจากคำสั่งที่ผิดพลาด)
        self.assertEqual(self.ac.temperature, 24)

        # ตรวจสอบการพยายามเข้าถึง private variable ตรงๆ (ต้องเกิด AttributeError)
        with self.assertRaises(AttributeError):
            temp = self.ac.__temperature

    def test_polymorphism(self):
        light_result = self.light.turn_on()
        ac_result = self.ac.turn_on()

        self.assertIn("Turning on Ceiling Light via WIFI", light_result)
        self.assertIn("Turning on Master AC via ZIGBEE in COOL mode at 25°C", ac_result)

    def test_scene_execution(self):
        evening_scene = Scene(name="Evening Relax")
        evening_scene.add_device(self.light)
        evening_scene.add_device(self.ac)

        results = evening_scene.execute()
        self.assertEqual(len(results), 2)
        self.assertIn("WIFI", results[0])
        self.assertIn("COOL mode", results[1])

if __name__ == '__main__':
    unittest.main()