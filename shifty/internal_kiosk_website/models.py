from django.db import models

# Create your models here.
class Products(models.Model):
	name    = models.CharField(max_length=100)
	barcode = models.CharField(max_length=100)
	price   = models.IntegerField()
	amount  = models.IntegerField()
	object = models.Manager()

	class Meta:
		verbose_name_plural = "products"

	def __str__(self):
			return f"Product: {self.name}"