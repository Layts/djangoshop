from django.db import models
from django.conf import global_settings
from django.shortcuts import reverse
from autoslug import AutoSlugField


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    photo = models.ImageField()
    aroma = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    slug = AutoSlugField(populate_from='title', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:item", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=100, default=item)
    order_name = models.ForeignKey("Order", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.CharField(max_length=100)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now=True)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField()
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title



