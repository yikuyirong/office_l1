def log(message):
    def wrapper(func):
        def wrapper2(*args, **kw):
            print(f"call {func.__name__} begin , message {message}")
            func(*args, **kw)
            print(f"call {func.__name__} end")

        return wrapper2

    return wrapper


@log("abc")
def sayHello(name):
    print(f"Hello {name}")


if __name__ == '__main__':
    sayHello("yikuyirong")
