# ============================================================
# PYTHON OOP EXERCISE — For experienced devs new to Python
# Topics: classes, dunder methods, encapsulation, inheritance,
#         super(), abstract base classes, properties,
#         classmethods, staticmethods, mixins
# ============================================================
# Run with: python learn-python/oop-exercise.py


# ------ SECTION 1: Classes & Instances ------
#
# In Python a class is defined with `class`. The constructor is
# always named `__init__` (double underscore = "dunder").
# `self` is always the first parameter — it's the instance itself
# (equivalent to `this` in Java/C#/JS, but explicit, not implicit).
#
# TASK 1a: Define a class `Robot` with:
#   - __init__(self, name: str, battery: int)  stores both attributes
#   - a method `status(self)` that prints  "Robot <name>: battery <battery>%"
# Then create two Robot instances and call status() on each.


class Robot:
    def __init__(self, name: str, battery: int):
        self.name = name
        self.battery = battery

    def status(self):
        print(f"Robot {self.name}: battery {self.battery}%")


r1 = Robot("R2D2", 80)
r2 = Robot("C3PO", 45)
r1.status()  # Robot R2D2: battery 80%
r2.status()  # Robot C3PO: battery 45%


# ------ SECTION 2: Dunder (magic) methods ------
#
# Python uses dunder methods to hook into built-in operations:
#   __str__  → what str(obj) / print(obj) shows (human-readable)
#   __repr__ → what repr(obj) shows (developer / debug view)
#   __eq__   → what == does
#   __lt__   → what < does  (enables sorting)
#
# TASK 2a: Add __str__ so print(r1) shows  "Robot(R2D2, 80%)"
# TASK 2b: Add __repr__ so repr(r1) shows  "Robot(name='R2D2', battery=80)"
# TASK 2c: Add __eq__  so two robots are equal when their names match
# TASK 2d: Add __lt__  so robots sort by battery ascending
#
# Redefine Robot below with all of the above added.


class Robot:
    def __init__(self, name: str, battery: int):
        self.name = name
        self.battery = battery

    def status(self): ...

    def __str__(self):
        return f"Robot({self.name}, {self.battery}%)"

    def __repr__(self):
        return f"Robot(name={self.name!r}, battery={self.battery})"

    def __eq__(self, other):
        if self.name == other.name:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.battery < other.battery:
            return True
        else:
            return False


r1 = Robot("R2D2", 80)
r2 = Robot("C3PO", 45)
r3 = Robot("R2D2", 99)
print(r1)  # Robot(R2D2, 80%)
print(repr(r2))  # Robot(name='C3PO', battery=45)
print(r1 == r3)  # True  — same name
print(sorted([r1, r2]))  # [Robot(name='C3PO'...), Robot(name='R2D2'...)]


# ------ SECTION 3: Encapsulation ------
#
# Python has no true private — convention signals intent instead:
#   self.name    → public: anyone can read/write
#   self._state  → protected: internal; subclasses may use it
#   self.__code  → name-mangled: becomes self._ClassName__code;
#                  accidental external access is harder but not impossible
#
# TASK 3a: Add a `_log` list (protected) that records each call to
#          status() as "status called at battery <n>".
#          Add a method `get_log(self)` that returns the list.
#
# TASK 3b: Add a `__secret_key` attribute (mangled) set to "XK-47".
#          Then run the two lines below — predict which one errors and why.
#
# Redefine Robot below with the full Section 2 interface PLUS the above.


class Robot:
    def __init__(self, name: str, battery: int):
        self.name = name
        self.battery = battery
        self._log = []
        self.__secret_key = "XK-47"

    def __str__(self):
        return f"Robot({self.name}, {self.battery}%)"

    def __repr__(self):
        return f"Robot(name={self.name}, battery={self.battery})"

    def __eq__(self, other):
        if self.name == other.name:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.battery < other.battery:
            return self
        else:
            return other

    def status(self):
        self._log.append(f"status called at battery {self.battery}")

    def get_log(self):
        return self._log


r1 = Robot("R2D2", 80)
r1.status()
r1.status()
print(r1.get_log())  # ['status called at battery 80', ...]

try:
    print(r1.__secret_key)  # AttributeError — why?
except AttributeError as e:
    print(f"Caught: {e}")

print(r1._Robot__secret_key)  # "XK-47" — mangled name still reachable


