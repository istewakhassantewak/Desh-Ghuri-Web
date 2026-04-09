



from django.db import models
from django.conf import settings
from bookings.models import Packages # Assuming Package model is in a 'tour' app

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null =True ,blank= True)
    package = models.ForeignKey(Packages, on_delete=models.CASCADE)
    guest_count = models.IntegerField(default=1,null=True,blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')  # Pending, Success, Failed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.package.title} - {self.status}"
