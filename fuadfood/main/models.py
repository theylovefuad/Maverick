from django.db import models
from accounts.forms import User
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    LABELS = (
        ('Best Selling Foods', 'Best Selling Foods'),
        ('New Food', 'New Food'),
    )   

    LABEL_COLOUR = (
        ('danger', 'danger'),
        ('success', 'success'),
        ('primary', 'primary'),
        ('info', 'info'),
        ('warning', 'warning'),
    )
    title = models.CharField(max_length=150)
    label = models.CharField(max_length=150, default='regular')
    description = models.CharField(max_length=250,blank=True)
    price = models.FloatField()
    pieces = models.IntegerField(default=6)
    instructions = models.CharField(max_length=250,default="Available")
    image = models.ImageField(default='default.png', upload_to='images')
    labels = models.CharField(max_length=25, choices=LABELS, blank=True)
    label_colour = models.CharField(max_length=15, choices=LABEL_COLOUR, blank=True)
    slug = models.SlugField(default="foods")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class OurDishes(models.Model):
    image = models.ImageField(upload_to="images") 
    title = models.CharField(max_length=150) 
    price = models.DecimalField(max_digits=1000, decimal_places=2)

class Order(models.Model):
    ORDER_STATUS = (
        ('Active', 'Active'),
        ('Delivered', 'Delivered')
    )

    model=Item
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=150)
    price=models.FloatField()
    portions=models.IntegerField()
    ordered_on=models.TimeField(default=timezone.now)
    ordered = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Active')




class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    rslug = models.SlugField()
    review = models.TextField()
    posted_on = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.review