# ------ SECTION 4: Properties ------
#
# @property turns a method into a read-only attribute.
# @<name>.setter adds a write accessor with validation.
# This is the Python idiom for getters/setters — don't write
# getBattery()/setBattery() Java-style.
#
# TASK 4a: Replace `self.battery` with a property backed by `self._battery`.
#          The setter should raise ValueError if the value is outside 0–100.
# TASK 4b: Add a read-only property `is_low` that returns True when battery < 20.
#
# You only need the constructor, the two properties, and __str__ here.


class Robot:
    def __init__(self, name: str, battery: int):
        self.name = name
        self.battery = battery  # this should go through the setter

    @property
    def battery(self) -> int:
        return self._battery

    @battery.setter
    def battery(self, value: int):
        if value >= 0 and value <= 100:
            self._battery = value
        else:
            raise ValueError(f"Value is outside the range 0-100")

    @property
    def is_low(self) -> bool:
        if self._battery < 20:
            return True
        else:
            return False

    def __str__(self):
        return f"Robot({self.name}, {self.battery}%)"


r1 = Robot("R2D2", 80)
print(r1.battery)  # 80
r1.battery = 15
print(r1.is_low)  # True

try:
    r1.battery = 150  # ValueError
except ValueError as e:
    print(f"Caught: {e}")


# ------ SECTION 5: Class methods & Static methods ------
#
# @classmethod receives the *class* (cls) as first arg, not the instance.
#   Use it for alternative constructors / factory methods.
# @staticmethod receives no implicit first arg — just a plain function
#   that lives in the class namespace for logical grouping.
#
# TASK 5a: Add a classmethod `Robot.fully_charged(name)` that returns
#          a Robot with battery=100.
# TASK 5b: Add a staticmethod `Robot.is_valid_name(name)` that returns
#          True only if name is a non-empty string.
#
# Include status() in this redefinition — it's needed by Section 6.


class Robot:
    def __init__(self, name: str, battery: int):
        self.name = name
        self.battery = battery

    def status(self):
        print(f"Robot {self.name}: battery {self.battery}%")

    @classmethod
    def fully_charged(cls, name: str) -> "Robot":
        return cls(name, 100)

    @staticmethod
    def is_valid_name(name: str) -> bool:
        if len(name) > 0:
            return True
        else:
            return False

    def __str__(self):
        return f"Robot({self.name}, {self.battery}%)"


full = Robot.fully_charged("BB-8")
print(full)  # Robot(BB-8, 100%)
print(Robot.is_valid_name("R2D2"))  # True
print(Robot.is_valid_name(""))  # False


# ------ SECTION 6: Inheritance & super() ------
#
# Python uses `class Child(Parent)` syntax.
# `super().__init__(...)` calls the parent constructor.
# Override a method by redefining it; call super() to extend rather
# than fully replace the parent behaviour.
#
# TASK 6a: Create `DroneRobot(Robot)` with an extra `altitude: int` param.
#          Override `status()` to print the parent line AND
#          "  └ altitude: <altitude>m" on the next line.
#
# TASK 6b: Create `SurgicalRobot(Robot)` with extra `precision: float`.
#          Override __str__ to include precision.


class DroneRobot(Robot):
    def __init__(self, name: str, battery: int, altitude: int):
        super().__init__(name, battery)
        self._altitude = altitude

    def status(self):
        super().status()
        print(f"  └ altitude: {self._altitude}m")

    def __str__(self):
        return f"DroneRobot({self.name}, {self.battery}%, {self._altitude}m)"


class SurgicalRobot(Robot):
    def __init__(self, name: str, battery: int, precision: float):
        super().__init__(name, battery)
        self._precision = precision

    def __str__(self):
        return (
            f"SurgicalRobot({self.name}, {self.battery}%, precision={self._precision})"
        )


drone = DroneRobot("Falcon", 60, 120)
drone.status()
# Robot Falcon: battery 60%
#   └ altitude: 120m
print(drone)  # DroneRobot(Falcon, 60%, 120m)

surgeon = SurgicalRobot("DaVinci", 90, 0.01)
print(surgeon)  # SurgicalRobot(DaVinci, 90%, precision=0.01)

print(isinstance(drone, Robot))  # True — is-a relationship


