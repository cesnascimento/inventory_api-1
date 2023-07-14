from django.db import models
from user_control.models import CustomUser
from user_control.views import add_user_activity


class InventoryGroup(models.Model):
    created_by = models.ForeignKey(
        CustomUser, null=True, related_name="inventory_groups",
        on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=100, unique=True)
    belongs_to = models.ForeignKey(
        'self', null=True, on_delete=models.SET_NULL, related_name="group_relations"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_name = self.name

    def save(self, *args, **kwargs):
        action = f"added new group - '{self.name}'"
        if self.pk is not None:
            action = f"updated group from - '{self.old_name}' to '{self.name}'"
        super().save(*args, **kwargs)
        add_user_activity(self.created_by, action=action)

    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted group - '{self.name}'"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return self.name


class Colaborador(models.Model):
    created_by = models.ForeignKey(
        CustomUser, null=True, related_name="colaborador",
        on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=100, unique=True)
    belongs_to = models.ForeignKey(
        InventoryGroup, null=True, on_delete=models.SET_NULL, related_name="colab_relations"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-id",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_name = self.name

    def save(self, *args, **kwargs):
        action = f"added new group - '{self.name}'"
        if self.pk is not None:
            action = f"updated group from - '{self.old_name}' to '{self.name}'"
        super().save(*args, **kwargs)
        add_user_activity(self.created_by, action=action)

    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted group - '{self.name}'"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return self.name


""" class Colaborador(models.Model):
    created_by = models.ForeignKey(
        CustomUser, null=True, related_name="colaboratte",
        on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=100)
    inventory_group = models.ForeignKey(InventoryGroup, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_name = self.name

    def save(self, *args, **kwargs):
        action = f"added new colab - '{self.name}'"
        if self.pk is not None:
            action = f"updated colab from - '{self.old_name}' to '{self.name}'"
        super().save(*args, **kwargs)
        add_user_activity(self.created_by, action=action)

    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted colab - '{self.name}'"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return self.name """


class Inventory(models.Model):
    created_by = models.ForeignKey(
        CustomUser, null=True, related_name="inventory_items",
        on_delete=models.SET_NULL
    )
    local = models.ForeignKey(
        InventoryGroup, related_name="inventories", null=True, on_delete=models.SET_NULL
    )
    patrimonio = models.PositiveIntegerField(null=True)
    hostname = models.CharField(max_length=25, null=True, unique=True)
    usuario = models.CharField(max_length=100, null=True)
    colaborador = models.ForeignKey(
        Colaborador, related_name="colaborador", null=True, on_delete=models.SET_NULL
    )
    sistema_operacional = models.CharField(max_length=10, null=True)
    service_tag = models.CharField(max_length=20, null=True)
    nf_so = models.PositiveIntegerField(null=True)
    empresa = models.CharField(max_length=50, null=True)
    marca = models.CharField(max_length=10, null=True)
    modelo = models.CharField(max_length=100, null=True)
    configuracao = models.TextField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:
            id_length = len(str(self.id))
            code_length = 6 - id_length
            zeros = "".join("0" for i in range(code_length))
            self.code = f"BOSE{zeros}{self.id}"
            self.save()

        action = f"Adicionado novo item ao inventário com o patrimonio - '{self.patrimonio}'"

        if not is_new:
            action = f"Atualizado item ao inventário com o patrimonio - '{self.patrimonio}'"

        add_user_activity(self.created_by, action=action)

    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"Deletado equipamento - '{self.patrimonio}'"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return f"{self.modelo} - {self.patrimonio}"


class Inventory_Notebook(models.Model):
    created_by = models.ForeignKey(
        CustomUser, null=True, related_name="inventory_notebook_items",
        on_delete=models.SET_NULL
    )
    local = models.ForeignKey(
        InventoryGroup, related_name="inventories_notebook", null=True, on_delete=models.SET_NULL
    )
    patrimonio = models.PositiveIntegerField(null=True)
    hostname = models.CharField(max_length=25, null=True, unique=True)
    usuario = models.CharField(max_length=100, null=True)
    colaborador = models.ForeignKey(
        Colaborador, related_name="colaborador_notebook", null=True, on_delete=models.SET_NULL
    )
    sistema_operacional = models.CharField(max_length=10, null=True)
    service_tag = models.CharField(max_length=20, null=True)
    nf_so = models.PositiveIntegerField(null=True)
    empresa = models.CharField(max_length=50, null=True)
    marca = models.CharField(max_length=10, null=True)
    modelo = models.CharField(max_length=100, null=True)
    configuracao = models.TextField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:
            id_length = len(str(self.id))
            code_length = 6 - id_length
            zeros = "".join("0" for i in range(code_length))
            self.code = f"BOSE{zeros}{self.id}"
            self.save()

        action = f"added new inventory item with code - '{self.patrimonio}'"

        if not is_new:
            action = f"updated inventory item with code - '{self.patrimonio}'"

        add_user_activity(self.created_by, action=action)

    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted inventory - '{self.patrimonio}'"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return f"{self.modelo} - {self.patrimonio}"
    

class Inventory_Mobile(models.Model):
    created_by = models.ForeignKey(
        CustomUser, null=True, related_name="inventory_mobile_items",
        on_delete=models.SET_NULL
    )
    patrimonio = models.PositiveIntegerField(null=True)
    marca = models.CharField(max_length=25, null=True)
    modelo = models.CharField(max_length=25, null=True)
    usuario = models.CharField(max_length=100, null=True)
    colaborador = models.ForeignKey(
        Colaborador, related_name="colaborador_mobile", null=True, on_delete=models.SET_NULL
    )
    imei = models.CharField(max_length=500, null=True)
    nf = models.CharField(max_length=50, null=True)
    linha = models.CharField(max_length=50, null=True)
    obs = models.TextField(max_length=500, null=True)


    class Meta:
        ordering = ("-created_by",)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:
            id_length = len(str(self.id))
            code_length = 6 - id_length
            zeros = "".join("0" for i in range(code_length))
            self.code = f"BOSE{zeros}{self.id}"
            self.save()

        action = f"added new inventory item with patrimonio - '{self.patrimonio}'"

        if not is_new:
            action = f"updated inventory item with patrimonio - '{self.patrimonio}'"

        add_user_activity(self.created_by, action=action)

    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted inventory - '{self.patrimonio}'"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return f"{self.modelo} - {self.colaborador}"
    

class Inventory_Datacenter(models.Model):
    created_by = models.ForeignKey(
        CustomUser, null=True, related_name="inventory_datacenter_items",
        on_delete=models.SET_NULL
    )
    ip = models.CharField(max_length=25, null=True, unique=True)
    descricao = models.CharField(max_length=500, null=True)
    hostname = models.CharField(max_length=25, null=True, unique=True)
    colaborador = models.ForeignKey(
        Colaborador, related_name="colaborador_datacenter", null=True, on_delete=models.SET_NULL
    )
    sistema_operacional = models.CharField(max_length=25, null=True)
    service_tag = models.CharField(max_length=25, null=True)
    nf_so = models.PositiveIntegerField(null=True)
    empresa = models.CharField(max_length=50, null=True)
    marca = models.CharField(max_length=25, null=True)
    modelo = models.CharField(max_length=100, null=True)
    configuracao = models.TextField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:
            id_length = len(str(self.id))
            code_length = 6 - id_length
            zeros = "".join("0" for i in range(code_length))
            self.code = f"BOSE{zeros}{self.id}"
            self.save()

        action = f"added new inventory item with patrimonio - '{self.ip}'"

        if not is_new:
            action = f"updated inventory item with patrimonio - '{self.ip}'"

        add_user_activity(self.created_by, action=action)

    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted inventory - '{self.ip}'"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return f"{self.modelo} - {self.colaborador}"


class Shop(models.Model):
    created_by = models.ForeignKey(
        CustomUser, null=True, related_name="shops",
        on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_name = self.name

    def save(self, *args, **kwargs):
        action = f"added new shop - '{self.name}'"
        if self.pk is not None:
            action = f"updated shp[] from - '{self.old_name}' to '{self.name}'"
        super().save(*args, **kwargs)
        add_user_activity(self.created_by, action=action)

    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted shop - '{self.name}'"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    created_by = models.ForeignKey(
        CustomUser, null=True, related_name="invoices",
        on_delete=models.SET_NULL
    )
    shop = models.ForeignKey(
        Shop, related_name="sale_shop", null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def delete(self, *args, **kwargs):
        created_by = self.created_by
        action = f"deleted invoice - '{self.id}'"
        super().delete(*args, **kwargs)
        add_user_activity(created_by, action=action)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice, related_name="invoice_items", on_delete=models.CASCADE
    )
    item = models.ForeignKey(
        Inventory, null=True, related_name="inventory_invoices",
        on_delete=models.SET_NULL
    )
    item_name = models.CharField(max_length=255, null=True)
    item_code = models.CharField(max_length=20, null=True)
    quantity = models.PositiveIntegerField()
    amount = models.FloatField(null=True)

    def save(self, *args, **kwargs):
        if self.item.remaining < self.quantity:
            raise Exception(
                f"item with code {self.item.code} does not have enough quantity")

        self.item_name = self.item.name
        self.item_code = self.item.code

        self.amount = self.quantity * self.item.price
        self.item.remaining = self.item.remaining - self.quantity
        self.item.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item_code} - {self.quantity}"
