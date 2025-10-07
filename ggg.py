def args(arguments):
    print("dj")
    def act_dec(func):
        def wrapper(argumets):
            print(arguments)
            func()
        return wrapper
    return act_dec

@args(1)
def exapmple():
    print("hello")

exapmple()