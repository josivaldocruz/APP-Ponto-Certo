from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Usuario(AbstractUser):

    PERFIL_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('GERENTE', 'Gerente'),
        ('OPERADOR', 'Operador'),
        ('ESTOQUISTA', 'Estoquista'),
    )

    nome = models.CharField(max_length=150, unique=True)
    senha = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, unique=True)
    perfil = models.CharField(max_length=20, choices=PERFIL_CHOICES)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    codigo_barras = models.CharField(max_length=50, unique=True)
    sku = models.CharField(max_length=50, unique=True)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    estoque_atual = models.IntegerField(default=0)
    estoque_minimo = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class Movimentacao_Estoque(models.Model):

    TIPO_CHOICES = (
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
        ('AJUSTE', 'Ajuste'),
        ('PERDA', 'Perda'),
        ('DEVOLUCAO', 'Devolução'),
    )

    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    usuario = models.ForeignKey('Usuario', on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    motivo = models.CharField(max_length=255, blank=True, null=True)
    data_hora = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.tipo} - {self.produto.nome}"

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    cpf_cnpj = models.CharField(max_length=20, unique=True, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nome

class Sessao_Caixa(models.Model):

    STATUS_CHOICES = (
        ('ABERTO', 'Aberto'),
        ('FECHADO', 'Fechado'),
    )

    usuario = models.ForeignKey('Usuario', on_delete=models.PROTECT)
    data_abertura = models.DateTimeField()
    data_fechamento = models.DateTimeField(blank=True, null=True)
    valor_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    valor_final_informado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor_final_sistema = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ABERTO')

    def __str__(self):
        return f"Caixa {self.id} - {self.status}"

class Venda(models.Model):

    STATUS_CHOICES = (
        ('CONCLUIDA', 'Concluída'),
        ('CANCELADA', 'Cancelada'),
    )

    sessao_caixa = models.ForeignKey(SessaoCaixa, on_delete=models.PROTECT)
    usuario = models.ForeignKey('Usuario', on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, blank=True, null=True)
    data_hora = models.DateTimeField(default=timezone.now)
    total_bruto = models.DecimalField(max_digits=10, decimal_places=2)
    desconto_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_liquido = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='CONCLUIDA')

    def __str__(self):
        return f"Venda {self.id}"

class Item_Venda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.produto.nome} ({self.quantidade})"

class Pagamento(models.Model):

    FORMA_CHOICES = (
        ('DINHEIRO', 'Dinheiro'),
        ('PIX', 'PIX'),
        ('CARTAO', 'Cartão'),
    )

    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='pagamentos')
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_CHOICES)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.forma_pagamento} - {self.valor_pago}"

class Auditoria_Log(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.PROTECT)
    acao = models.CharField(max_length=100)
    tabela_afetada = models.CharField(max_length=50)
    registro_id = models.IntegerField()
    valor_antigo = models.TextField(blank=True, null=True)
    valor_novo = models.TextField(blank=True, null=True)
    justificativa = models.TextField()
    data_hora = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.acao