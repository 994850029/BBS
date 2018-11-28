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
        res += c

    return res

def add_dianxiang(width,height,img_draw):
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        # 在图片上画线
        img_draw.line((x1, y1, x2, y2), fill=get_random_color())

    for i in range(10):
        # 画点
        img_draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        # 画弧形
        img_draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

