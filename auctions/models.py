from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category (models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

class Item (models.Model):
    item = models.CharField(max_length=64)
    price = models.IntegerField()
    description = models.TextField(blank=True, null = True)
    picture = models.TextField(blank=True, null = True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(blank=True)

    def __str__(self):
        return f"{self.item}"

class Bidder(models.Model):
    price = models.IntegerField()
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.winner}, bids {self.price} on {self.item}"


class Watchlist(models.Model):
    #item = models.ManyToManyField(Item, blank=True, default="None", related_name="user")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}, {self.item}"

class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=False, null = False)

    def __str__(self):
        return f"{self.commenter} comments on {self.item}" 