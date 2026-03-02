import unittest

# สมมติว่ามีการ import classes ต่างๆ ที่คุณเขียนไว้
# from smart_home import SmartLight, SmartAC, Scene, SmartHomeApp

class TestSmartHomePolymorphism(unittest.TestCase):

    def setUp(self):
        # สร้าง App
        self.app = SmartHomeApp()
        
        # สร้างอุปกรณ์ (Light และ AC) ที่มีการเชื่อมต่อต่างกัน
        self.light1 = SmartLight(name="Living Room Main", brand="Philips", room="Living Room", conn_type="Wi-Fi")
        self.light2 = SmartLight(name="Bedroom Lamp", brand="Xiaomi", room="Bedroom", conn_type="Bluetooth")
        self.ac1 = SmartAC(mode="Cool", name="Master AC", brand="Daikin", room="Bedroom", conn_type="Zigbee")
        
        # เพิ่มเข้า App
        self.app.register_device(self.light1)
        self.app.register_device(self.light2)
        self.app.register_device(self.ac1)

    def test_polymorphism_turn_on(self):
        # ทดสอบว่าแต่ละอุปกรณ์เรียก Method เดียวกัน (turn_on) 
        # แต่ผลลัพธ์การทำงาน (Protocol) ต่างกันตาม conn_type
        # หมายเหตุ: ในโค้ดจริงอาจจะเป็นการเช็คค่า String ที่ return ออกมา หรือ Mock print
        self.assertEqual(self.light1.turn_on(), "Sending Wi-Fi signal to turn on Living Room Main")
        self.assertEqual(self.light2.turn_on(), "Sending Bluetooth pairing signal to turn on Bedroom Lamp")
        self.assertEqual(self.ac1.turn_on(), "Sending Zigbee mesh signal to turn on Master AC in Cool mode")

    def test_mixed_devices_in_scene(self):
        # ทดสอบการสร้าง Scene ที่มีอุปกรณ์ผสมกัน
        sleep_scene = Scene(name="Good Night")
        sleep_scene.add_device(self.light2) # เพิ่มไฟ
        sleep_scene.add_device(self.ac1)    # เพิ่มแอร์
        
        # อุปกรณ์ 1 ชิ้นอยู่ได้หลาย Scene
        movie_scene = Scene(name="Movie Time")
        movie_scene.add_device(self.light1)
        movie_scene.add_device(self.ac1)    # แอร์ตัวเดิมอยู่ในอีก Scene ได้
        
        self.app.add_scene(sleep_scene)
        self.app.add_scene(movie_scene)
        
        # ตรวจสอบจำนวนอุปกรณ์ใน Scene
        self.assertEqual(len(sleep_scene.get_devices()), 2)
        
    def test_execute_scene(self):
        # ทดสอบการสั่งทำงานระดับ Scene
        sleep_scene = Scene(name="Good Night")
        sleep_scene.add_device(self.light2)
        sleep_scene.add_device(self.ac1)
        
        # เมื่อสั่ง execute scene ควรเรียกคำสั่ง turn_on ของทุกอุปกรณ์ในลิสต์
        results = sleep_scene.execute()
        self.assertIn("Sending Bluetooth pairing signal to turn on Bedroom Lamp", results)
        self.assertIn("Sending Zigbee mesh signal to turn on Master AC in Cool mode", results)

    def test_search_device_by_name_or_brand(self):
        # ทดสอบการค้นหา
        search_results = self.app.search("Xiaomi")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].name, "Bedroom Lamp")

    def test_view_by_room(self):
        # ทดสอบการดึงข้อมูลตาม Room (เทียบเท่าการดึงเพลงตาม Album)
        bedroom_devices = self.app.get_devices_by_room("Bedroom")
        self.assertEqual(len(bedroom_devices), 2) # ควรเจอ light2 และ ac1

if __name__ == '__main__':
    unittest.main()
