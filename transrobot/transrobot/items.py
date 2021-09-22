# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class TransrobotItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PaymentItem(Item):
    data = Field()
    empenho = Field()
    parcela = Field()
    tipo = Field()
    favorecido = Field()
    valor = Field()

class PaymentDetailedItem (Item):
    tipo = Field()
    num_empenho = Field()
    tipo_empenho = Field()
    especie_empenho = Field()
    unidade_jurisdicionada = Field()
    unidade_orcamentaria = Field()
    historico_empenho = Field()
    data_empenho = Field()
    cpf_cnpj = Field()
    nome_razao_social = Field()
    funcao = Field()
    subfuncao = Field()
    programa = Field()
    acao = Field()
    categoria_economica = Field()
    grupo_despesa = Field()
    modalidade_aplicacao = Field()
    elemento_despesa = Field()
    subelemento_despesa = Field()
    licitacao_modalidade = Field()
    licitacao_sequencial_modalidade = Field()
