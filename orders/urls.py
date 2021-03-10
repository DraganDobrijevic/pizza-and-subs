from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("home", views.home, name="home"),
    path("menu", views.menu, name="menu"),
    path("cart", views.cart, name="cart"),
    path("menu/regular_pizza/<int:pizza_id>", views.regular_pizza, name="regular_pizza"),
    path("menu/sicilian_pizza/<int:pizza_id>", views.sicilian_pizza, name="sicilian_pizza"),
    path("menu/subs/<int:sub_id>", views.subs, name="subs"),
    path("menu/pasta/<int:pasta_id>", views.pasta, name="pasta"),
    path("menu/salad/<int:salad_id>", views.salad, name="salad"),
    path("menu/dinner_platter/<int:platter_id>", views.platters, name="platters"),
    path("menu/delete/<int:item_id>", views.delete, name="delete"),
    path("menu/order", views.order, name="order"),
    path("orders", views.orders, name="orders"),
    path("orders/status/<int:item_id>", views.status, name="status"),
    path("my_orders", views.my_orders, name="my_orders"),
    # path("<int:flight_id>", views.flight, name="flight"),
    # path("<int:flight_id>/book", views.book, name="book")
]
