
class Chain(object):

    def __init__(self,path=""):
        self.path = path

    def __call__(self, *args, **kwargs):
        return Chain("%s:%s" % (self.path, "".join(args)))

    def __getattr__(self, item):

        if item == "show":
            return lambda : self.path
        else:
            return Chain("%s/%s" % (self.path,item))

    # def __getattribute__(self, item):
    #     print(item)


path = Chain().users("yikuyirong").list("order").show()


print(path)
