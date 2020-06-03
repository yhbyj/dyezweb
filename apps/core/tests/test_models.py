# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/25 7:26'

from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from core import models


def sample_user(mobile='15257911111', password='123456'):
    """创建一个用户实例"""
    return get_user_model().objects.create_user(mobile, password)


class UserAppModelTests(TestCase):
    """测试类：自定义用户模块的数据模型"""

    def test_create_user_with_mobile_phone_number_successful(self):
        """测试：用移动电话号码创建用户，成功"""
        mobile = '15257911111'
        password = '123456'
        user = get_user_model().objects.create_user(
            mobile=mobile,
            password=password
        )

        self.assertEqual(user.mobile, mobile)
        self.assertTrue(user.check_password(password))

    def test_new_user_invalid_mobile(self):
        """测试：创建新用户时，没有用户名，抛出异常"""
        mobile = None
        password = '123456'
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                mobile=mobile,
                password=password
            )

    def test_create_new_superuser(self):
        """测试：创建超级用户，成功"""
        mobile = '15257999999'
        password = '123456'
        user = get_user_model().objects.create_superuser(
            mobile=mobile,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_sms_code_successful(self):
        """测试：创建短信验证码，成功"""
        mobile = '15257911111'
        code = '1234'
        sms_code = models.SmsCode.objects.create(
            mobile=mobile,
            code=code
        )

        self.assertEqual(sms_code.mobile, mobile)
        self.assertEqual(sms_code.code, code)

    def test_sms_code_str(self):
        """测试：返回短信验证码对象的字符串表示，成功"""
        sms_code = models.SmsCode.objects.create(
            mobile='15257911111',
            code='123456'
        )

        self.assertEqual(str(sms_code), sms_code.code)


class RecipeAppModelTests(TestCase):
    """测试类：recipe模块的数据模型"""

    def test_tag_str(self):
        """测试：返回标签对象的字符串表示，成功"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='超人'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom source',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_image_field(self, mock_uuid):
        """Test that images are saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)


def sample_clazz():
    """返回一个班级对象"""
    return models.Clazz.objects.create(
        title='测试班级'
    )


def sample_major_category():
    """返回一个专业类别对象"""
    return models.MajorCategory.objects.create(
        name='测试专业类别'
    )


def sample_major(category=None):
    """返回一个专业对象"""
    if category is None:
        category = sample_major_category()
    return models.Major.objects.create(
        name='测试专业',
        category=category
    )


class StudentAppModelTests(TestCase):
    """学生模块的数据模型测试"""

    def test_clazz_str(self):
        """测试：班级对象字符串展示"""
        clazz = sample_clazz()
        self.assertEqual(str(clazz), clazz.title)

    def test_major_category_str(self):
        """测试：专业类别对象字符串展示"""
        major_category = sample_major_category()
        self.assertEqual(str(major_category), major_category.name)

    def test_major_str(self):
        """测试：专业对象字符串展示"""
        major = sample_major()
        self.assertEqual(str(major), major.name)

    def test_student_str(self):
        """测试：学生对象字符串展示"""
        major = sample_major()
        clazz = sample_clazz()
        student = models.Student.objects.create(
            name='测试学生',
            major=major,
            clazz=clazz
        )
        self.assertEqual(str(student), student.name)

    def test_admission_str(self):
        """测试：入学报名对象字符串展示"""
        admission = models.Admission.objects.create(
            name='测试入学报名',
            user=sample_user()
        )
        self.assertEqual(str(admission), admission.name)
