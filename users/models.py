from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserBankAccount(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='account')
    account_no=models.IntegerField()
    balance=models.DecimalField(default=10,max_digits=12,decimal_places=2)
    def __str__(self):
        return str(self.account_no)

class Deposite(models.Model):
    account=models.ForeignKey(UserBankAccount,related_name='acount',on_delete=models.CASCADE)
    amount=models.IntegerField()
    def __str__(self):
        return str(self.amount)