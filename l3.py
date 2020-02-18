

class Student(object):

    # __slots__ = ("name","age")

    def __str__(self):
        return "name is %s , age is %d" % (self.name,self.age)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self,value):

        if isinstance(value,int) :
            if value < 0 or value > 100:
                raise ValueError("Value must be in range 0 to 100")
        else:
            raise ValueError("Score is not int value.")

        self._score = value




s = Student()

s.name = "yikuyirong"
s.age = 42
s.score = 101

print(str(s))




