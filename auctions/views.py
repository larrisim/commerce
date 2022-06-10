from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Category, Item, Bidder, Comment, Watchlist

@login_required
def index(request):
    return render(request, "auctions/index.html",{
        "items": Item.objects.all().filter(active=True)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def newlist(request):
    if request.method =="POST":
        title = request.POST["title"]
        description = request.POST["description"]
        category = Category.objects.get(category=request.POST["category"])
        picture = request.POST["picture"]
        price = request.POST["price"]
        user = request.user

        print(title, category, price)
        
        item = Item.objects.create(item=title, category=category, description=description, picture=picture, price=price, owner=user)
        item.save()

        print(item)
        print(item.description)
        print(item.picture)

        return HttpResponseRedirect(reverse("listing", args=[item.id]))

    else:
        return render(request, "auctions/newlist.html", {
            "categories":Category.objects.all()
        })

@login_required
def listing(request, item_id):
    if request.method == "POST":

        if "comment" in request.POST:
            commenter = request.user
            comment = request.POST["comment"]
            item = Item.objects.get(pk=item_id)
            
            entry = Comment.objects.create(commenter = commenter, comment = comment, item=item)
            entry.save()

            return HttpResponseRedirect(reverse("listing", args=[item.id]))

        elif "new_bid" in request.POST:
            #return HttpResponseRedirect(reverse("listing", args=[item.id]))
            new_price = request.POST["new_bid"]
            item = Item.objects.get(pk=item_id)
            current_price = item.price
            winner = request.user

            if int(new_price) > current_price:
                entry = Bidder.objects.create(item = item, winner = winner, price = new_price)
                entry.save()
                Item.objects.filter(pk=item_id).update(price = new_price)

                return HttpResponseRedirect(reverse("listing", args=[item.id]))

        elif "add_to_watchlist" in request.POST:
            user = request.user
            item = Item.objects.get(pk=item_id)
            entry = Watchlist.objects.create(item=item, user=user)
            entry.save()
            return HttpResponseRedirect(reverse("listing", args=[item.id]))
        
        elif "remove_from_watchlist" in request.POST:
            user = request.user
            item = Item.objects.get(pk=item_id)
            Watchlist.objects.filter(item=item, user=user).delete()
            return HttpResponseRedirect(reverse("listing", args=[item.id]))
        
        elif "close_bid" in request.POST:
            Item.objects.filter(pk=item_id).update(active=False)
            #winner = Bidder.objects.filter(item = Item.objects.get(pk=item_id))
            return HttpResponseRedirect(reverse("index"))

    else:
        user = request.user
        watchlist = Watchlist.objects.filter(user = user, item = Item.objects.get(pk=item_id))
        bid = Bidder.objects.filter(item = Item.objects.get(pk=item_id))
        #winner = bid.winner

        return render(request, "auctions/listing.html",{
            "item": Item.objects.get(pk=item_id),
            "user": request.user,
            "watchlist": watchlist,
            "comments": Comment.objects.all().filter(item = Item.objects.get(pk=item_id)),
            #"bid": Bidder.objects.all().filter(item = Item.objects.get(pk=item_id))
            "winner": bid
        })

@login_required
def watchlist(request):
    user = request.user
    #watchlist = Watchlist.objects.all().filter(user = user)
    #print(Watchlist.objects.all().filter(user = user))

    #item = Watchlist.objects.select_related('item').all().filter(user = user)
    item__in = Item.objects.prefetch_related('watchlist_set').filter(watchlist__user=user)
    #print(item)
    #watch_list = list(watchlist)
    #item = Item.objects.all().filter(active = True)

    return render(request, "auctions/watchlist.html",{
        "items": item__in,
    })

@login_required
def categories(request):
    if request.method == "POST":

        category = Category.objects.get(category=request.POST["category"])
        return render(request, "auctions/categories.html",{
        "items": Item.objects.filter(active=True, category = category),
        "categories": Category.objects.exclude(category = category),
        "default": category
        })

    else:
        return render(request, "auctions/categories.html",{
        "items": Item.objects.filter(active=True),
        "categories": Category.objects.all(),
        "default": "Choose A Category"
    })