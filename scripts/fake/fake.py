from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from app import db
from app.models.user import User, Follow
from app.models.post import Post
from app.models.comment import Comment

from random import randint, random
from tqdm import tqdm


def fake_users(count=100, en_cn=0.3, moderator_rate=0.2, commit=10):
    """
    生成虚假用户数据
    :param count: 生成假数据的条数
    :param en_cn: 英语与中文比例，默认0.3，生成数据的30%是英文数据
    :param moderator_rate: 拥有更高权限的用户的比例，默认0.2
    :param commit: 每生成多少条数据进行一次提交
    :return: None
    """
    assert type(count) == int
    assert type(en_cn) == float
    assert type(moderator_rate) == float
    assert type(commit) == int
    i = 0
    with tqdm(total=count, unit="items") as pbar:
        pbar.set_description('generate fake data [user]: ')
        while i < count // commit:
            try:
                generate_fake_user(commit, en_cn, moderator_rate)
            except Exception as e:
                print("error happened when generate fake users: ", e)
                db.session.rollback()
            pbar.update(commit)
            i += 1
        try:
            generate_fake_user(count % commit, en_cn, moderator_rate)
        except Exception as e:
            print("error happened when generate fake users: ", e)
            db.session.rollback()


def generate_fake_user(count, en_cn=0.3, moderator_rate=0.2):
    """
    :param count: 生成数量
    :param en_cn: 英语与中文比例，默认0.3，生成数据的30%是英文数据
    :param moderator_rate: 拥有更高权限的用户的比例，默认0.2
    :return:
    """
    i = 0
    fake_cn = Faker("zh_CN")
    fake_en = Faker("en_US")
    while i < count:
        fake = fake_cn if random() > en_cn else fake_en
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='password',
                 confirmed=True,
                 role_id=1 if random() > moderator_rate else 2,
                 name=fake.name(),
                 location=fake.city(),
                 about_me=fake.text(),
                 member_since=fake.past_date(),
                 last_seen=fake.past_date())
        db.session.add(u)
        i += 1
    if count != 0:
        db.session.commit()


def fake_posts(count_per_user=5, en_cn=0.3, poisson=True):
    """
    生成用户post数据
    :param count_per_user: 每个用户平均生成多少数据
    :param en_cn: 英语与中文比例，默认0.3，生成数据的30%是英文数据
    :param poisson: 用户平均发送post的数量服从泊松分布，数学期望为count_per_user
        需要用到numpy库，如果没有numpy，则固定生成5条数据
    :return:
    """
    assert type(count_per_user) == int
    assert type(en_cn) == float
    assert type(poisson) == bool

    user_list = User.query.all()
    # 为每一个用户生成一个发送post的条数，存于x列表中
    x = [count_per_user for i in range(len(user_list))]
    if poisson:
        try:
            import numpy as np
            x = np.random.poisson(lam=count_per_user, size=len(user_list))
        except:
            pass

    fake_cn = Faker("zh_CN")
    fake_en = Faker("en_US")

    with tqdm(total=len(user_list), unit="items") as pbar:
        pbar.set_description('generate fake data [post]: ')
        for i in range(len(user_list)):
            try:
                generate_fake_posts(user_list[i], x[i], fake_cn, fake_en, en_cn)
            except Exception as e:
                print("error happened when generate fake post: ", e)
                db.session.rollback()
            pbar.update(1)


def generate_fake_posts(user, count, fake_cn, fake_en, en_cn=0.3):
    """
    给定uid，生成5条post数据
    :param user: 用户
    :param count: 生成数量
    :param en_cn: 英语与中文比例，默认0.3，生成数据的30%是英文数据
    :return:
    """
    fake = fake_cn if random() > en_cn else fake_en
    for i in range(count):
        p = Post(body=fake.text(),
                 timestamp=fake.past_date(),
                 author=user)
        db.session.add(p)
    db.session.commit()


def fake_follows(follow_per_user=5, poisson=True):
    """
    生成假的follow数据
    :param follow_per_user: 平均每个用户follow多少个其他用户
    :param poisson: 用户平均follows数量服从泊松分布，数学期望为follow_per_user
        需要用到numpy库，如果没有numpy，则固定生成5follow
    :return:
    """
    assert type(follow_per_user) == int
    assert type(poisson) == bool

    user_list = User.query.all()
    # 为每一个用户生成一个发送post的条数，存于x列表中
    x = [follow_per_user for i in range(len(user_list))]
    if poisson:
        try:
            import numpy as np
            x = np.random.poisson(lam=follow_per_user, size=len(user_list))
        except Exception as e:
            pass

    fake = Faker()
    uid_list = [user.id for user in user_list]
    with tqdm(total=len(user_list), unit="items") as pbar:
        pbar.set_description('generate fake data [follow]: ')
        for i in range(len(user_list)):
            for j in range(x[i]):
                try:
                    # 对于每一个用户的每一次生成followed对象，都随机一个并进行尝试
                    follower = uid_list[i]
                    followed = uid_list[randint(0, len(user_list) - 1)]
                    p = Follow(follower_id=follower,
                               followed_id=followed,
                               timestamp=fake.past_date())
                    db.session.add(p)
                    db.session.commit()
                except Exception as e:
                    # print("error happened when generate fake post: ", e)
                    db.session.rollback()
                    j -= 1
            pbar.update(1)


def fake_comments(comment_rate=0.4, comment_per_post=5, poisson=True, en_cn=0.3):
    """
    生成假的comment评论数据
    :param comment_rate: 评论率，有0.4的概率进行评论
    :param comment_per_post: 每次评论的评论数量
    :param poisson: 是否符合泊松分布
    :param en_cn: 英语与中文比例，默认0.3，生成数据的30%是英文数据
    :return:
    """
    assert type(comment_rate) == float
    assert type(comment_per_post) == int
    assert type(poisson) == bool

    post_list = Post.query.all()
    x = [comment_per_post for i in range(len(post_list))]
    if poisson:
        try:
            import numpy as np
            x = np.random.poisson(lam=comment_per_post, size=len(post_list))
        except Exception as e:
            pass

    fake_cn = Faker("zh_CN")
    fake_en = Faker("en_US")

    user_list = db.session.query(User.id).all()
    user_list = [user[0] for user in user_list]

    with tqdm(total=len(post_list), unit="items") as pbar:
        pbar.set_description('generate fake data [post]: ')
        for i in range(len(post_list)):
            if random() > comment_rate:
                pbar.update(1)
                continue
            try:
                generate_fake_comments(post_list[i], x[i], fake_cn, fake_en, user_list, en_cn)
            except Exception as e:
                print("error happened when generate fake comments: ", e)
                db.session.rollback()
            pbar.update(1)


def generate_fake_comments(post, count, fake_cn, fake_en, user_list, en_cn=0.3):
    """
    给定uid，生成post数据
    :param post: post对象
    :param count: 生成数量
    :param en_cn: 英语与中文比例，默认0.3，生成数据的30%是英文数据
    :return:
    """
    fake = fake_cn if random() > en_cn else fake_en
    user_len = len(user_list)
    for i in range(count):
        random_author = randint(0, user_len - 1)
        p = Comment(body=fake.text(),
                    timestamp=fake.past_date(),
                    post=post,
                    author_id=user_list[random_author])
        db.session.add(p)
    db.session.commit()
