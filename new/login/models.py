from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=10,unique=True)
    password = models.CharField(max_length=20,null=False)
    tel = models.CharField(max_length=11,unique=True)
    wx = models.CharField(max_length=11,unique=True)
    zfb = models.CharField(max_length=11,unique=True)
    addr1 = models.CharField(max_length=30,null=False)
    addr2 = models.CharField(max_length=30,null=False)
    
    def __str__(self):
        return self.name

class Itemsss(models.Model):
    item_id = models.IntegerField(unique=True)
    item_name = models.CharField(max_length=100)
    item_src = models.TextField(max_length=300,null=False)
    item_value = models.CharField(max_length=30,null=False)
    item_description = models.TextField(max_length=1000,null=False)

    
    def __str__(self):
        return str(self.item_id)

class itrecord(models.Model):  
    item_name = models.CharField(max_length=100,unique=True)
    item_r1 = models.FloatField(max_length=10,null=True)
    item_r2 = models.FloatField(max_length=10,null=True)
    item_r3 = models.FloatField(max_length=10,null=True)
    item_r4 = models.FloatField(max_length=10,null=True)
    item_r5 = models.FloatField(max_length=10,null=True)
    item_r6 = models.FloatField(max_length=10,null=True)
    item_r7 = models.FloatField(max_length=10,null=True)
    item_r8 = models.FloatField(max_length=10,null=True)
    item_r9 = models.FloatField(max_length=10,null=True)
    item_r10 = models.FloatField(max_length=10,null=True)

    def __str__(self):
        return self.item_name


class shopcars(models.Model):
    car_no = models.IntegerField(null=True)
    user_name = models.CharField(max_length=100,null=True)
    item_id = models.IntegerField(null=True)
    item_counter = models.IntegerField(null=True)
    item_value = models.CharField(max_length=30,null=False)
    item_money = models.CharField(max_length=30,null=False)

    def __str__(self):
        return str(self.car_no)
    


