import os
import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

from utils.db.base_model import BaseModel
from utils.db.validation import check_id_card_no


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/recipe/', filename)


class UserManager(BaseUserManager):
    """自定义用户模型管理类"""

    def create_user(self, mobile, password=None, **extra_fields):
        """创建和保存一个新用户"""
        if not mobile:
            raise ValueError('用户必须有一个有效的手机号码')
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, mobile, password):
        """创建一个超级用户"""
        user = self.create_user(mobile, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# 模型已经迁移建表,并且表中已经有数据之后,再给表/模型新增字段时,必须给默认值或可以为空,不然迁移就报错
class User(AbstractBaseUser, PermissionsMixin):
    """自定义用户模型，mobile 替代 username"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号码')
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    email = models.EmailField(max_length=255, null=True, blank=True, verbose_name='电子邮箱')
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')
    is_active = models.BooleanField(default=True, verbose_name='激活状态')
    is_staff = models.BooleanField(default=False, verbose_name='员工状态')


    USERNAME_FIELD = 'mobile'

    objects = UserManager()

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """Tag to be used for a recipe"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used for a recipe"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title


class SmsCode(models.Model):
    """
    短信验证码类
    """
    mobile = models.CharField(max_length=11, verbose_name='手机号码')
    code = models.CharField(max_length=10, verbose_name='短信验证码')
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '短信验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


class Student(BaseModel):
    """
    学生模型类
    """
    gender_choices = (
        (0, '男'),
        (1, '女'),
    )
    status_choices = (
        (0, '下线'),
        (1, '上线'),
    )
    name = models.CharField(max_length=50, verbose_name='姓名')
    # gender = models.CharField(max_length=10, default='男', choices=(("男", "男"), ("女", "女")), verbose_name='性别')
    gender = models.SmallIntegerField(default=0, choices=gender_choices, verbose_name='性别')
    # age = models.IntegerField(default=0, verbose_name='年龄')
    status = models.SmallIntegerField(default=1, choices=status_choices, verbose_name='学生状态')
    clazz = models.ForeignKey('Clazz', on_delete=models.CASCADE, verbose_name='班级')
    major = models.ForeignKey('Major', on_delete=models.CASCADE, verbose_name='专业')

    class Meta:
        verbose_name = "学生"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Clazz(BaseModel):
    """
    班级模型类
    """
    status_choices = (
        (0, '下线'),
        (1, '上线'),
    )
    title = models.CharField(max_length=50, verbose_name='名称')
    status = models.SmallIntegerField(default=1, choices=status_choices, verbose_name='班级状态')

    class Meta:
        db_table = 'tb_clazz'
        verbose_name = "班级"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class MajorCategory(BaseModel):
    """
    专业类别模型类
    """
    CATEGORY_TYPE = (
        (1, "一级类别"),
        (2, "二级类别"),
    )
    name = models.CharField(max_length=50, verbose_name='专业类别')
    desc = models.TextField(default="", verbose_name="类别描述")
    # 设置目录树的级别
    category_type = models.SmallIntegerField(default=2, choices=CATEGORY_TYPE, verbose_name="类别级别")
    # 设置models有一个指向自己的外键
    parent_category = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, verbose_name="父类别",
                                        related_name="sub_cat")

    class Meta:
        verbose_name = "专业类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        title = '{}--{}'.format(self.parent_category, self.name)
        title = title.replace('None--', '')
        return title


class Major(BaseModel):
    """
    专业模型类
    """
    status_choices = (
        (0, '下线'),
        (1, '上线'),
    )
    # todo
    # 专业对应的类别应该是二级类别，不能对应一级类别，如何解决？
    category = models.ForeignKey(MajorCategory, on_delete=models.CASCADE, verbose_name="专业类别")
    short_code = models.CharField(max_length=2, verbose_name="专业编号")
    name = models.CharField(max_length=50, verbose_name='专业名称')
    status = models.SmallIntegerField(default=1, choices=status_choices, verbose_name='专业状态')
    quota = models.IntegerField(default=35,  verbose_name='招生人数')
    code = models.CharField(max_length=6, null=True, blank=True, verbose_name="专业代码")

    class Meta:
        verbose_name = "专业"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Guardian(BaseModel):
    """
    监护人模型类
    """
    name = models.CharField(max_length=50, verbose_name='姓名')

    class Meta:
        verbose_name = '监护人'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GuardianAddress(BaseModel):
    """
    监护人地址模型类
    """
    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE, related_name='addresses', verbose_name='监护人')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province_addresses',
                                 verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_addresses',
                                 verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
    email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='电子邮箱')
    # 邮政编码
    zip_code = models.CharField(max_length=6, verbose_name='邮政编码')

    class Meta:
        verbose_name = '监护人地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']


