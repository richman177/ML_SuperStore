from django.db import models 


class Store(models.Model): 
    category = models.CharField(max_length=100) 
    sub_category = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    segment = models.CharField(max_length=100) 
    ship_mode = models.CharField(max_length=100)
    discount = models.FloatField() 
    quantity = models.FloatField()
    month = models.IntegerField()
    dayofweek = models.IntegerField()
    predicted_sales = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.category} {self.sub_category} {self.region} {self.segment} {self.ship_mode}"
