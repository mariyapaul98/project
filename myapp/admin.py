from django.contrib import admin

#user_login,user_details,cake_master,cake_order,cake_payment,user_cake_order,cake_offers
# Register your models here.
from .models import user_login,user_details,service_master,service_order,service_payment,service_offers


admin.site.register(user_login)
admin.site.register(user_details)
admin.site.register(service_master)
admin.site.register(service_order)
admin.site.register(service_payment)
admin.site.register(service_offers)
