from django.contrib.auth.models import AbstractUser
from django.db import models


CATEGORY_CHOICES = [
        ("Mobile Phone", "Mobile Phone"),
        ("Laptops", "Laptops"),
        ("Cameras", "Cameras"),
        ("Televisions", "Televisions"),
        ("Audio Equipment", "Audio Equipment")
    ]

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.name

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    creation_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="images/", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="listings", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def highest_bid(self):
        highest_bid = self.bids.order_by("-amount").first()
        return highest_bid.amount if highest_bid else self.starting_bid

class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    item = models.ForeignKey(Listing, related_name="bids", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.amount} on {self.item}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing ,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} watching {self.item}"
    
class Comments(models.Model):
    comment = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} commented on {self.item}"