class Admission(BaseModel):
    """入学申请（报名）模型类"""
    # 性别选项
    SEX_CHOICES = (
        (0, "男"),
        (1, "女")
    )
    # 户口性质选项
    HUKOU_CHOICES = (
        (0, "农"),
        (1, "非农")
    )
    # 民族选项（Ethnicity）
    NATIONALITY_CHOICES = (
        (0, "汉族"),
        (1, "蒙古族"),
        (2, "回族"),
        (3, "藏族"),
        (4, "维吾尔族"),
        (5, "苗族"),
        (6, "彝族"),
        (7, "壮族"),
        (8, "布依族"),
        (9, "朝鲜族"),
        (10, "满族"),
        (11, "侗族"),
        (12, "瑶族"),
        (13, "白族"),
        (14, "土家族"),
        (15, "哈尼族"),
        (16, "哈萨克族"),
        (17, "傣族"),
        (18, "黎族"),
        (19, "僳僳族"),
        (20, "佤族"),
        (21, "畲族"),
        (22, "高山族"),
        (23, "拉祜族"),
        (24, "水族"),
        (25, "东乡族"),
        (26, "纳西族"),
        (27, "景颇族"),
        (28, "柯尔克孜族"),
        (29, "土族"),
        (30, "达斡尔族"),
        (31, "仫佬族"),
        (32, "羌族"),
        (33, "布朗族"),
        (34, "撒拉族"),
        (35, "毛南族"),
        (36, "仡佬族"),
        (37, "锡伯族"),
        (38, "阿昌族"),
        (39, "普米族"),
        (40, "塔吉克族"),
        (41, "怒族"),
        (42, "乌孜别克族"),
        (43, "俄罗斯族"),
        (44, "鄂温克族"),
        (45, "德昂族"),
        (46, "保安族"),
        (47, "裕固族"),
        (48, "京族"),
        (49, "塔塔尔族"),
        (50, "独龙族"),
        (51, "鄂伦春族"),
        (52, "赫哲族"),
        (53, "门巴族"),
        (54, "珞巴族"),
        (55, "基诺族")
    )
    # 政治面貌选项
    POLITICAL_STATUS_CHOICES = (
        (0, "群众"),
        (1, "团员")
    )
    # 健康状况选项
    HEALTH_STATUS_CHOICES = (
        (0, "健康或良好"),
        (1, "一般或较弱")
    )
    # 学生来源选项
    ORIGIN_CHOICES = (
        (0, "应届"),
        (1, "往届")
    )
    # 初中毕业学校选项
    GRADUATE_SCHOOL_CHOICES = (
        (0, "安恬初中"),
        (1, "八达中小学"),
        (2, "春蕾学校"),
        (3, "大联初级中学　"),
        (4, "东江镇中"),
        (5, "东阳市横店第二初级中学"),
        (6, "东阳市横店第三初级中学　"),
        (7, "东阳市横店镇爱心学校"),
        (8, "防军初级中学"),
        (9, "歌山一中"),
        (10, "郭宅初中"),
        (11, "横店镇第一初级中学"),
        (12, "湖溪镇中"),
        (13, "虎鹿镇初级中学"),
        (14, "画水镇初级中学"),
        (15, "画溪初中"),
        (16, "怀鲁初中"),
        (17, "槐堂初中"),
        (18, "李宅初中"),
        (19, "六石街道初级中学"),
        (20, "马宅初中"),
        (21, "南马镇初级中学"),
        (22, "南溪初级中学"),
        (23, "千祥初级中学"),
        (24, "三单初中"),
        (25, "三联初中"),
        (26, "上村初级中学"),
        (27, "上卢初中"),
        (28, "唐表初中"),
        (29, "塘西初中"),
        (30, "亭塘初中"),
        (31, "巍山镇中"),
        (32, "吴宁二中"),
        (33, "吴宁三中"),
        (34, "吴宁四中"),
        (35, "吴宁一中"),
        (36, "象岗初中"),
        (37, "樟村初中"),
        (38, "佐村镇中")
    )
    # 初中毕业生姓名，最长字符50，必选项
    name = models.CharField(max_length=50, verbose_name='姓名')
    # 性别，默认值为(0, "男")
    sex = models.SmallIntegerField(default=0, choices=SEX_CHOICES, verbose_name='性别')
    # 户口性质，默认值为(0, "农")
    hukou = models.SmallIntegerField(default=0, choices=HUKOU_CHOICES, verbose_name='户口性质')
    # 民族性质，默认值为(0, "汉")
    nationality = models.SmallIntegerField(default=0, choices=NATIONALITY_CHOICES, verbose_name='民族')
    # 籍贯，默认值为“浙江东阳”
    native_place = models.CharField(default='浙江东阳', max_length=50, blank=True,  verbose_name='籍贯')
    # 身份证号码
    id_card_no = models.CharField(max_length=18, verbose_name='身份证号码',
                                  validators=[RegexValidator(r'\d{17}\w{1}', message='请输入正确格式的身份证号码！')])
    # 政治面貌，默认值为(0, "群众")
    political_status = models.SmallIntegerField(default=0, choices=POLITICAL_STATUS_CHOICES, verbose_name='政治面貌')
    # 健康状况，默认值为(0, "健康或良好")
    health_status = models.SmallIntegerField(default=0, choices=HEALTH_STATUS_CHOICES, verbose_name='健康状况')
    # 学生来源，默认值为(0, "应届")
    origin = models.SmallIntegerField(default=0, choices=ORIGIN_CHOICES, verbose_name='学生来源')
    # 家长姓名
    parent_name = models.CharField(max_length=50, verbose_name='家长姓名')
    # 初中毕业学校，默认值(0, "安恬初中")
    graduate_school = models.SmallIntegerField(default=0, choices=GRADUATE_SCHOOL_CHOICES, verbose_name='初中毕业学校')
    # 担任职务
    position = models.CharField(max_length=50, blank=True, verbose_name='担任职务')

    # 在新增加下列字段时，模型已经迁移建表,并且表中已经有数据
    # 因此必须给默认值或可以为空,不然迁移就报错！
    # 大专班1
    # major11 = models.CharField(max_length=50, null=True, blank=True, verbose_name='大专班1')
    # 大专班2
    # major12 = models.CharField(max_length=50, null=True, blank=True, verbose_name='大专班2')
    # 中职班1
    # major21 = models.CharField(max_length=50, null=True, blank=True, verbose_name='中职班1')
    # 中职班2
    # major22 = models.CharField(max_length=50, null=True, blank=True, verbose_name='中职班2')
    # 一个人可以报多个专业，一个专业可以被多个人申请
    majors = models.ManyToManyField(Major, through='AdmissionMajor',
                                    through_fields=('admission', 'major'), verbose_name='专业')

    # 用户
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='用户')
    # 填表人
    filler = models.CharField(max_length=50, null=True, blank=True, verbose_name='填表人')
    # 推荐人（教职工）
    adviser = models.CharField(max_length=50, null=True, blank=True, verbose_name='推荐人')
    # 家庭住址
    address = models.CharField(max_length=100, null=True, blank=True, verbose_name='家庭住址')
    # 邮政编码
    zip_code = models.CharField(max_length=6, null=True, blank=True, verbose_name='邮编',
                                validators=[RegexValidator(r'\d{6}', message='请输入正确格式的邮政编码！')])
    # 联系方式1
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号码',
                              validators=[RegexValidator(r'1[345678]\d{9}', message='请输入正确格式的手机号码！')])
    # 联系方式2
    telephone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='电话号码')
    # 预报名确认
    confirmed = models.BooleanField(default=False, verbose_name='预报名确认状态')
    # 确认文书
    confirmed_with = models.TextField(default='你已成功预报名，需网上报名时再次确认，优先录取。', max_length=200, verbose_name='确认文书')
    # 确认人
    confirmed_by = models.CharField(max_length=50, null=True, blank=True, verbose_name='确认人')
    # 确认日期
    confirmed_on = models.DateField(null=True, blank=True, verbose_name='确认日期')
    # 备注
    memo = models.TextField(max_length=200, null=True, blank=True, verbose_name='备注')

    class Meta:
        verbose_name = '入学申请（报名）'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def clean(self):
        """
        自定义数据验证
        :return:
        """
        # 验证身份证号码
        code, message = check_id_card_no(self.id_card_no)
        if code != 0:
            raise ValidationError(message)


