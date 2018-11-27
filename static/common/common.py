import random


def get_random_color():

    return (
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    )

def get_random_yzm(i):
    res = ''
    for j in range(i):
        num = str(random.randint(0,9))
        S = chr(random.randint(65,90))
        s = chr(random.randint(97,122))
        c= random.choice([num,S,s])
        res +=c

    return res