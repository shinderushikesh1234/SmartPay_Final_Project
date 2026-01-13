from django.db import models
from django.contrib.auth.models import User
class Merchant(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    store_name = models.CharField(max_length=100)
    upi_id = models.CharField(max_length=100,blank=True)
    qr_code = models.ImageField(upload_to='qrcodes/',blank=True,null=True)
    def __str__(self): return self.store_name
class Transaction(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchant,on_delete=models.CASCADE)
    amount = models.IntegerField()
    stripe_payment_id = models.CharField(max_length=200,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
