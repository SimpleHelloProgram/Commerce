from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createListing, name="create"),
    path("display_cat", views.display_cat, name = "display_cat"),
    path("listing/<int:id>", views.listin, name = "listing"),
    path("removeWatchList/<int:id>", views.removeWatchList, name = "removeWatchList"),
    path("addWatchList/<int:id>",  views.addWatchList, name = "addWatchList"),
    path("display_watchList", views.display_watchList, name = "display_watchList"),
    path("add_comment/<int:id>", views.add_comment, name = "add_comment"),
    path("add_bid/<int:id>", views.add_bid, name = "add_bid"),
    path("closeAuction/<int:id>", views.closeAuction , name = "closeAuction"),
]
