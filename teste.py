class Inventory(models.Model):
    created_by = models.ForeignKey(
        CustomUser, null=True, related_name="inventory_items",
        on_delete=models.SET_NULL
    )
    local = models.ForeignKey(
        InventoryGroup, related_name="inventories", null=True, on_delete=models.SET_NULL
    )
    colaborador = models.ForeignKey(
        Colaborador, related_name="colaborador", null=True, on_delete=models.SET_NULL
    )

    patrimonio = models.PositiveIntegerField(null=True)
    hostname = models.CharField(max_length=25, null=True, unique=True)
    usuario = models.CharField(max_length=100, null=True)
    sistema_operacional = models.CharField(max_length=10, null=True)
    service_tag = models.CharField(max_length=20, null=True)
    nf_so = models.PositiveIntegerField(null=True)
    empresa = models.CharField(max_length=50, null=True)
    marca = models.CharField(max_length=10, null=True)
    modelo = models.CharField(max_length=100, null=True)
    configuracao = models.TextField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tipo = models.CharField(max_length=255, null=True)

    #Depreciado
    depreciado = models.BooleanField(default=False)

    # Campos para Mobile
    imei = models.CharField(max_length=500, null=True)
    nf_mobile = models.CharField(max_length=50, null=True)
    linha = models.CharField(max_length=50, null=True)
    obs = models.TextField(max_length=500, null=True)

    # Campos para Datacenter
    ip = models.CharField(max_length=25, null=True, unique=True)
    descricao = models.CharField(max_length=500, null=True)
    hostname = models.CharField(max_length=25, null=True, unique=True)

    # query Inventory by tipo = Notebook
    Inventory.objects.filter(tipo='Notebook').filter(Depreciado=False)
    Inventory.objects.filter(tipo='Notebook').filter(Depreciado=True)

    def save_mobile(self, *args, **kwargs):
        self.tipo = 'Mobile'
        # Function here
      
    def save_datacenter(self, *args, **kwargs):
        self.tipo = 'Datacenter'
        # Function here

    def save_notebook(self, *args, **kwargs):
        self.tipo = 'Notebook'
        # Function here