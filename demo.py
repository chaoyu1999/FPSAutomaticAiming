import keyboard


def abc(x):
    if x.name == 'caps lock':
        print(x)


keyboard.hook(abc)
keyboard.wait()
