# Crawler - Portal da Transparência de Sta Cruz do Capibaribe, PE

Esse crawler foi feito com o intuito de extrair as informações de despesas
diárias > pagamentos da prefeitura de Santa Cruz do Capibaribe. Por existir uma
limitação no tempo de permanência no site, imposto pela empresa Tenosoft que,
fornece fornece o software, esse crawler precisa ser rodado em buckets para
conseguir extrair todo o histórico de informação. Para extrair as informações
de pagamento, podem ser usados buckets de tamanho 10k, já para extrair as
informações detalhadas o tamanho máximo do bucket que conseguimos usar foi de
apenas 410.

Nesse projeto temos dois spiders implementados, o payments e o detail, que
capturam respectivamente as informações de pagamento, e o detalhe desse
pagamento.

## Pré-requisitos

Para rodar o projeto, é necessário ter o [virtualenv](https://docs.python.org/3/library/venv.html) do Python, e o [Scrapy](https://scrapy.org/)
instalados.

## Executando o projeto

Para executar o projeto, você deve primeiro ativar o ambiente virtual. Na raíz
do projeto do github, execute:

```
$ source tcc-env/bin/activate
```

Depois vá para o diretório raíz do crawler.

```
$ cd transbot/
```

Para executar o Spider payments, faça:

```
scrapy crawl payments -o payments.csv
```

O comando acima irá executar o spider e em seguida gerar um arquivo csv
(de nome payments.csv) com os dados extraídos da página. Para executar o spider
detail é só usar o mesmo comando acima, substituindo payments por detail.
