import datetime


def main():
    test = "test, test".split(",")

    for i in range(len(test)):
        test[i] = test[i].strip()

    print("meow".split(", "))


main()
