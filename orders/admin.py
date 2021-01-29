from django.contrib import admin
from .models import Regular_Pizza, Sicilian_Pizza, Topping, Sub, Subs_Extra, Pasta, Salad, Dinner_Platter, Cart, All_Order

# # Register your models here.

# class PassengerInline(admin.StackedInline):
#     model = Passenger.flights.through
#     extra = 1

# class FlightAdmin(admin.ModelAdmin):
#     inlines = [PassengerInline]

# class PassengerAdmin(admin.ModelAdmin):
#     filter_horizontal = ("flights",)

admin.site.register(Regular_Pizza)
admin.site.register(Sicilian_Pizza)
admin.site.register(Topping)
admin.site.register(Sub)
admin.site.register(Subs_Extra)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Dinner_Platter)
admin.site.register(Cart)
admin.site.register(All_Order)

# admin.site.register(Flight, FlightAdmin)
# admin.site.register(Passenger, PassengerAdmin)
