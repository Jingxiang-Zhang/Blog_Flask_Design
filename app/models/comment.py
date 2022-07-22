from datetime import datetime
from markdown import markdown
import bleach
from flask import url_for
from app.exceptions import ValidationError
from .. import db


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean, comment="close the comment")
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        """
        用于数据库启用监听事件的回调处理函数，触发事件为Comment的body值发生变化。
        当监测到body值发生变化后，仅保留allowed_tags中的html标签，取出其余的标签
        并将其转化为html格式后赋值到body_html中
        :param target: body值发生变化时的post对象
        :param value: body变化后的值
        :param oldvalue:
        :param initiator:
        :return:
        """
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    # ---------------------  api接口相关功能，已经停止使用，因为不同版本api可能有不同需求  -----
    # ---------------------  因此所有的api功能均由api内部的service实现  ------------------------
    def to_json(self):
        """
        用于api的Comment数据访问
        :return:
        """
        json_comment = {
            'url': url_for('api/v1.0.get_comment', id=self.id),
            'post_url': url_for('api/v1.0.get_post', id=self.post_id),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author_url': url_for('api/v1.0.get_user', id=self.author_id),
        }
        return json_comment

    @staticmethod
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


db.event.listen(Comment.body, 'set', Comment.on_changed_body)
