from django.db import models

class Pay(models.Model):
    merchant = models.TextField()
    sum = models.TextField()
    comment = models.TextField()
    status = models.BooleanField()

    def __str__(self):
        return f'Pay {self.id} by {self.merchant}'
    
class Wallet(models.Model):
    merchant = models.TextField()
    wallet = models.TextField()

    def __str__(self):
        return f'Merchant: {self.merchant}'
