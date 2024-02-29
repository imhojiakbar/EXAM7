from django.db import models

from apps.shared.models import AbstractModel
from apps.users.models import User


# Create your models here.
class Category(AbstractModel):
    name = models.CharField(max_length=128)


class Product(AbstractModel):
    title = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=1000000000, decimal_places=2)
    ends_in = models.DateField()
    owner = models.CharField(max_length=128)
    like_count = models.IntegerField(default=0)


class ProductLike(AbstractModel):
    user = models.ForeignKey(User, models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE)

    def __str__(self):
        return f"{self.product}-{self.user}"

