
from django.db import models
from mapbox_location_field.models import LocationField
from django.utils import timezone
from django.conf import settings
import math




class Announcement(models.Model):
    TEHRAN_ZONES = [
        ('AKB','اکباتان'),
        ('VALI','ولی عصر'),
        ('CHTGR','چیتگر'),
        ('AGHD','اقدسیه'),
        ('ARG','آرژانتین'),
        ('OTHER','حومه شهر'),
        ('KSHV', 'بلوارکشاورز'),
    ]
    CITY = [
        ('yazd','یزد'),
        ('tehran','تهران'),

    ]
    subject = models.CharField(max_length=100, verbose_name='عنوان')
    detail = models.TextField(blank=True, verbose_name='توضیحات')
    is_chatActive = models.BooleanField(default=True, verbose_name='آیا چت فعال باشد؟')
    phone_number = models.CharField(max_length=12, verbose_name='شماره تلفن')
    pub_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to ='uploads/',null=True, blank=True, verbose_name='تصویر')
    zone = models.CharField(max_length=20 ,choices=TEHRAN_ZONES, default='OTHER', verbose_name='منطقه')
    city = models.CharField(max_length=20 ,choices=CITY, default='tehran', verbose_name='شهر')
    is_immediate = models.BooleanField(default=False, verbose_name='فوری')
    is_exchange = models.BooleanField(default=False, verbose_name='قابل معاوضه')
    location = LocationField(map_attrs={"center": [0,0], "marker_color": "blue"},null=True,blank=True, verbose_name='نقشه')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        default= 3
    )
    def whenpublished(self):
        now = timezone.now()

        diff= now - self.pub_date

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds

            if seconds == 1:
                return str(seconds) +  "ثانیه پیش"

            else:
                return str(seconds) + " ثانیه پیش"



        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " دقیقه پیش"

            else:
                return str(minutes) + " دقیقه پیش"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " ساعت پیش"

            else:
                return str(hours) + "ساعت پیش"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days

            if days == 1:
                return str(days) + " روز پیش"

            else:
                return str(days) + " روز پیش"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)


            if months == 1:
                return str(months) + " ماه پیش"

            else:
                return str(months) + "ماه پیش"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " سال پیش"

            else:
                return str(years) + " سال پیش"
    class Meta:
        abstract = True

class Car(Announcement):
    SELL_CHOICES = [
        ('sell','فروش'),
        ('rent','اجاره'),
        ('need','درخواستی')
    ]
    prod_year = models.PositiveSmallIntegerField(verbose_name='سال ساخت')
    sell_choice = models.CharField(max_length=20, choices= SELL_CHOICES, default='sell', verbose_name='نوع فروش')
    price = models.DecimalField(max_digits=20, decimal_places=3, verbose_name='قیمت')
    is_exchange = models.BooleanField(default=False, verbose_name='قابل معاوضه')
    function = models.IntegerField(default=0, verbose_name='کارکرد(کیلومتر)')

class SedanCar(Car):
    DOC_CHOICES = [
        ('singlePaper','تک برگی'),
        ('twoPaper','دوبرگی'),
        ('multiPaper','چندبرگی')
    ]
    BUY_CHOICES = [
        ('cash','نقدی'),
        ('semiCash','نقدی-قسطی'),
        ('lean','قسطی')
    ]
    GEARBOX_CHOICES = [
        ('auto','اتوماتیک'),
        ('handy','دستی'),
    ]
    BODY_CHOICES = [
        ('good','سالم'),
        ('bad','رنگ شده'),
    ]
    brand = models.CharField(max_length = 20 , null=True)
    car_model = models.CharField(max_length = 20, null=True)
    buy_type = models.CharField(max_length = 20 ,choices=BUY_CHOICES, default='cash',blank=True)
    body_state = models.CharField(max_length = 20 , choices=BODY_CHOICES, default='good',blank=True)
    gearbox_type = models.CharField(max_length = 20 , choices=GEARBOX_CHOICES, default='handy', blank=True)
    color = models.CharField(max_length = 20 , null=True)
    nstional_id = models.CharField(max_length = 20,null=True, blank=True)


class HeavyCar(Car):
    pass

class Property(Announcement):
    PUB_CHOICES = [
        ('person','شخص'),
        ('amlak', 'املاک'),
    ]
    SELL_CHOICES = [
        ('sell','فروش'),
        ('rent','اجاره'),
        ('need','درخواستی')
    ]
    sell_choice = models.CharField(max_length=20, choices= SELL_CHOICES, default='sell')
    area = models.IntegerField(default=0)
    publisher = models.CharField(max_length = 20 , choices=PUB_CHOICES)

class Apartmant(Property):
    room_num = models.IntegerField(default=0)
    year_of_build = models.IntegerField(default=0)
    floor = models.IntegerField(default=1)
    elevator = models.BooleanField(default=True)
    parking = models.BooleanField(default=True)
    depot = models.BooleanField(default=True)
    apartmant_Property = models.OneToOneField(Property, on_delete=models.CASCADE, parent_link=True)
    class Meta:
        abstract = True


class ApartmantRent(Apartmant):
    deposit_price = models.DecimalField(max_digits=20, decimal_places=3)
    rent_price = models.DecimalField(max_digits=20, decimal_places=3)


class ApartmantBuy(Apartmant):
    nstional_id = models.CharField(max_length = 20,null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=3)

class OldProperty(Property):
    price = models.DecimalField(max_digits=20, decimal_places=3)


class Villa(Apartmant):
    balkony = models.BooleanField(default=True)
    class Meta:
        abstract = True

class villaRent(Villa):
    deposit_price = models.DecimalField(max_digits=20, decimal_places=3)
    rent_price = models.DecimalField(max_digits=20, decimal_places=3)

class villaBuy(Villa):
    nstional_id = models.CharField(max_length = 20,null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=3)


class Commercial(Property):
    price = models.DecimalField(max_digits=20, decimal_places=3)
    nstional_id = models.CharField(max_length = 20,null=True, blank=True)
    is_haveDoc = models.BooleanField(default=True)
    commerical_Property = models.OneToOneField(Property, on_delete=models.CASCADE, parent_link=True)

class office(Apartmant, Commercial):
    pass

class Booth(Commercial):
    room_num = models.IntegerField(default=0)
    year_of_build = models.IntegerField(default=0)
class Industrial(Booth):
    pass
