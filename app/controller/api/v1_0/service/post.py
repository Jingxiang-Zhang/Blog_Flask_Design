from flask import url_for
from app.models.post import Post
from app.exceptions import ValidationError


def post_info_to_json(post):
    """
    用于api的post数据访问
    :return:
    """
    json_post = {
        'url': url_for('api/v1.0.get_post', id=post.id),
        'body': post.body,
        'body_html': post.body_html,
        'timestamp': post.timestamp,
        'author_url': url_for('api/v1.0.get_user', id=post.author_id),
        'comments_url': url_for('api/v1.0.get_post_comments', id=post.id),
        'comment_count': post.comments.count()
    }
    return json_post


def from_json(json_post):
    """
    从post的json数据中取出body
    :param json_post:
    :return:
    """
    body = json_post.get('body')
    if body is None or body == '':
        raise ValidationError('post does not have a body')
    return Post(body=body)