# ------ SECTION 7: Abstract Base Classes (Python's interfaces) ------
#
# Python has no `interface` keyword. The equivalent is an ABC:
#   - subclass ABC and mark methods with @abstractmethod
#   - any class that doesn't implement all abstract methods
#     cannot be instantiated — same guarantee as a Java interface
#
# TASK 7a: Define abstract class `Sensor(ABC)` with:
#   - abstract method `read(self) -> float`
#   - abstract method `unit(self) -> str`
#   - concrete method `report(self)` that prints "<read()> <unit()>"
#
# TASK 7b: Implement `TemperatureSensor(Sensor)` — return 36.6 and "°C"
# TASK 7c: Implement `PressureSensor(Sensor)` — return 1013.25 and "hPa"
# TASK 7d: Try to instantiate `Sensor()` directly and observe the TypeError.

from abc import ABC, abstractmethod


class Sensor(ABC):
    @abstractmethod
    def read(self) -> float: ...

    @abstractmethod
    def unit(self) -> str: ...

    def report(self):
        print(f"{self.read()} {self.unit()}")


class TemperatureSensor(Sensor):
    def read(self) -> float:
        return 36.6

    def unit(self) -> str:
        return "°C"


class PressureSensor(Sensor):
    def read(self) -> float:
        return 1013.25

    def unit(self) -> str:
        return "hPa"


TemperatureSensor().report()  # 36.6 °C
PressureSensor().report()  # 1013.25 hPa

try:
    Sensor()
except TypeError as e:
    print(f"Caught: {e}")

# Polymorphism — treat all sensors the same way
sensors: list[Sensor] = [TemperatureSensor(), PressureSensor()]
for s in sensors:
    s.report()


# ------ SECTION 8: Mixins (multiple inheritance done right) ------
#
# Python supports multiple inheritance. The safe idiomatic pattern is
# a *mixin*: a small class that adds one capability, no __init__,
# never used standalone.
#
# Python resolves method lookup left-to-right via the MRO
# (Method Resolution Order). Print LoggableDrone.__mro__ to see it.
#
# TASK 8a: Create `LoggableMixin` with:
#   - `log(self, msg)` — prefixes msg with class name, stores in self._log
#     (initialise _log lazily with hasattr so it works with any base class)
#   - `dump_log(self)` — prints every stored line
#
# TASK 8b: Create `LoggableDrone(LoggableMixin, DroneRobot)`.
#          Override status() to call super().status() then self.log(...)
#          with a message recording battery and altitude.


class LoggableMixin:
    def log(self, msg: str):
        newmsg = f"[{self.__class__.__name__}] {msg}"
        if hasattr(self, "_log"):
            self._log.append(newmsg)
        else:
            self._log = []
            self._log.append(newmsg)

    def dump_log(self):
        for line in self._log:
            print(line)


class LoggableDrone(LoggableMixin, DroneRobot):
    def status(self):
        super().status()
        self.log(f"status reported — battery {self.battery}%, alt {self._altitude}m")


ld = LoggableDrone("Eagle", 55, 200)
ld.status()
ld.status()
ld.dump_log()
# [LoggableDrone] status reported — battery 55%, alt 200m
# [LoggableDrone] status reported — battery 55%, alt 200m

print(LoggableDrone.__mro__)


# ------ SECTION 9: Dataclasses (modern shortcut) ------
#
# @dataclass auto-generates __init__, __repr__, and __eq__ from
# annotated fields. Add `order=True` to get __lt__ etc. for free.
# Use `field(default_factory=...)` for mutable defaults (lists, dicts).
#
# TASK 9a: Write `RobotDC` as a @dataclass with fields:
#   name: str, battery: int, sensors: list[str]  (default empty list)
#   Add order=True so instances are sortable.
# Confirm print(), ==, and sorted() all work without writing them.

from dataclasses import dataclass, field


@dataclass(order=True)
class RobotDC:
    name: str
    battery: int = field(compare=False)
    sensors: list[str] = field(default_factory=list, compare=False)


ra = RobotDC("R2D2", 80)
rb = RobotDC("C3PO", 45)
ra.sensors.append("lidar")

print(ra)  # RobotDC(name='R2D2', battery=80, sensors=['lidar'])
print(ra == RobotDC("R2D2", 80))  # True
print(sorted([ra, rb]))  # sorted by name then battery
