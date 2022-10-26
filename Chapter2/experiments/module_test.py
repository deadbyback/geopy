# coding=utf-8


print("I'm module_test.py and my name is: " + __name__)


def function1():
    print("Hi, I'm inside function1.")


if __name__ == '__main__':
    print("Calling function1 - only if i'm __main__...")
    function1()
