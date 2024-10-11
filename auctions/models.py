from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    type = models.CharField(max_length=50)
    
    def __str__(self):
        return self.type


    
class Bid(models.Model):
    bid = models.FloatField(default = 0)
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank = True, null = True, related_name = "userBid")

    def __str__(self):
        return str(self.bid)
    
    
class listing(models.Model):
    title = models.CharField(max_length=800)
    description = models.CharField(max_length=1000)
    img_url = models.CharField(max_length=1000)
    price = models.ForeignKey(Bid,on_delete=models.CASCADE, blank = True, null = True, related_name = "bidPrice")
    owner = models.ForeignKey(User,on_delete=models.CASCADE, blank = True, null = True, related_name = "user")
    catergory = models.ForeignKey(Category, on_delete=models.CASCADE)
    isActive = models.BooleanField(default = True)
    watchlist = models.ManyToManyField(User, blank=True, null = True, related_name="listingWatchlist")
    
    def __str__(self):
        return self.title
    
class Comments(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE, blank = True, null = True, related_name = "userComment")
    comment = models.CharField(max_length=2000)
    listing = models.ForeignKey(listing ,on_delete=models.CASCADE, blank = True, null = True, related_name = "listingComment")
    
    def __str__(self):
        return f"{self.owner} comment to {self.listing}"


