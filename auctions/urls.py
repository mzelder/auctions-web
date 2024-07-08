from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("comment/<int:id>", views.add_comment, name="add_comment"),
    path("bid/<int:id>", views.bid, name="bid"), 
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/add/<int:id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("categories", views.categories_list, name="categories_list"),
    path("categories/<int:id>", views.get_category_listings, name="get_category_listings")
]
