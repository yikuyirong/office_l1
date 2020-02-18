


class Parent(object):

    def __init__(self,name):
        print(f"Hello {name}")

class Child(Parent):

    def __init__(self):

        Parent.__init__(self,"yikuyirong")

        # super(Child,self).__init__("yikuyirong")



Child()
