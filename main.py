from time import sleep
import pygame
import os
import os.path as osp
from PIL import Image
from tqdm import tqdm
import string
import random
import numpy as np

"""
该程序用来标注数据，程序实现了能够随时停止，并且恢复运行后为上一次标注的位置
第一次运行确保图片需要修改图片起始保存路径为自己的路径，标注完成后图片保存在data目录中,名称为类型+随机字母+按放入顺序命名
标注错误无法撤销，请直接在文件中删除
要重新开始标注数据需要删除img_pth.txt文件和data目录下的所有文件夹
发现进度条不动时请停止点击
"""

"""图片起始保存路径"""
base_img_path = 'images'
# 定义五个按钮类型
NORMAL = 0
CLOSE_EYES = 1
OPEN_MOUTH = 2
HOLD_PHONE = 3
LOOK_AROUND = 4

# 定义图片路径列表
image_paths = os.listdir(base_img_path)
if not osp.exists('img_pth.txt'):
    with open('img_pth.txt', 'w', encoding='utf-8') as f:
        for pth in image_paths:
            f.write(pth)
            f.write('\n')
with open('img_pth.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
image_paths = []
for line in lines:
    image_paths.append(line.replace('\n', ''))
# 初始化pygame
pygame.init()

if not osp.exists('data/close_eyes'):
    os.mkdir('data/close_eyes')
if not osp.exists('data/hold_phone'):
    os.mkdir('data/hold_phone')
if not osp.exists('data/look_around'):
    os.mkdir('data/look_around')
if not osp.exists('data/normal'):
    os.mkdir('data/normal')
if not osp.exists('data/open_mouth'):
    os.mkdir('data/open_mouth')


def generate_random_string(length):
    # 生成随机的字母数字串
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))


# 创建窗口并加载图片
screen = pygame.display.set_mode((800, 600))
image = Image.open(osp.join(base_img_path, image_paths[0]))
# 创建五个按钮
button_normal = pygame.Rect(100, 500, 100, 50)
button_close_eyes = pygame.Rect(220, 500, 100, 50)
button_open_mouth = pygame.Rect(340, 500, 100, 50)
button_hold_phone = pygame.Rect(460, 500, 100, 50)
button_look_around = pygame.Rect(580, 500, 100, 50)

# 文字
font = pygame.font.Font("msyh.ttf", 16)
text_normal = font.render('正常', True, (0, 0, 0))
text_close_eyes = font.render('闭眼', True, (0, 0, 0))
text_open_mouth = font.render('张嘴', True, (0, 0, 0))
text_hold_phone = font.render('拿手机', True, (0, 0, 0))
text_look_around = font.render('四周看', True, (0, 0, 0))


# 定义事件处理函数
def handle_event(button_type, image):
    active = True
    random_string = generate_random_string(30)
    try:
        # 将图片存入对应的文件夹中
        if button_type == NORMAL:
            cls = 'normal'
            image.save(osp.join('data', cls, str(NORMAL) + random_string + 'image{:06d}.jpg'.format(
                len(os.listdir(osp.join('data', cls))) + 1)))
        elif button_type == CLOSE_EYES:
            cls = 'close_eyes'
            image.save(osp.join('data', cls, str(CLOSE_EYES) + random_string + 'image{:06d}.jpg'.format(
                len(os.listdir(osp.join('data', cls))) + 1)))
        elif button_type == OPEN_MOUTH:
            cls = 'open_mouth'
            image.save(osp.join('data', cls, str(OPEN_MOUTH) + random_string + 'image{:06d}.jpg'.format(
                len(os.listdir(osp.join('data', cls))) + 1)))
        elif button_type == HOLD_PHONE:
            cls = 'hold_phone'
            image.save(osp.join('data', cls, str(HOLD_PHONE) + random_string + 'image{:06d}.jpg'.format(
                len(os.listdir(osp.join('data', cls))) + 1)))
        elif button_type == LOOK_AROUND:
            cls = 'look_around'
            image.save(osp.join('data', cls, str(LOOK_AROUND) + random_string + 'image{:06d}.jpg'.format(
                len(os.listdir(osp.join('data', cls))) + 1)))
        # 显示下一张图片
        image_paths.pop(0)
        array_img1 = np.array(image.resize([800, 450]))

        image = Image.open(osp.join(base_img_path, image_paths[0]))
        array_img2 = np.array(image.resize([800, 450]))
        similarity = np.sum(
            (array_img1[:, array_img1.shape[1] // 3:, :array_img1.shape[1] // 3 * 2] - array_img2[:,
                    array_img2.shape[1] // 3:,  :array_img2.shape[1] // 3 * 2]) ** 2)
        if similarity > 10000000:
            active = False
        return active, image
    except Exception as e:
        print(e)

active = True
with tqdm(total=len(image_paths)) as pbar:
    # 渲染界面
    while True:
        text_pbar = font.render(str(pbar), True, (255, 0, 0))
        try:
            # 绘制图片和按钮
            rimg = image.resize([800, 450])
            pygame_image = pygame.image.fromstring(rimg.tobytes(), rimg.size, rimg.mode)
            screen.blit(pygame_image, (0, 0))
            pygame.draw.rect(screen, (255, 255, 255), button_normal)
            pygame.draw.rect(screen, (255, 255, 255), button_close_eyes)
            pygame.draw.rect(screen, (255, 255, 255), button_open_mouth)
            pygame.draw.rect(screen, (255, 255, 255), button_hold_phone)
            pygame.draw.rect(screen, (255, 255, 255), button_look_around)
            screen.blit(text_normal, (130, 515))
            screen.blit(text_close_eyes, (250, 515))
            screen.blit(text_open_mouth, (370, 515))
            screen.blit(text_hold_phone, (490, 515))
            screen.blit(text_look_around, (610, 515))
            screen.blit(text_pbar, (350, 400))

            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open('img_pth.txt', 'w', encoding='utf-8') as f:
                        for line in image_paths:
                            f.write(line)
                            f.write('\n')
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_normal.collidepoint(event.pos):
                        active, image = handle_event(NORMAL, image)
                        pbar.update(1)
                    elif button_close_eyes.collidepoint(event.pos):
                        active, image = handle_event(CLOSE_EYES, image)
                        pbar.update(1)
                    elif button_open_mouth.collidepoint(event.pos):
                        active, image = handle_event(OPEN_MOUTH, image)
                        pbar.update(1)
                    elif button_hold_phone.collidepoint(event.pos):
                        active, image = handle_event(HOLD_PHONE, image)
                        pbar.update(1)
                    elif button_look_around.collidepoint(event.pos):
                        active, image = handle_event(LOOK_AROUND, image)
                        pbar.update(1)
                    # if not active:
                    #     print('sleep 3s')
                    #     sleep(3)
                    #     pygame.event.clear()
            if not image_paths:
                pygame.quit()
                exit()
            # 更新界面
            pygame.display.update()
        except Exception as e:
            sleep(3)
            print(e)
            image = Image.open(osp.join(base_img_path, image_paths[0]))
