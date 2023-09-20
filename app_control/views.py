from django.http import HttpResponse
import psycopg2
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from .serializers import (
    Inventory, InventorySerializer, InventoryGroupSerializer, InventoryGroup,
    Shop, ShopSerializer, InventoryWithSumSerializer,
    ShopWithAmountSerializer, Colaborador, ColaboradorSerializer, 
    Inventory_Notebook, InventoryNotebookSerializer, Inventory_Mobile, InventoryMobileSerializer, Inventory_Datacenter, InventoryDatacenterSerializer
)
from rest_framework.response import Response
from inventory_api.custom_methods import IsAuthenticatedCustom
from inventory_api.utils import CustomPagination, get_query
from django.db.models import Count, Sum, F, Value
from django.db.models.functions import Concat
from django.db.models.functions import Coalesce, TruncMonth
from user_control.views import add_user_activity
from user_control.models import CustomUser
import csv
import codecs
from django.views.generic import View


class InventoryView(ModelViewSet):
    queryset = Inventory.objects.select_related(
        "local", "created_by", "colaborador")
    serializer_class = InventorySerializer
    permission_classes = (IsAuthenticatedCustom,)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset

        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)

        if keyword:
            search_fields = (
                "patrimonio", "colaborador__name", "motivo_depreciado"
            )
            query = get_query(keyword, search_fields)
            return results.filter(query)
        return results

    def create(self, request, *args, **kwargs):
        request.data.update({"created_by_id": request.user.id})
        return super().create(request, *args, **kwargs)


class InventoryNotebookView(ModelViewSet):
    queryset = Inventory_Notebook.objects.select_related(
        "local", "created_by", "colaborador")
    serializer_class = InventoryNotebookSerializer
    permission_classes = (IsAuthenticatedCustom,)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset

        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)

        if keyword:
            search_fields = (
                "patrimonio", "colaborador__name", "motivo_depreciado"
            )
            query = get_query(keyword, search_fields)
            return results.filter(query)
        return results

    def create(self, request, *args, **kwargs):
        permission_classes = (IsAuthenticatedCustom,)
        request.data.update({"created_by_id": request.user.id})
        return super().create(request, *args, **kwargs)
    
class InventoryMobileView(ModelViewSet):
    queryset = Inventory_Mobile.objects.select_related(
        "created_by", "colaborador")
    serializer_class = InventoryMobileSerializer
    permission_classes = (IsAuthenticatedCustom,)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset

        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)

        if keyword:
            search_fields = (
                "imei", "colaborador__name", "motivo_depreciado"
            )
            query = get_query(keyword, search_fields)
            return results.filter(query)
        return results

    def create(self, request, *args, **kwargs):
        request.data.update({"created_by_id": request.user.id})
        return super().create(request, *args, **kwargs)


class InventoryDatacenterView(ModelViewSet):
    queryset = Inventory_Datacenter.objects.select_related(
        "created_by", "colaborador")
    serializer_class = InventoryDatacenterSerializer
    permission_classes = (IsAuthenticatedCustom,)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset

        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)

        if keyword:
            search_fields = (
                "ip", "motivo_depreciado"
            )
            query = get_query(keyword, search_fields)
            return results.filter(query)
        return results

    def create(self, request, *args, **kwargs):
        request.data.update({"created_by_id": request.user.id})
        return super().create(request, *args, **kwargs)


class InventoryGroupView(ModelViewSet):
    queryset = InventoryGroup.objects.select_related(
        "belongs_to", "created_by").prefetch_related("inventories", "inventories_notebook")
    serializer_class = InventoryGroupSerializer
    permission_classes = (IsAuthenticatedCustom,)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset

        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)

        if keyword:
            search_fields = (
                "created_by__fullname", "created_by__email", "name"
            )
            query = get_query(keyword, search_fields)
            results = results.filter(query)


        return results.annotate(
            desktop_items=Count('inventories', distinct=True),
            notebook_items=Count('inventories_notebook', distinct=True),
            total_items=Count('inventories', distinct=True) + Count('inventories_notebook', distinct=True),
        )

        
    def create(self, request, *args, **kwargs):
        request.data.update({"created_by_id": request.user.id})
        return super().create(request, *args, **kwargs)


class ColaboradorView(ModelViewSet):
    queryset = Colaborador.objects.select_related(
        "created_by").prefetch_related("colaborador", "colaborador_notebook", "colaborador_mobile", "colaborador_datacenter")
    serializer_class = ColaboradorSerializer
    permission_classes = (IsAuthenticatedCustom,)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset

        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)

        if keyword:
            search_fields = (
                "created_by__fullname", "created_by__email", "name",
            )
            query = get_query(keyword, search_fields)
            results = results.filter(query)
        
        return results.annotate(
            total_items=Count('colaborador', distinct=True) + Count('colaborador_notebook', distinct=True) + Count('colaborador_mobile', distinct=True) + Count('colaborador_datacenter', distinct=True)
        )

    def create(self, request, *args, **kwargs):
        request.data.update({"created_by_id": request.user.id})
        return super().create(request, *args, **kwargs)


class ShopView(ModelViewSet):
    queryset = Shop.objects.select_related("created_by")
    serializer_class = ShopSerializer
    permission_classes = (IsAuthenticatedCustom,)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset

        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)

        if keyword:
            search_fields = (
                "created_by__fullname", "created_by__email", "name"
            )
            query = get_query(keyword, search_fields)
            results = results.filter(query)

        return results

    def create(self, request, *args, **kwargs):
        request.data.update({"created_by_id": request.user.id})
        return super().create(request, *args, **kwargs)


