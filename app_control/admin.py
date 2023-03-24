from django.contrib import admin
from .models import Inventory, InventoryGroup, Shop, Invoice, InvoiceItem, Colaborador, Inventory_Notebook, Inventory_Datacenter, Inventory_Mobile


admin.site.register((Inventory, InventoryGroup, Shop, Invoice, InvoiceItem, Colaborador, Inventory_Notebook, Inventory_Datacenter, Inventory_Mobile))