class AdmissionMajor(BaseModel):
    """
    入学申请专业类：一个申请人可以申请多个专业，一个专业可以被多个人申请
    This is a many-to-many intermediary model
    """
    # 入学申请
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='admissions', verbose_name='入学申请')
    major = models.ForeignKey(Major, on_delete=models.CASCADE, related_name='majors', verbose_name='专业')

    class Meta:
        verbose_name = '入学申请专业'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}{}'.format(self.admission.name, self.major.name)


class Dormitory(BaseModel):
    """
    学生宿舍模型类
    """
    building_choices = (
        (6, '6号楼'),
        (7, '7号楼'),
        (8, '8号楼'),
    )
    # 寝室编号，必填项，如405
    short_code = models.CharField(max_length=3, verbose_name="寝室编号")
    # 学生自己起的名字，非必填项
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='寝室名称')
    beds = models.SmallIntegerField(default=10, verbose_name='床位数')
    with_bathroom = models.BooleanField(default=True, verbose_name='是否带卫生间')
    building = models.SmallIntegerField(default=7, choices=building_choices, verbose_name='所属楼栋')

    class Meta:
        verbose_name = '寝室'
        verbose_name_plural = verbose_name

    def __str__(self):
        title = '{}-{}'.format(self.building, self.short_code)
        title = title.replace('None-', '')
        return title


