from django.contrib import admin

# Register your models here.

from . import models
#name:zlx    passw:123456
admin.site.register(models.User)
admin.site.register(models.Itemsss)
admin.site.register(models.itrecord)
admin.site.register(models.shopcars)
