from django.contrib import admin
from .models import (
    Usuario, Categoria, Produto, Movimentacao_Estoque,
    Cliente, Sessao_Caixa, Venda, Item_Venda, Pagamento, Auditoria_Log
)

# --- Inlines para uma gestão visual melhor ---

class Item_Venda_Inline(admin.TabularInline):
    model = Item_Venda
    extra = 0
    readonly_fields = ('subtotal',)

class Pagamento_Inline(admin.TabularInline):
    model = Pagamento
    extra = 0

# --- Configurações das Classes Admin ---

@admin.register(Usuario)
class Usuario_Admin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'perfil', 'ativo', 'criado_em')
    list_filter = ('perfil', 'ativo')
    search_fields = ('nome', 'email')

@admin.register(Produto)
class Produto_Admin(admin.ModelAdmin):
    list_display = ('nome', 'sku', 'preco_venda', 'estoque_atual', 'categoria', 'ativo')
    list_filter = ('categoria', 'ativo')
    search_fields = ('nome', 'sku', 'codigo_barras')
    list_editable = ('preco_venda', 'ativo')

@admin.register(Venda)
class Venda_Admin(admin.ModelAdmin):
    list_display = ('id', 'data_hora', 'usuario', 'cliente', 'total_liquido', 'status')
    list_filter = ('status', 'data_hora', 'usuario')
    search_fields = ('id', 'cliente__nome', 'usuario__username')
    readonly_fields = ('total_bruto', 'total_liquido', 'data_hora')
    inlines = [Item_Venda_Inline, Pagamento_Inline]
    
    # Organizando os campos no formulário de edição
    fieldsets = (
        ('Informações da Venda', {
            'fields': ('sessao_caixa', 'usuario', 'cliente', 'status')
        }),
        ('Valores', {
            'fields': ('total_bruto', 'desconto_total', 'total_liquido')
        }),
    )

@admin.register(Sessao_Caixa)
class Sessao_CaixaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'data_abertura', 'status', 'valor_final_sistema')
    list_filter = ('status', 'data_abertura')

@admin.register(Movimentacao_Estoque)
class Movimentacao_EstoqueAdmin(admin.ModelAdmin):
    list_display = ('produto', 'quantidade', 'tipo', 'usuario', 'data_hora')
    list_filter = ('tipo', 'data_hora')
    search_fields = ('produto_nome', 'motivo')

@admin.register(Auditoria_Log)
class Auditoria_LogAdmin(admin.ModelAdmin):
    list_display = ('data_hora', 'usuario', 'acao', 'tabela_afetada', 'registro_id')
    readonly_fields = ('data_hora', 'usuario', 'acao', 'tabela_afetada', 'registro_id', 'valor_antigo', 'valor_novo', 'justificativa')
    
    def has_add_permission(self, request): return False # Logs não devem ser criados manualmente

# Registro simples para as demais tabelas
admin.site.register(Categoria)
admin.site.register(Cliente)