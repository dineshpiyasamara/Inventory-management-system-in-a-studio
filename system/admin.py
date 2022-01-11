from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from system.models import *


# stack Account to User
class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Accounts'


class CustomizedUserAdmin(UserAdmin):
    inlines = (AccountInline, )


admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)

admin.site.register(Item)
admin.site.register(SellingPrice)
admin.site.register(Suppliers)
admin.site.register(Purchases)
admin.site.register(Customers)
admin.site.register(Sales)
