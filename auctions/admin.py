from django.contrib import admin

from .models import User, Category, Item, Bidder, Watchlist, Comment 

# Register your models here.
#class Categories(admin.ModelAdmin):
#    list_display = ("name","username", "passowrd", "email")

class ItemAdmin(admin.ModelAdmin):
    list_display =("id", "item", "category", "price", "owner")

class BidAdmin(admin.ModelAdmin):
    #filter_horizontal = ("item",)
    list_display =("item", "winner", "price")

class WatchlistAdmin(admin.ModelAdmin):
    #filter_horizontal = ("item",)
    list_display =("id", "item", "user")

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
admin.site.register(Bidder, BidAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Comment)