class ThreeCompetitionRuleCategory(BaseModel):
    """
    三项竞赛评分细则类别模型类
    """
    CATEGORY_TYPE = (
        (1, "一级类别"),
        (2, "二级类别"),
    )
    name = models.CharField(max_length=50, verbose_name='三项竞赛评分细则类别')
    desc = models.TextField(null=True, blank=True, verbose_name="类别描述")
    # 设置目录树的级别
    category_type = models.SmallIntegerField(default=2, choices=CATEGORY_TYPE, verbose_name="类别级别")
    # 设置models有一个指向自己的外键
    parent_category = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, verbose_name="父类别",
                                        related_name="sub_cat")

    class Meta:
        verbose_name = "三项竞赛评分细则类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        title = '{}--{}'.format(self.parent_category, self.name)
        title = title.replace('None--', '')
        return title


class ThreeCompetitionRule(BaseModel):
    """
    三项竞赛评分细则模型类
    """
    # 三项竞赛评分细则对应的类别应该是二级类别，不能对应一级类别，如何解决？
    category = models.ForeignKey(ThreeCompetitionRuleCategory, on_delete=models.CASCADE, verbose_name="三项竞赛评分细则类别")
    name = models.CharField(max_length=50, verbose_name='三项竞赛评分细则名称')
    code = models.CharField(max_length=6, null=True, blank=True, verbose_name="三项竞赛评分细则代码")
    desc = models.TextField(null=True, blank=True, verbose_name="三项竞赛评分细则描述")
    min = models.DecimalField(default=0.00, max_digits=3, decimal_places=2,  verbose_name='评分区间下限')
    max = models.DecimalField(default=5.00, max_digits=3, decimal_places=2, verbose_name='评分区间上限')

    class Meta:
        verbose_name = '三项竞赛评分细则'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ThreeCompetitionRuleOption(BaseModel):
    """
    三项竞赛评分细则选项模型类
    """
    rule = models.ForeignKey(ThreeCompetitionRule, on_delete=models.CASCADE, verbose_name="三项竞赛评分细则")
    name = models.CharField(max_length=50, verbose_name='选项名称')
    value = models.CharField(max_length=50, verbose_name='选项值')

    class Meta:
        verbose_name = '三项竞赛评分细则选项'
        verbose_name_plural = verbose_name

    def __str__(self):
        title = '{}--{}--{}'.format(self.rule, self.name, self.value)
        title = title.replace('None--', '')
        return title


class DormitoryCompetition(BaseModel):
    """
    寝室竞赛模型类
    """
    dormitory = models.ForeignKey(Dormitory, on_delete=models.CASCADE, verbose_name="寝室")
    option = models.ForeignKey(ThreeCompetitionRuleOption, on_delete=models.CASCADE, verbose_name="三项竞赛评分细则选项")
    score = models.DecimalField(default=0.00, max_digits=3, decimal_places=2, verbose_name='评分')
    is_minus = models.BooleanField(default=True, verbose_name='是否扣分')

    class Meta:
        verbose_name = '寝室竞赛'
        verbose_name_plural = verbose_name

    def __str__(self):
        title = '{}--{}'.format(self.dormitory,self.option)
        title = title.replace('None--', '')
        return title
