from .. import db


class Permission:
    """
    用户权限类别
    """
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, comment="role name")
    default = db.Column(db.Boolean, default=False, index=True, comment="whether user role is default")
    permissions = db.Column(db.Integer, comment="user permissions")
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        """
        数据库初始化的时候插入不同的角色类型
        :return:
        """
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        """
        给某角色添加权限
        :param perm:
        :return:
        """
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        """
        给某角色减少权限
        :param perm:
        :return:
        """
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        """
        清空角色权限
        :return:
        """
        self.permissions = 0

    def has_permission(self, perm):
        """
        判断用户是否有某项权限
        :param perm:
        :return:
        """
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name