""" class InvoiceView(ModelViewSet):
    queryset = Invoice.objects.select_related(
        "created_by", "shop").prefetch_related("invoice_items")
    serializer_class = InvoiceSerializer
    permission_classes = (IsAuthenticatedCustom,)
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset

        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        results = self.queryset.filter(**data)

        if keyword:
            search_fields = (
                "created_by__fullname", "created_by__email", "shop__name"
            )
            query = get_query(keyword, search_fields)
            results = results.filter(query)

        return results

    def create(self, request, *args, **kwargs):
        request.data.update({"created_by_id": request.user.id})
        return super().create(request, *args, **kwargs) """


class SummaryView(ModelViewSet):
    http_method_names = ('get',)
    queryset = InventoryView.queryset

    def list(self, request, *args, **kwargs):
        total_desktop = InventoryView.queryset.count()
        total_notebook = InventoryNotebookView.queryset.count()
        total_mobile = InventoryMobileView.queryset.count()
        total_datacenter = InventoryDatacenterView.queryset.count()

        return Response({
            "total_inventory": total_desktop,
            "total_group": total_notebook,
            "total_shop": total_mobile,
            "total_users": total_datacenter
        })


class SalePerformanceView(ModelViewSet):
    http_method_names = ('get',)
    permission_classes = (IsAuthenticatedCustom,)
    queryset = InventoryView.queryset

    def list(self, request, *args, **kwargs):
        query_data = request.query_params.dict()
        total = query_data.get('total', None)
        query = self.queryset

        if not total:
            start_date = query_data.get("start_date", None)
            end_date = query_data.get("end_date", None)

            if start_date:
                query = query.filter(
                    created_at__range=[
                        start_date, end_date]
                )

        items = query.annotate(
            sum_of_item=Coalesce(
                Sum("inventory_invoices__quantity"), 0
            )
        ).order_by('-sum_of_item')[0:10]

        response_data = InventoryWithSumSerializer(items, many=True).data
        return Response(response_data)


class SaleByShopView(ModelViewSet):
    http_method_names = ('get',)
    permission_classes = (IsAuthenticatedCustom,)
    queryset = InventoryView.queryset

    def list(self, request, *args, **kwargs):
        query_data = request.query_params.dict()
        total = query_data.get('total', None)
        monthly = query_data.get('monthly', None)
        query = InventoryView.queryset

        if not total:
            start_date = query_data.get("start_date", None)
            end_date = query_data.get("end_date", None)

            if start_date:
                query = query.filter(
                    sale_shop__created_at__range=[start_date, end_date]
                )

        if monthly:
            shops = query.annotate(month=TruncMonth('created_at')).values(
                'month', 'name').annotate(amount_total=Sum(
                    F("sale_shop__invoice_items__quantity") *
                    F("sale_shop__invoice_items__amount")
                ))

        else:
            shops = query.annotate(amount_total=Sum(
                F("sale_shop__invoice_items__quantity") *
                F("sale_shop__invoice_items__amount")
            )).order_by("-amount_total")

        response_data = ShopWithAmountSerializer(shops, many=True).data
        return Response(response_data)


""" class PurchaseView(ModelViewSet):
    http_method_names = ('get',)
    permission_classes = (IsAuthenticatedCustom,)
    queryset = InvoiceView.queryset

    def list(self, request, *args, **kwargs):
        query_data = request.query_params.dict()
        total = query_data.get('total', None)
        query = InvoiceItem.objects.select_related("invoice", "item")

        if not total:
            start_date = query_data.get("start_date", None)
            end_date = query_data.get("end_date", None)

            if start_date:
                query = query.filter(
                    created_at__range=[start_date, end_date]
                )

        query = query.aggregate(
            amount_total=Sum(F('amount') * F('quantity')), total=Sum('quantity')
        )

        return Response({
            "price": "0.00" if not query.get("amount_total") else query.get("amount_total"),
            "count": 0 if not query.get("total") else query.get("total"),
        }) """


class InventoryCSVLoaderView(ModelViewSet):
    http_method_names = ('post',)
    queryset = InventoryView.queryset
    permission_classes = (IsAuthenticatedCustom,)
    serializer_class = InventorySerializer

    def create(self, request, *args, **kwargs):
        try:
            data = request.FILES['data']
        except Exception as e:
            raise Exception("You need to provide inventory CSV 'data'")

        inventory_items = []

        try:
            csv_reader = csv.reader(codecs.iterdecode(data, 'utf-8'))
            for row in csv_reader:
                if not row[0]:
                    continue
                inventory_items.append(
                    {
                        "group_id": row[0],
                        "total": row[1],
                        "name": row[2],
                        "price": row[3],
                        "photo": row[4],
                        "created_by_id": request.user.id
                    }
                )
        except csv.Error as e:
            raise Exception(e)

        if not inventory_items:
            raise Exception("CSV file cannot be empty")

        data_validation = self.serializer_class(
            data=inventory_items, many=True)
        data_validation.is_valid(raise_exception=True)
        data_validation.save()

        return Response({"success": "Inventory items added successfully"})

class ExportInventoryCSVView(View):

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="inventory.csv"'

        writer = csv.writer(response)
        writer.writerow(['Patrimonio', 'Hostname', 'Colaborador', 'Sistema Operacional', 'Service Tag', 'NF SO', 'Empresa', 'Marca', 'Modelo', 'Configuração'])

        inventories = Inventory.objects.all().values_list('patrimonio', 'hostname', 'colaborador__name', 'sistema_operacional', 'service_tag', 'nf_so', 'empresa', 'marca', 'modelo', 'configuracao')

        for inventory in inventories:
            writer.writerow(inventory)

        return response
