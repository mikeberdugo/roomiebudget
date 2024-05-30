from django.contrib import admin
from .models import Account, Bill, Payment,Board

admin.site.register(Board)
admin.site.register(Account)
admin.site.register(Bill)
admin.site.register(Payment)
