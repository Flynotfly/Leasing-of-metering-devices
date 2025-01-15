from django.contrib import admin

from .models import Profile, Contract, FinanceDetails, Payment, WarrantyCase


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'display_name', 'role']


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['lessor', 'lessee', 'seller']


@admin.register(FinanceDetails)
class FinanceDetailsAdmin(admin.ModelAdmin):
    list_display = ['contract', 'monthly_payment']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['contract', 'amount', 'date']


@admin.register(WarrantyCase)
class WarrantyCaseAdmin(admin.ModelAdmin):
    list_display = ['contract']
