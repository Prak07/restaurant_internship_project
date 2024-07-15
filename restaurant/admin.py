from django.contrib import admin
from rangefilter.filters import NumericRangeFilter
from .models import Restaurant
# Register your models here.


class RestaurantAdmin(admin.ModelAdmin):
    list_filter = ('location',('items', NumericRangeFilter))

admin.site.register(Restaurant,RestaurantAdmin)