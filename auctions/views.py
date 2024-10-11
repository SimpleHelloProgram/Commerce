from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, listing, Comments, Bid


def index(request):
    activeLt = listing.objects.filter(isActive = True)
    allC = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listing":activeLt,
        "categories":allC
    })

def removeWatchList(request, id):
    listingData = listing.objects.get(id = id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def addWatchList(request, id):
    listingData = listing.objects.get(id = id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id,)))
    
    
def listin(request, id):
    listings = listing.objects.get(id = id)
    isListingInWatchlist = request.user in listings.watchlist.all()
    allComment = Comments.objects.filter(listing = listings)
    isOwner = request.user.username == listings.owner.username
    return render(request, "auctions/listing.html", {
        "listing":listings,
        "isListingInWatchList":isListingInWatchlist,
        "comments":allComment,
        "isOwner":isOwner,
    })

def display_watchList(request):
    currentUser = request.user
    listings = currentUser.listingWatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listing":listings,
    })

def add_comment(request, id):
    currentUser = request.user
    listingData = listing.objects.get(id = id)
    message = request.POST["comment"]
    
    newComment = Comments(
        owner = currentUser,
        listing = listingData,
        comment = message
    )
    newComment.save()
    
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def add_bid(request, id):
        new_Bid = request.POST["new-Bid"]
        listings = listing.objects.get(id = id)
        isOwner = request.user.username = listings.owner.username
        isListingInWatchlist = request.user in listings.watchlist.all()
        allComment = Comments.objects.filter(listing = listings)
        
        if float(new_Bid) > listings.price.bid:
            updateBid = Bid(user = request.user, bid = float(new_Bid))
            updateBid.save()
            listings.price = updateBid
            listings.save()
            return render(request, "auctions/listing.html", {
                "listing":listings,
                "message":"Successful Buy",
                 "update": True,
                "isListingInWatchList":isListingInWatchlist,
                 "comments":allComment,
                 "isOwner":isOwner
            })
        else:
            return render(request, "auctions/listing.html", {
                "listing":listings,
                "message":"Failed Buy",
                "update": False,
                "isListingInWatchList":isListingInWatchlist,
                "comments":allComment,
                "isOwner":isOwner
            })
def display_cat(request):
     if request.method == "POST":
        categoryC = request.POST["catergory"]
        category = Category.objects.get(type = categoryC)
        activeLt = listing.objects.filter(isActive = True, catergory = category)
        allC = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listing":activeLt,
            "selected":category,
            "categories":allC
        })

def closeAuction(request, id):
    listingData = listing.objects.get(id = id)
    currentUser = request.user
    listingData.isActive = False
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComment = Comments.objects.filter(listing = listingData)
    listingData.save()
    isOwner = request.user.username = listingData.owner.username
    return render(request, "auctions/listing.html", {
        "listing":listingData,
        "update":True,
        "isListingInWatchList":isListingInWatchlist,
        "comments":allComment,
        "message":"Auction is succefully closed",
        "isOwner":isOwner
    })

def createListing(request):
    if request.method == "GET":
        allC = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories":allC
        })
    else:
        title = request.POST["title"]
        img = request.POST["img"]
        dec = request.POST["Decription"]
        price = request.POST["price"]
        cat = request.POST["catergory"]
        
        catData = Category.objects.get(type = cat)
        currentUser = request.user
        newbid = Bid(bid = float(price), user = currentUser)
        newbid.save()
        
        newListing = listing(title = title, description = dec, 
                             img_url = img, price = newbid,
                             catergory = catData, owner = currentUser)
        
        newListing.save()
        
        return HttpResponseRedirect(reverse("index"))
    


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
