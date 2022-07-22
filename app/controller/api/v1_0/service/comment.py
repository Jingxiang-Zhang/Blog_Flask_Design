from flask import url_for
from app.exceptions import ValidationError
from app.models.comment import Comment


def comment_info_to_json(comment):
    """
    用于api的Comment数据访问
    :return:
    """
    json_comment = {
        'url': url_for('api/v1.0.get_comment', id=comment.id),
        'post_url': url_for('api/v1.0.get_post', id=comment.post_id),
        'body': comment.body,
        'body_html': comment.body_html,
        'timestamp': comment.timestamp,
        'author_url': url_for('api/v1.0.get_user', id=comment.author_id),
    }
    return json_comment


def from_json(json_comment):
    """
    从Comment的json数据中取出body
    :param json_post:
    :return:
    """
    body = json_comment.get('body')
    if body is None or body == '':
        raise ValidationError('comment does not have a body')
    return Comment(body=body)
