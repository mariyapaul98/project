from django.db import models

#user_login,user_details,service_master,service_order,service_payment,service_offers

# Create your models here.
class user_login(models.Model):
    uname = models.CharField(max_length=100)
    passwd = models.CharField(max_length=25)
    u_type = models.CharField(max_length=10)

    def __str__(self):
        return self.uname

class user_details(models.Model):
    user_id = models.IntegerField()
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=200)
    gender = models.CharField(max_length=25)
    age = models.IntegerField()
    addr = models.CharField(max_length=500)
    pin = models.IntegerField()
    contact = models.IntegerField()
    email = models.CharField(max_length=25)

    def __str__(self):
        return self.fname


class service_master(models.Model):
    name  = models.CharField(max_length=50)
    description  = models.CharField(max_length=500)
    qty  = models.CharField(max_length=50)
    price  = models.CharField(max_length=50)
    pic = models.CharField(max_length=500)
    dt = models.CharField(max_length=50)
    tm = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

class service_order(models.Model):
    user_id = models.IntegerField()
    service_id = models.IntegerField()
    dt  = models.CharField(max_length=50)
    tm  = models.CharField(max_length=50)
    remarks = models.CharField(max_length=50)
    bdt = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

class service_payment(models.Model):
    user_id = models.IntegerField()
    service_id = models.IntegerField()
    amt = models.CharField(max_length=50)
    card_no = models.CharField(max_length=50)
    cvv  = models.CharField(max_length=50)
    dt  = models.CharField(max_length=50)
    tm  = models.CharField(max_length=50)
    status = models.CharField(max_length=50)


class service_offers(models.Model):
    pic = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    dt = models.CharField(max_length=50)
    tm = models.CharField(max_length=50)
    status = models.CharField(max_length=50)