import random
import string
from django.db import models

class ReportDefinition(models.Model):
    name = models.CharField(max_length=255)
    query = models.TextField()
    query_id = models.CharField(max_length=5, unique=True, primary_key=True)  # Set as primary key
    visualization_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Updated on every save

    def save(self, *args, **kwargs):
        if not self.query_id:
            self.query_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'report_definition'    
    
class SaleOrder(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    product_name = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
