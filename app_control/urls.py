from django.urls import path, include
from .views import (
    InventoryView, ShopView, SummaryView, PurchaseView, SaleByShopView,
    InventoryGroupView, SalePerformanceView, InvoiceView, InventoryCSVLoaderView, 
    ColaboradorView, InventoryNotebookView, InventoryMobileView
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

router.register('inventory', InventoryView, "inventory")
router.register('inventory-notebook', InventoryNotebookView, "inventory-notebook")
router.register('inventory-mobile', InventoryMobileView, "inventory-mobile")
router.register('inventory-csv', InventoryCSVLoaderView, "inventory-csv")
router.register('shop', ShopView, "shop")
router.register('summary', SummaryView, "summary")
router.register('purchase-summary', PurchaseView, "purchase-summary")
router.register('sales-by-shop', SaleByShopView, "sales-by-shop")
router.register('group', InventoryGroupView, "group")
router.register('top-selling', SalePerformanceView, "top-selling")
router.register('invoice', InvoiceView, "invoice")
router.register('colaborate', ColaboradorView, "colaborate")

urlpatterns = [
    path("", include(router.urls))
]