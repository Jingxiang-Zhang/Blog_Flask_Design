from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth_blueprint
from app import db
from app.models.user import User
from app.email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm,\
    PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm


@auth_blueprint.before_app_request
def before_request():
    """
    在每次请求之前，判断用户的登录情况，未登录状态下只允许访问部分页面
    :return:
    """
    if current_user.is_authenticated:
        current_user.ping()  # 调用了models中的user类中的ping函数
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth_blueprint.route('/unconfirmed')
def unconfirmed():
    """
    未授权返回的页面
    :return:
    """
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('routes/auth/unconfirmed.html')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """
    用户登录页面
    :return:
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid email or password.')
    return render_template('routes/auth/login.html', form=form)


@auth_blueprint.route('/logout')
@login_required
def logout():
    """
    用户登出界面
    :return:
    """
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """
    用户注册界面
    :return:
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(),
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'routes/auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('routes/auth/register.html', form=form)


@auth_blueprint.route('/confirm/<token>')
@login_required
def confirm(token):
    """
    激活邮箱的路径
    :param token:
    :return:
    """
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth_blueprint.route('/confirm')
@login_required
def resend_confirmation():
    """
    用于重新发送确认邮件
    :return:
    """
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'routes/auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth_blueprint.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """
    用于修改密码
    :return:
    """
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("routes/auth/change_password.html", form=form)


@auth_blueprint.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    """
    用于忘记密码后用邮箱发送重置密码的邮件
    :return:
    """
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'routes/auth/email/reset_password',
                       user=user, token=token)
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('routes/auth/reset_password.html', form=form)


@auth_blueprint.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    """
    用于重置密码界面密码的接收
    :param token:
    :return:
    """
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('routes/auth/reset_password.html', form=form)


@auth_blueprint.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    """用于更换邮箱"""
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'routes/auth/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("routes/auth/change_email.html", form=form)


@auth_blueprint.route('/change_email/<token>')
@login_required
def change_email(token):
    """
    用于更换邮箱时候的邮箱token的接收
    """
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('main.index'))
