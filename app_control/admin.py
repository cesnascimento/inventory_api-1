from django.contrib import admin
from .models import Inventory, InventoryGroup, Shop, Invoice, InvoiceItem, Colaborador


admin.site.register((Inventory, InventoryGroup, Shop, Invoice, InvoiceItem, Colaborador))