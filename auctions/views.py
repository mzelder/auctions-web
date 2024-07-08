from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing, Bid, Watchlist, Category, Comments
from .forms import ListingForm


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })

@login_required
def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            # Valid bid
            starting_bid = form.cleaned_data["starting_bid"] 
            if starting_bid <= 0:
                messages.error(request, "Starting bid must be greater than 0")
                return redirect("create")
            # Valid category
            category = form.cleaned_data["category"]
            category = Category.objects.get(name=category)

            listing = Listing( 
                title = form.cleaned_data["title"],
                description = form.cleaned_data["description"],
                starting_bid = starting_bid,
                image = form.cleaned_data["image"],
                category = category,
                user = request.user
            )
            listing.save()

            #Check if bid exist in database
            bid = Bid.objects.filter(item=listing)
            bid = Bid(amount=starting_bid, item=listing, user=request.user)
            bid.save()

            messages.success(request, "Listing created sucessfully!")
            return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create.html", {
        "form": ListingForm()
    }) 

def listing(request, id):
    listing = Listing.objects.get(id=id)
    comments = listing.comments.all()
    bids = listing.bids.order_by("-amount")    
    latest_bid = bids.first()

    if latest_bid.user == request.user:
        message = "You are the highest bidder"
    else:
        message = f"The highest bid is from {latest_bid.user}"
    
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": bids,
        "message": message,
        "comments": comments
    })

@login_required
def bid(request, id):
    listing = Listing.objects.get(id=id)
    if request.method == "POST":
        bid_amount = request.POST.get("amount")

        # Checking if bid amount is not null
        if not bid_amount:
            messages.error(request, "Bid amount is required")
            return redirect("listing", id=id)

        # Checking if bid amount is a number
        try:
            bid_amount = float(bid_amount)
        except ValueError:
            messages.error(request, "Bid amount must be a number")
            return redirect("listing", id=id)
        
        # Checking if bid is greater than the starting bid
        highest_bid = listing.bids.order_by("-amount").first()
        if bid_amount <= highest_bid.amount:
            messages.error(request, "Bid amount must be greater than the current one")
            return redirect("listing", id=id)
        
        # Addding the bid to the database
        bid = Bid(
            amount = bid_amount,
            item = listing,
            user = request.user
        )
        bid.save()
        messages.success(request, "Bid added successfully")
        return redirect("listing", id=id)

@login_required
def watchlist(request):
    watchlist_items = Watchlist.objects.filter(user=request.user).select_related("item")
    print(f"THIS IS THIS: {watchlist_items}")
    return render(request, "auctions/watchlist.html", {
        "watchlist_items": watchlist_items
    })

@login_required
def add_to_watchlist(request, id):
    listing = Listing.objects.get(id=id)
    watchlist_item = Watchlist(user=request.user, item=listing)
    watchlist_item.save()
    return redirect("watchlist")

def categories_list(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def get_category_listings(request, id):
    category = Category.objects.get(id=id)
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "category": category
    })

@login_required
def add_comment(request, id):
    listing = Listing.objects.get(id=id)
    comment = request.POST.get("comment")
    Comments(comment=comment, user=request.user, item=listing).save()
    return redirect("listing", id=id)


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
