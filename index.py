import math
import random
import time
import turtle as t
turtle = t.Turtle()

tries = 20
size = 1000
radius = 100

screen = turtle.getscreen()
screen.screensize(size, size)
screen.setworldcoordinates(0, 0, size, size)
turtle.penup()
turtle.speed(size)

class Vector:
    x: float
    y: float

    def __init__(self, a_x = 1, a_y = 1):
        self.x = a_x
        self.y = a_y

    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalize(self):
        mag = self.magnitude()
        self.x /= mag
        self.y /= mag
        return self

    def isInside(self, minX: float, minY: float, maxX: float, MaxY: float):
        if self.x > minX and self.x < maxX and self.y > minY and self.y < MaxY:
            return True
        return False

    @staticmethod
    def fromRad(rad: float, radius: float = 1):
        x = math.sin(rad) * radius
        y = math.cos(rad) * radius
        return Vector(x, y)

    @staticmethod
    def random(width: float = 0, height: float = 0):
        if width <= 0 & height <= 0:
            rad = random.random() * (math.pi * 2)
            return Vector.fromRad(rad)
        else:
            return Vector(random.random() * width, random.random() * height)

    def __str__(self):
        return "x: " + str(self.x) + " y: " + str(self.y)

    def __iadd__(self, other: "Vector"):
        self.x += other.x
        self.y += other.y
        return self
    
    def __isub__(self, other: "Vector"):
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, other: "Vector"):
        if isinstance(other, self.__class__):
            self.x *= other.x
            self.y *= other.y
            return self
        if isinstance(other, float) | isinstance(other, int):
            self.x *= other
            self.y *= other
            return self

    def __add__(self, other: "Vector"):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector"):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other: "Vector"):
        if isinstance(other, self.__class__):
            return Vector(self.x * other.x, self.y * other.y)
        if isinstance(other, float) | isinstance(other, int):
            return Vector(self.x * other, self.y * other)
        

class Node:
    position: Vector

    def __init__(self, position: Vector = Vector.random(size, size)):
        self.position = position

    def getPoints(self, pointCount = tries, radius = radius):
        points = []
        radOffset = random.random() * (math.pi * 2)
        radMulti = math.pi * 2 / pointCount
        for i in range(pointCount):
            offset = radOffset + i * radMulti
            points.append(self.position + (Vector.fromRad(offset) * (random.random() * radius + radius)))
        return points

    def __str__(self):
        return str(self.position)


#Actual Important Algorithm

nodes = []
activeList = []

activeList.append(Node(Vector(size/2, size/2)))

while len(activeList) > 0:
    #index = random.randrange(0, len(activeList))
    node = activeList[random.randint(0, len(activeList) - 1)]
    
    turtle.goto(node.position.x, node.position.y)
    string = hex(round(abs(math.sin(time.clock() / 10)) * 0xffffff)).replace("0x", "")
    while len(string) < 6:
        string = "0" + string
    turtle.dot(radius, "#" + string)

    points = node.getPoints(tries)

    for p in points:
        isGood = True
        for a in activeList + nodes:
            if (p - a.position).magnitude() < radius or (not p.isInside(0, 0, size, size)):
                isGood = False
                break
        if isGood:
            activeList.append(Node(p))

    nodes.append(node)
    activeList.remove(node)

time.sleep(10000);