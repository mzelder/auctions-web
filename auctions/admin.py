from django.contrib import admin
from .models import User, Listing, Bid, Watchlist, Category, Comments

# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Watchlist)
admin.site.register(Category)
admin.site.register(Comments)