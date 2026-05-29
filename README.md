# Análise Regional de Frete no E-commerce Brasileiro

## Tema e Problema

O custo do frete é um dos principais fatores que influenciam o comportamento de compra online no Brasil. Neste projeto, investigamos se o valor do frete impacta o padrão de fluxo de compras entre as regiões brasileiras — ou seja, se consumidores tendem a comprar de vendedores da mesma região quando o frete é mais barato (compras **intra-regionais**) em comparação com compras de outras regiões (**inter-regionais**).

A etapa final do projeto aplica técnicas de **Deep Learning** para prever padrões de consumo com base nas características logísticas e regionais identificadas nas análises exploratórias.

---

## Base de Dados

Este projeto utiliza o dataset público **[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)**, disponível no Kaggle.

Os arquivos utilizados são:

| Arquivo | Descrição |
|---|---|
| `olist_orders_dataset.csv` | Informações sobre os pedidos realizados |
| `olist_order_items_dataset.csv` | Itens de cada pedido (preço, frete, vendedor) |
| `olist_customers_dataset.csv` | Localização dos clientes (estado) |
| `olist_sellers_dataset.csv` | Localização dos vendedores (estado) |

> **Como configurar:** Baixe o dataset no Kaggle e coloque os arquivos CSV na pasta `data/` do projeto.

---

## Objetivos do Projeto

1. **Mapear o fluxo regional de compras** — identificar a proporção de pedidos intra-regionais vs. inter-regionais por região do comprador.
2. **Analisar o papel do frete** — comparar o frete médio e o ratio frete/preço entre compras intra e inter-regionais para cada região.
3. **Identificar padrões logísticos** — determinar os fluxos de maior volume (vendedor → comprador) e os trajetos com maior custo de frete.
4. **Prever padrões de consumo com Deep Learning** — utilizar as variáveis logísticas e regionais para treinar um modelo preditivo de comportamento de compra.

---

## Instalação

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/samiravieira16-ui/analise_regional_frete.git
   cd analise_regional_frete
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure os dados:**
   - Baixe o dataset em [Kaggle - Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
   - Coloque os arquivos CSV na pasta `data/`:
     ```
     data/
     ├── Conjunto_de_dados_de_pedidos.csv
     ├── Conjunto_de_dados_de_itens_do_pedido.csv
     ├── Conjunto_de_dados_de_clientes.csv
     └── Conjunto_de_dados_de_vendedores.csv
     ```

4. **Execute a análise:**
   ```bash
   python analise_regional.py
   ```

Os resultados (gráficos e CSVs) serão gerados na pasta `outputs/`.

---

## Estrutura do Projeto

```
analise_regional_frete/
│
├── analise_regional.py     # Script principal com todas as análises e visualizações
│
├── src/
│   └── utils.py            # Mapeamento de estados para regiões do Brasil
│
├── data/                   # (não versionada) CSVs do dataset Olist
│   ├── olist_orders_dataset.csv  # Conjunto_de_dados_de_pedidos
│   ├── olist_order_items_dataset.csv # Conjunto_de_dados_de_itens_do_pedido
│   ├── olist_customers_dataset.csv  # Conjunto_de_dados_de_clientes
│   └── olist_sellers_dataset.csv  # Conjunto_de_dados_de_vendedores
│
├── outputs/                # (gerada ao executar) Gráficos e CSVs de resultado
│   ├── analise1_percentual_compras.png
│   ├── analise2_heatmaps_fluxo_frete.png
│   ├── analise3_influencia_frete_proximidade.png
│   ├── fluxo_regional.csv
│   └── influencia_frete.csv
│
├── LICENSE
└── README.md
```
