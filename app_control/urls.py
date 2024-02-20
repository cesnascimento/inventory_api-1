from django.urls import path, include
from .views import (
    ExportInventoryCSVView, ExportInventoryDatacenterCSVView, ExportInventoryMobileCSVView, ExportInventoryNotebookCSVView, InventoryView, ShopView, SummaryView, SaleByShopView,
    InventoryGroupView, SalePerformanceView, InventoryCSVLoaderView, 
    ColaboradorView, InventoryNotebookView, InventoryMobileView,
    InventoryDatacenterView
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

router.register('inventory', InventoryView, "inventory")
router.register('inventory-notebook', InventoryNotebookView, "inventory-notebook")
router.register('inventory-mobile', InventoryMobileView, "inventory-mobile")
router.register('inventory-datacenter', InventoryDatacenterView, "inventory-datacenter")
router.register('inventory-csv', InventoryCSVLoaderView, "inventory-csv")
router.register('shop', ShopView, "shop")
router.register('summary', SummaryView, "summary")
router.register('sales-by-shop', SaleByShopView, "sales-by-shop")
router.register('group', InventoryGroupView, "group")
router.register('top-selling', SalePerformanceView, "top-selling")
router.register('colaborate', ColaboradorView, "colaborate")

urlpatterns = [
    path('export-desktop-csv/', ExportInventoryCSVView.as_view(), name='export_inventory_csv'),
    path('export-notebook-csv/', ExportInventoryNotebookCSVView.as_view(), name='export_inventory_notebook_csv'),
    path('export-mobile-csv/', ExportInventoryMobileCSVView.as_view(), name='export_inventory_mobile_csv'),
    path('export-datacenter-csv/', ExportInventoryDatacenterCSVView.as_view(), name='export_inventory_datacenter_csv'),
    path("", include(router.urls))
]