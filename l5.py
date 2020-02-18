
class Animal(object):

    def sayHello(self):
        print("Helo , I am a animal.")


class CanFly(Animal):

    def fly(self):
        print("I can fly.")

class CanRun(Animal):

    def run(self):
        print("I can run.")


class Dog(CanRun, CanFly):
    pass


d = Dog()

def run(self):
    print("Dog can run.")

from types import MethodType

dog = Animal()

dog.run = MethodType(run,dog)

dog.run()

print(isinstance(dog,CanRun))



