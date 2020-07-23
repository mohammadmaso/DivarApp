from django.contrib import admin
from .models import Announcement, Car, SedanCar, HeavyCar, Commercial, office, Industrial, ApartmantBuy,ApartmantRent, OldProperty, villaBuy, villaRent,Booth

admin.site.register(SedanCar)
admin.site.register(HeavyCar)
admin.site.register(Car)
admin.site.register(Commercial)
admin.site.register(office)
admin.site.register(Industrial)
admin.site.register(ApartmantBuy)
admin.site.register(ApartmantRent)
admin.site.register(villaBuy)
admin.site.register(villaRent)
admin.site.register(OldProperty)
admin.site.register(Booth)
