from django.db import models
import datetime
import os

# Create your models here.

def get_file_path(request, filename):
    orginal_filename = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s"% (nowTime,orginal_filename)
    return os.path.join('image/', filename)

class Login(models.Model):
    logid=models.AutoField(primary_key=True)
    username=models.CharField(max_length=100,unique=True,null=False,blank=False)
    password=models.CharField(max_length=100,null=False,blank=False)
    role=models.CharField(max_length=20,null=False)

    def __str__(self):
        return self.username
    

class User(models.Model):
    uid=models.AutoField(primary_key=True)
    fname=models.CharField(max_length=100,null=False,default=None)
    email=models.CharField(max_length=100,unique=True,null=False)
    dob=models.CharField(max_length=100,null=False)
    phone=models.BigIntegerField()
    ustatus=models.CharField(max_length=100,null=False,default="waiting")
    login=models.ForeignKey(Login, on_delete=models.CASCADE,default=None)

    def __str__(self):
        return self.fname


class Staff(models.Model):
    sid=models.AutoField(primary_key=True)
    fname=models.CharField(max_length=100,null=False,default=None)
    email=models.CharField(max_length=100,unique=True,null=False)
    dob=models.CharField(max_length=100,null=False)
    phone=models.BigIntegerField()
    address=models.CharField(max_length=300,null=False)
    gender=models.CharField(max_length=20,null=False)
    image=models.ImageField(upload_to=get_file_path, height_field=None, width_field=None, max_length=None)
    login=models.ForeignKey(Login, on_delete=models.CASCADE,default=None)


    def __str__(self):
        return self.fname


class District(models.Model):
    did=models.AutoField(primary_key=True)
    dname=models.CharField(max_length=50,null=False,unique=True)


    def __str__(self):
        return self.dname



class Location(models.Model):
    lid=models.AutoField(primary_key=True)
    lname=models.CharField(max_length=100,null=False,unique=True)
    district=models.ForeignKey(District,on_delete=models.CASCADE)


    def __str__(self):
        return self.lname



class Route(models.Model):
    rid=models.AutoField(primary_key=True)
    fromlocation=models.CharField(max_length=100,null=False)
    tolocation=models.CharField(max_length=100,null=False)
    rmap=models.ImageField(upload_to=get_file_path)




class Bus(models.Model):
    bid=models.AutoField(primary_key=True)
    btype=models.CharField(max_length=100,null=False)
    bno=models.CharField(max_length=100,null=False,unique=True)
    seats=models.IntegerField()




class Bus_Schedule(models.Model):
    bsc_id=models.AutoField(primary_key=True)
    route=models.ForeignKey(Route, on_delete=models.CASCADE)
    deptime=models.CharField(max_length=100,null=False)
    arrivaltime=models.CharField(max_length=100,null=False)
    bus=models.ForeignKey(Bus, on_delete=models.CASCADE)


class Seat_Schedule(models.Model):
    seatid=models.AutoField(primary_key=True)
    schedule_date=models.CharField(max_length=100,null=False)
    bus_schedule=models.ForeignKey(Bus_Schedule, on_delete=models.CASCADE)
    available_seat=models.IntegerField()


class Staffallot(models.Model):
    allot_id=models.AutoField(primary_key=True)
    bus_schedule=models.ForeignKey(Bus_Schedule, on_delete=models.CASCADE)
    schedule_date=models.ForeignKey(Seat_Schedule, on_delete=models.CASCADE)
    staff=models.ForeignKey(Staff, on_delete=models.CASCADE)
    status=models.CharField(max_length=10,null=False)

class Ticketrate(models.Model):
    ticket_id=models.AutoField(primary_key=True)
    route=models.ForeignKey(Route, on_delete=models.CASCADE)
    adult=models.IntegerField()
    child=models.IntegerField()
    bustype=models.ForeignKey(Bus, on_delete=models.CASCADE)



class Bank(models.Model):
    card=models.IntegerField()
    expiry=models.CharField(max_length=30,default=None)
    cvv=models.IntegerField()
    balance=models.IntegerField()


class Ticket(models.Model):
    ticid=models.AutoField(primary_key=True)
    uname=models.ForeignKey(User, on_delete=models.CASCADE)
    date=models.ForeignKey(Seat_Schedule, on_delete=models.CASCADE)
    pas=models.IntegerField()
    adult=models.IntegerField()
    child=models.IntegerField()
    tot=models.IntegerField()
