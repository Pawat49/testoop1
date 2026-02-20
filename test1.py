from abc import ABC, abstractmethod
import unittest

class Employee(ABC):

    def __init__(self,name,base_rate):
        self.__name = name
        self.__base_rate = base_rate

    # getter artibute Employee
    @property
    def name(self):
        return self.__name
    
    @property
    def base_rate(self):
        return self.__base_rate
    
    # setter aritibute Employee
    @name.setter
    def name(self,name):
        if isinstance(name,int):
            raise ValueError("name can't be int")
        self.__name = name
    
    @base_rate.setter
    def base_rate(self,base_rate):
        if base_rate <= 0:
            raise ValueError("base rate lower than 0")
        self.__base_rate = base_rate
    
    @abstractmethod
    def calculate_salary(self):
        pass

class FullTimeEmployee(Employee):
    
    def __init__(self, name, base_rate,bonus):
        super().__init__(name, base_rate)
        self.__bonus = bonus

    # getter artibute Employee
    @property
    def bonus(self):
        return self.__bonus
    
    # setter artibute FullTimeEmployee
    @bonus.setter
    def bonus(self,bonus):
        if bonus <= 0:
            raise ValueError("base rate lower than 0")
        self.__bonus = bonus
        
    def calculate_salary(self):
        return self.base_rate + self.bonus

class PartTimeEmployee(Employee):
    
    def __init__(self, name, base_rate,hours_worked):
        super().__init__(name, base_rate)
        self.__hours_worked = hours_worked

    # getter artibute Employee
    @property
    def hours_worked(self):
        return self.__hours_worked
    
    # setter artibute PartTimeEmployee 
    @hours_worked.setter
    def hours_worked(self,hours_worked):
        if hours_worked < 0:
            raise ValueError("hours worked lower than 0")
        self.__hours_worked = hours_worked

    def calculate_salary(self):
        return self.base_rate * self.hours_worked
    

class TestEmployeePayrollSystem(unittest.TestCase):

    def test_1_abstraction(self):
        with self.assertRaises(TypeError):
            emp = Employee("John", 15000)

    def test_2_encapsulation(self):
        emp1 = FullTimeEmployee("Alice", 20000, 5000)
        
        # เช็ค Getter (ดึงค่าผ่าน @property)
        self.assertEqual(emp1.name, "Alice")
        self.assertEqual(emp1.base_rate, 20000)
        
        # เช็ค Setter แบบถูกต้อง (อัปเดตค่าผ่าน @base_rate.setter)
        emp1.base_rate = 25000
        self.assertEqual(emp1.base_rate, 25000)
        
        # เช็ค Setter แบบค่าผิดเงื่อนไข
        with self.assertRaises(ValueError):
            emp1.base_rate = -500
        with self.assertRaises(ValueError):
            emp1.base_rate = 0

    def test_3_inheritance(self):
        emp_pt = PartTimeEmployee("Bob", 300, 40)
        
        self.assertTrue(isinstance(emp_pt, Employee))
        self.assertEqual(emp_pt.name, "Bob") 

    def test_4_polymorphism(self):
        emp_ft = FullTimeEmployee("Charlie", 30000, 10000)
        emp_pt = PartTimeEmployee("David", 500, 120)
        
        employees = [emp_ft, emp_pt]
        salaries = [emp.calculate_salary() for emp in employees]
        
        self.assertEqual(salaries, [40000, 60000])

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)

