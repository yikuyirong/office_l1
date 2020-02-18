
class Screen(object):

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self,value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self,value):
        self._height = value

    @property
    def resolution(self):
        return "%d * %d" % (self.width , self.height)

    def __str__(self):
        return "width is : %d, height is : %d, resolution is %s" % (self.width,self.height,self.resolution)


s = Screen()

s.width = 1024
s.height = 768

print(str(s))



