import os
from PIL import Image
from tqdm import tqdm
from flask import current_app
from hashlib import md5
from app.models.user import User
from random import randint
from app import db


def fake_profile(source_path, temp_path, max_img=None):
    """
    将文件夹中的图像进行放缩，使其生成头像，并进行临时存储
    :param source_path: 原目录
    :param temp_path: 目标目录
    :param max_img: 最多使用多少图像
    :return:
    """
    assert os.path.exists(source_path)
    if not max_img:
        max_img = 99999
    # 获取图像源全部的图像列表
    img_path = os.listdir(source_path)
    # 过滤，仅保留jpg与png格式
    img_path = filter(lambda x: os.path.splitext(x)[1] in (".jpg", ".png"), img_path)
    img_path = list(img_path)

    # 获取avatar保存地址
    app = current_app._get_current_object()
    base = app.config['AVATAR_PATH']

    # 获取初始化数据
    height = app.config['AVATAR_HEIGHT']
    width = app.config['AVATAR_WIDTH']
    min_height = app.config['AVATAR_MIN_HEIGHT']
    min_width = app.config['AVATAR_MIN_WIDTH']

    # 用于存放经过图像哈希值的列表
    md5_list = list()
    i = 0
    with tqdm(total=min(len(img_path), max_img), unit="items") as pbar:
        pbar.set_description('process img')
        for p in img_path:
            path = os.path.join(source_path, p)
            pbar.update(1)
            try:
                # 处理并保存图像
                img = Image.open(path)
                img.thumbnail((height, width))
                img.save(temp_path)
                # 取图像哈希值，并存入md5_list列表
                with open(temp_path, "rb") as f:
                    img_hash = md5(f.read()).hexdigest()
                md5_list.append(img_hash)
                # 将图像按照哈希值保存到AVATAR_PATH中的avatar中
                base_img = os.path.join(base, "avatar")
                if not os.path.exists(base_img):
                    os.mkdir(base_img)
                file_dir_base = os.path.join(base_img, img_hash[:2])
                if not os.path.exists(file_dir_base):
                    os.mkdir(file_dir_base)
                img.save(os.path.join(file_dir_base, img_hash + ".png"))

                # 将图像按照哈希值保存到AVATAR_PATH中的avatar_min中
                img.thumbnail((min_height, min_width))
                base_img_min = os.path.join(base, "min_avatar")
                if not os.path.exists(base_img_min):
                    os.mkdir(base_img_min)
                file_dir_base = os.path.join(base_img_min, img_hash[:2])
                if not os.path.exists(file_dir_base):
                    os.mkdir(file_dir_base)
                img.save(os.path.join(file_dir_base, img_hash + ".png"))

                i += 1
                if i >= max_img:
                    break
            except Exception as e:
                print(e)

    # 将生成的图像哈希值随机分配给用户
    user_list = User.query.all()
    with tqdm(total=len(user_list), unit="items") as pbar:
        pbar.set_description('filling avatar hash in database')
        for i in range(len(user_list)):
            pbar.update(1)
            try:
                r = randint(0, len(md5_list) - 1)
                user_list[i].avatar_hash = md5_list[r]
                db.session.add(user_list[i])
                db.session.commit()
            except Exception as e:
                print("error happened when filling avatar hash in database: ", str(e))
                db.session.rollback()


def resize_img(source_path, des_path, height, width, max_img=None):
    assert os.path.exists(source_path)
    assert os.path.exists(des_path)
    if not max_img:
        max_img = 99999
    # 获取图像源全部的图像列表
    img_path = os.listdir(source_path)
    # 过滤，仅保留jpg与png格式
    img_path = filter(lambda x: os.path.splitext(x)[1] in (".jpg", ".png"), img_path)
    img_path = list(img_path)

    i = 0
    with tqdm(total=min(len(img_path), max_img), unit="items") as pbar:
        pbar.set_description('process img')
        for p in img_path:
            path = os.path.join(source_path, p)
            pbar.update(1)
            try:
                # 处理并保存图像
                img = Image.open(path)
                img.thumbnail((height, width))
                dest = os.path.join(des_path, str(i) + ".png")
                img.save(dest)
                i += 1
                if i >= max_img:
                    break
            except Exception as e:
                print(e)


if __name__ == "__main__":
    resize_img(r"D:\图片\手机保存\风景壁纸", r"D:\avatar", 256, 256, max_img=300)
    pass
