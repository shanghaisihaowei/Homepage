
from utils import get_code
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings


from django.template import Context, loader
from utils import HomePage_logging
logger = HomePage_logging.get_logger()
def send_emails(type_code, message, email, sendtype,lang='zh-hans'):
    """
    发送邮件验证码

    :param type_code: 验证码缓存
    :param message: 描述信息
    :param email: 接受邮件的邮箱
    :param sendtype: 邮件类型
    :param lang: 邮件语言
    :return: True/False
    """
    email = str(email)


    verification_code = get_code.get_code()
    cache.set(type_code % email, verification_code, 60 * 30)  # 缓存时间30分钟。
    recipient_list = [email, ]
    to = []
    if sendtype == 1:  # 注册验证码
        if lang == 'zh-hans': # 发送中文验证码
            context = {
                'title1': '您正在注册GreaterWMS',
                'title2': '欢迎注册GreaterWMS，请将验证码填写到注册页面',
                'email': str(email),
                'code': str(verification_code)
            }
            subject = 'GreaterWMS社区'  # 标题
            # 发送的html模板的名称
            email_template_name = 'email_view.html'
            t = loader.get_template(email_template_name)
            html_message = t.render(context)
            result = send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, html_message=html_message)
        else:
            context = {
                'title1': 'You are registering for GreaterWMS',
                'title2': """Welcome to register for GreaterWMS, please fill
                             in the verification code on the registration
                             page.""",
                'email': str(email),
                'code': str(verification_code)
            }
            subject = 'GreaterWMSCommunity'  # 标题
            # 发送的html模板的名称
            email_template_name = 'email_view_en-us.html'
            t = loader.get_template(email_template_name)
            html_message = t.render(context)
            result = send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, html_message=html_message)
        if result == 1:
            logger.warning("用户:%s 注册短信发送成功！" % email)
            return True  # 短信发送成功

        else:
            logger.warning("用户:%s 注册短信！" %email)
            return False

    elif sendtype == 2:  # 登录验证码
        if lang == 'zh-hans':  # 发送中文验证码
            context = {
                'title1': '您正在注册GreaterWMS',
                'title2': '欢迎注册GreaterWMS，请将验证码填写到注册页面',
                'email': str(email),
                'code':str(verification_code)
            }
            subject = 'GreaterWMS社区'  # 标题
            # 发送的html模板的名称
            email_template_name = 'email_view.html'
            t = loader.get_template(email_template_name)
            html_message = t.render(context)
            result = send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, html_message=html_message)
        else:
            context = {
                'title1': 'You are logging into GreaterWMS',
                'title2': """Welcome to logging into for GreaterWMS, please fill
                                         in the verification code on the registration
                                         page.""",
                'email': str(email),
                'code': str(verification_code)
            }

            subject = 'GreaterWMSCommunity'  # 标题
            # 发送的html模板的名称
            email_template_name = 'email_view_en-us.html'
            t = loader.get_template(email_template_name)
            html_message = t.render(context)
            result = send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, html_message=html_message)
        if result == 1:
            logger.warning("用户:%s 登录短信发送成功！" % email)
            return True  # 短信发送成功
        else:
            logger.warning("用户:%s 登录短信发送失败！" % email)
            return False

    elif sendtype == 3:  # 修改密码验证码
        if lang == 'zh-hans':  # 发送中文验证码
            context = {
                'title1': '您正在重置密码',
                'title2': '欢迎登录GreaterWMS，请将验证码填写到修改密码页面',
                'email': str(email),
                'code': str(verification_code)
            }
            subject = 'GreaterWMS社区'  # 标题
            # 发送的html模板的名称
            email_template_name = 'email_view.html'
            t = loader.get_template(email_template_name)
            html_message = t.render(context)
            result = send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, html_message=html_message)
        else:
            context = {
                'title1': 'You are resetting the GreaterWMS password',
                'title2': """Welcome to register for GreaterWMS, please fill
                                                    in the verification code on the registration
                                                    page.""",
                'email': str(email),
                'code': str(verification_code)
            }
            subject = 'GreaterWMSCommunity'  # 标题
            # 发送的html模板的名称
            email_template_name = 'email_view_en-us.html'
            t = loader.get_template(email_template_name)
            html_message = t.render(context)
            result = send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, html_message=html_message)
        if result == 1:
            logger.warning("用户:%s修改密码短信发送成功！" % email)
            return True  # 短信发送成功
        else:
            logger.warning("用户:%s修改密码短信发送失败！" % email)
            return False

    elif sendtype == 4:  # 校验支付宝账户
        if lang == 'zh-hans':  # 发送中文验证码
            context = {
                'title1': '您正在添加提现账号',
                'title2': '欢迎使用GreaterWMS，请将验证码填写添加账号邮箱验证框',
                'email': str(email),
                'code': str(verification_code)
            }
            subject = 'GreaterWMS社区'  # 标题
            # 发送的html模板的名称
            email_template_name = 'email_view.html'
            t = loader.get_template(email_template_name)
            html_message = t.render(context)
            result = send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, html_message=html_message)
        else:
            context = {
                'title1': 'You are adding Withdrawal account.',
                'title2': """Welcome to greaterwms. Please fill in the verification code and add it to the account email verification box""",
                'email': str(email),
                'code': str(verification_code)
            }
            subject = 'GreaterWMSCommunity'  # 标题
            # 发送的html模板的名称
            email_template_name = 'email_view_en-us.html'
            t = loader.get_template(email_template_name)
            html_message = t.render(context)
            result = send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, html_message=html_message)
        if result == 1:
            logger.warning("用户:%s添加支付宝账户短信发送成功！" % email)
            return True  # 短信发送成功
        else:
            logger.warning("用户:%s添加支付宝账户短信发送失败！" % email)
            return False





