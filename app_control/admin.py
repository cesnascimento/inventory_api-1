from django.contrib import admin
from .models import Inventory, InventoryGroup, Shop, Colaborador, Inventory_Notebook, Inventory_Datacenter, Inventory_Mobile


admin.site.register((Inventory, InventoryGroup, Shop, Colaborador, Inventory_Notebook, Inventory_Datacenter, Inventory_Mobile))