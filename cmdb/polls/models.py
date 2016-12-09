from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Host(models.Model):
    # position = models.ForeignKey(Position, on_delete=models.CASCADE)
    hostname =models.CharField(max_length=25,null=False,unique=True)
    ipaddress01 = models.CharField(max_length=16,null=False,unique=True)
    ipaddress02 = models.CharField(max_length=16,blank=True,null=True,unique=True)
    vip = models.CharField(max_length=16,blank=True,null=True,unique=True)
    remark = models.CharField(max_length=16,blank=True,null=True)

    def __str__(self):
        return self.hostname
    def get_host(self):
        host = []
        if self.ipaddress02:
            host = [self.hostname,self.ipaddress01,self.ipaddress02]
        else:
            host = [self.hostname,self.ipaddress01]
        if self.vip:
            host = [self.hostname,self.ipaddress01,self.vip]
        if self.ipaddress01 and self.ipaddress02 and self.vip:
            host = [self.hostname,self.ipaddress01,self.ipaddress02,self.vip]
        return host

@python_2_unicode_compatible
class Position(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    province = models.CharField(max_length=10,null=False)
    city = models.CharField(max_length=10,null=False)
    serverroom = models.CharField(max_length=10,null=False)
    cabinet = models.CharField(max_length=10,null=False)
    remark = models.CharField(max_length=20,blank=True,null=True)

    def __str__(self):
        position = []
        position = [self.province,self.city,self.serverroom,self.cabinet]
        return ''.join(position)




@python_2_unicode_compatible
class User(models.Model):
    # operate = models.ForeignKey(Operate)
    ROLE_CHOICE = (
        (0,'admin'),
        (1,'guest'),
    )
    role = models.IntegerField(choices=ROLE_CHOICE)
    name = models.CharField(max_length=10,unique=True,null=False)
    password = models.CharField(max_length=25,null=False)
    mail = models.CharField(max_length=25,unique=True,null=False)

    def __str__(self):
        return self.name

    def get_user(self):
        user = []
        user = [self.name,self.role,self.mail]
        return user

@python_2_unicode_compatible
class Operate(models.Model):
    host = models.ForeignKey(Host)
    user = models.ForeignKey(User)
    position = models.ForeignKey(Position)
    STATUS_CHOICE = (
        (0 ,'online'),
        (1 , 'offline'),
    )
    status = models.IntegerField(choices=STATUS_CHOICE)
    log = models.TextField(max_length=1000)
    timestamp = models.DateTimeField('Operate Time')
    remark = models.CharField(max_length=20,blank=True,null=True)

    def __str__(self):
        return self.log

    def get_host_status(self):
        return self.status




