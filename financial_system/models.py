from django.db import models
from django.db.models import Sum
from django.utils import timezone


# from mptt.models import MPTTModel, TreeForeignKey


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.user_id, filename)


# def manager_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
#     return 'manager_{0}/{1}'.format(instance.manager.manager_id, filename)


class User(models.Model):
    # 用户信息表
    # 用户ID，
    user_id = models.AutoField(primary_key=True)
    # 用户名，用于显示和评论
    user_name = models.CharField(max_length=45)
    # 用户密码
    password = models.CharField(max_length=45)
    # 用户性别
    user_gender = models.CharField(max_length=5)
    # 用户电话号码，用于注册，联系
    phone_number = models.CharField(max_length=45)
    # 用户邮箱
    user_email = models.EmailField(unique=True)
    # 用户头像路径
    photo = models.ImageField(upload_to=user_directory_path, default='user-128.png')
    # 账户余额
    account_balance = models.FloatField(null=True, default=0)

    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '-'.join([self.user_name, self.phone_number])

    class Meta:
        db_table = 'user'


class Manager(models.Model):
    # 管理员信息表
    manager_id = models.AutoField(primary_key=True)
    # 管理员，用于显示和评论
    manager_name = models.CharField(max_length=45)
    # 管理员密码
    password = models.CharField(max_length=45)
    # 管理员电话号码，用于注册，联系
    phone_number = models.CharField(max_length=45)
    # 管理员头像路径
    photo_url = models.CharField(max_length=45)

    def __str__(self):
        return '-'.join([self.manager_id, self.phone_number])

    class Meta:
        db_table = 'manager'


class StockInfo(models.Model):
    # 股票信息表，记录股票系统中的股票信息
    # 股票ID，固定6位，PK
    stock_id = models.AutoField(primary_key=True)
    # 股票名称
    stock_name = models.CharField(max_length=45)
    # 股票发行时间
    issuance_time = models.CharField(max_length=45)
    # 股票昨日收盘价
    closing_price_y = models.FloatField(null=True)
    # 股票今日开盘价
    open_price_t = models.FloatField(null=True)
    # 股票类型，上证/深证
    stock_type = models.CharField(max_length=15, null=True)
    # 股票所在版块，科创、金融。。
    block = models.CharField(max_length=45, null=True)
    # 涨跌幅，用于筛选牛股推荐
    change_extent = models.FloatField(null=True)

    def __str__(self):
        return '-'.join([self.stock_id, self.stock_name])

    class Meta:
        db_table = 'stock_info'


class Watchlist(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    stock_id = models.ForeignKey(to=StockInfo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'watchlist'


class HistoryTrade(models.Model):
    TRADE_TYPE_CHOICES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]

    # 历史交易记录表
    # 交易ID，PK
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    # 交易股票ID，FK
    stock_id = models.ForeignKey(to=StockInfo, on_delete=models.CASCADE)
    # 交易价格
    trade_price = models.FloatField()
    # 成交股数
    trade_quantity = models.PositiveIntegerField()
    # 成交时间
    trade_dateTime = models.CharField(max_length=40)

    trade_type = models.CharField(max_length=4, choices=TRADE_TYPE_CHOICES, default='BUY')

    def __str__(self):
        return '-'.join([self.user_id.phone_number, self.stock_id])

    class Meta:
        db_table = 'history_trade'


class News(models.Model):
    # 新闻id
    news_id = models.AutoField(primary_key=True)

    # stock_id = models.ForeignKey(StockInfo, on_delete=models.SET_NULL, null=True)

    # 新闻标题
    title = models.CharField(max_length=100)
    # 新闻来源
    source = models.URLField(null=True)
    # 新闻内容
    content = models.TextField()
    # 发生时间
    news_dataTime = models.DateField(auto_now=True)

    def __str__(self):
        return '-'.join([str(self.news_id), self.title])

    class Meta:
        db_table = 'news'


class StockComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    # 评论标题
    title = models.CharField(max_length=50)
    # 评论内容
    content = models.TextField()
    # 发表时间
    comment_time = models.DateTimeField(auto_now=True)
    # 发起用户
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    # 关联股票
    stock_id = models.ForeignKey(to=StockInfo, on_delete=models.CASCADE)

    def __str__(self):
        return '-'.join([str(self.user_id), self.title])

    class Meta:
        db_table = 'stock_comment'


class CommentReply(models.Model):
    reply_id = models.AutoField(primary_key=True)
    # 所回复的评论的id
    comment_id = models.ForeignKey(to=StockComment, on_delete=models.CASCADE)

    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    # 所回复的评论的时间
    reply_time = models.DateTimeField(auto_now=True)
    # 回复内容
    content = models.TextField()

    def __str__(self):
        return '-'.join([str(self.reply_id)])

    class Meta:
        db_table = 'comment_reply'
        ordering = ['reply_time']


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback', null=True)
    email = models.EmailField(null=False, blank=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.email} - {self.title}"

    class Meta:
        db_table = 'feedback'
        ordering = ['created_at']


class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.user_name} - {'Read' if self.read else 'Unread'}"

    class Meta:
        db_table = 'user_notification'
        ordering = ['created_at']

# 可以用来做树级评论
# class Comment(MPTTModel):
#     stock_id = models.ForeignKey(
#         StockInfo,
#         on_delete=models.CASCADE,
#         related_name='comments'
#     )
#     user_id = models.ForeignKey(
#         UserTable,
#         on_delete=models.CASCADE,
#         related_name='comments'
#     )
#     # mptt树形结构可以参考
#     parent = TreeForeignKey(
#         'self',
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name='children'
#     )
#
#     # 记录二级评论回复给谁, str
#     reply_to = models.ForeignKey(
#         UserTable,
#         null=True,
#         blank=True,
#         on_delete=models.CASCADE,
#         related_name='replyers'
#     )
#
#     body = models.TextField(null=True)
#     created = models.DateTimeField(auto_now_add=True)
#
#     # 替换 Meta 为 MPTTMeta
#     # class Meta:
#     #     ordering = ('created',)
#
#     def __str__(self):
#         return self.body[:20]
#
#     class MPTTMeta:
#         order_insertion_by = ['created']