def send_company_feedback_email(name,you_emeil,leave_word,options):

    subject = 'GreaterWMS官方网站'
    if options == 0:  # 有关网站的建议

        email=settings.PRODUCT_MANAGER_EMAIL
        message='有关网站的建议'
        recipient_list = [email, ]
        html_message = "<h1>产品经理您好！用户姓名为：%s 联系邮箱为: %s, 给您留言:%s <br/>" % (name,you_emeil,leave_word)
        result = send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, html_message=html_message)
        if result == 1:
            logger.warning("用户:%s给产品经理留言成功！" % email)
            return True  # 短信发送成功
        else:
            logger.warning("用户:%s给产品经理留言失败！" % email)
            return False

    elif options == 1:  # 对产品的建议或问题
        email=settings.PRODUCT_MANAGER_EMAIL
        message='对产品的建议或问题'
        recipient_list = [email, ]
        html_message = "<h1>产品经理您好！用户姓名为：%s 联系邮箱为: %s , 给您留言:%s <br/>" % (name,you_emeil,leave_word)
        result = send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, html_message=html_message)
        if result == 1:
            logger.warning("用户:%s给产品经理留言成功" % email)
            return True  # 短信发送成功
        else:
            logger.warning("用户:%s给产品经理留言失败！" % email)
            return False

    elif options == 2:  # 人才招聘
        email=settings.PERSONNEL_MANAGER_EMAIL
        message='人才招聘'
        recipient_list = [email, ]
        html_message = "<h1>招聘经理您好！用户姓名为：%s 联系邮箱为: %s, 给您留言:%s <br/>" % (name,you_emeil,leave_word)
        result = send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, html_message=html_message)
        if result == 1:
            logger.warning("用户:%s给人事经理留言成功！" % email)
            return True  # 短信发送成功
        else:
            logger.warning("用户:%s给人事经理留言失败！" % email)
            return False

    if options == 3:  # 商务合作
        email=settings.MARKETING_MANAGER_EMAIL
        message='商务合作'
        recipient_list = [email, ]
        html_message = "<h1>市场经理您好！用户姓名为：%s 联系邮箱为: %s , 给您留言:%s <br/>" % (name,you_emeil,leave_word)
        result = send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, html_message=html_message)
        if result == 1:
            logger.warning("用户:%s给市场经理留言成功！" % email)
            return True  # 短信发送成功
        else:
            logger.warning("用户:%s给市场经理留言失败！" % email)
            return False

    if options == 4:  # 其他
        email=settings.PUBLIC_EMAIL
        message='其他'
        recipient_list = [email, ]
        html_message = "<h1>市场经理您好！用户姓名为：%s 联系邮箱为: %s , 给您留言:%s <br/>" % (name,you_emeil,leave_word)
        result = send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, html_message=html_message)
        if result == 1:
            logger.warning("用户:%s给市场经理留言成功！" % email)
            return True  # 短信发送成功
        else:
            logger.warning("用户:%s给市场经理留言失败！" % email)
            return False


def server_exception_message(details):
    subject = 'GreaterWMS官方网站服务器邮件'
    email = settings.PUBLIC_EMAIL
    message = '服务器邮件'
    recipient_list = [email, ]
    html_message = "<h1>开发运维人员您好：服务器邮件：%s<br/>" % (details)
    result = send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, html_message=html_message)
    if result == 1:
        logger.warning("服务器给公用邮箱%s 发送邮件成功！--->发送的信息是%s" % (email,details))
        return True  # 短信发送成功
    else:
        logger.warning("用户:%s给市场经理留言失败！" % email)
        return False