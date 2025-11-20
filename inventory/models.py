from django.db import models

class InventoryItem(models.Model):
    name = models.CharField(max_length=150)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=20, default="ml")  # ml, g, pcs
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
