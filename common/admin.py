from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Account)
admin.site.register(Bill)
admin.site.register(Payment)
admin.site.register(RecurringPayment)
admin.site.register(ShoppingList)
admin.site.register(ListItem)
admin.site.register(UserNotification)
admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(Patrimony)

admin.site.register(Budget)
admin.site.register(BudgetCategory)
admin.site.register(BudgetItem)