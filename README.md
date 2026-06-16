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

### Dependências Principais
- **pandas** — Manipulação e análise de dados
- **numpy** — Computação numérica
- **matplotlib & seaborn** — Visualizações
- **scikit-learn** — Machine Learning e pré-processamento
- **joblib** — Serialização de modelos

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

## Execução do Projeto

### Passo 1: Análise Exploratória
Execute o script principal para gerar análises e visualizações:

```bash
python analise_regional.py
```

**Saídas geradas:**
- `outputs/fluxo_regional.csv` — Matriz de fluxo de compras entre regiões
- `outputs/influencia_frete.csv` — Análise da influência do frete
- Gráficos e visualizações no formato PNG

### Passo 2: Preparação de Dados para Machine Learning
Execute o script de preparação para gerar os conjuntos de treino e teste:

```bash
python outputs/preparacao_ml.py
```

**Saídas geradas:**
- `outputs/X_treino.csv` — Features do conjunto de treino
- `outputs/X_teste.csv` — Features do conjunto de teste
- `outputs/y_treino.csv` — Target do conjunto de treino
- `outputs/y_teste.csv` — Target do conjunto de teste

### Passo 3: Treinamento do Modelo Deep Learning
Execute o modelo de Rede Neural para prever padrões de compra:

```bash
python outputs/modelo_dl.py
```

**Saídas geradas:**
- Acurácia e métricas de desempenho do modelo
- Matriz de confusão
- Relatório de classificação

---

## Estrutura do Projeto

```
analise_regional_frete/
│
├── analise_regional.py     # Script principal com análises exploratórias e visualizações
│
├── src/
│   ├── __init__.py
│   └── utils.py            # Mapeamento de estados para regiões do Brasil
│
├── data/                   # (não versionada) CSVs do dataset Olist
│   ├── Conjunto_de_dados_de_pedidos.csv
│   ├── Conjunto_de_dados_de_itens_do_pedido.csv
│   ├── Conjunto_de_dados_de_clientes.csv
│   ├── Conjunto_de_dados_de_vendedores.csv
│   └── limpeza_dados.py    # Script de limpeza e processamento dos dados brutos
│
├── outputs/                # (gerada ao executar) Resultados e modelos
│   ├── analise_regional.py        # Análise exploratória
│   ├── preparacao_ml.py           # Preparação dos dados para Machine Learning
│   ├── modelo_dl.py               # Treinamento do modelo Deep Learning (MLP)
│   │
│   ├── fluxo_regional.csv         # Matriz de fluxo intra/inter-regional
│   ├── influencia_frete.csv       # Análise da influência do frete por região
│   │
│   ├── X_treino.csv               # Features do conjunto de treino
│   ├── X_teste.csv                # Features do conjunto de teste
│   ├── y_treino.csv               # Target do conjunto de treino
│   └── y_teste.csv                # Target do conjunto de teste
│
├── LICENSE
├── README.md
└── requirements.txt
```

---

## Pipeline Completo do Projeto

O projeto segue um pipeline em 3 etapas:

### 1. **Análise Exploratória** (`analise_regional.py`)
- Carregamento e limpeza dos dados
- Análise do fluxo regional de compras
- Avaliação da influência do frete nos padrões de compra
- Geração de visualizações e exportação de resultados em CSV

### 2. **Preparação para Machine Learning** (`preparacao_ml.py`)
- Seleção de features relevantes: preço, valor do frete, ratio frete/preço
- Codificação do target (tipo de compra: Intra vs Inter-Regional)
- Normalização dos dados com StandardScaler
- Divisão em conjuntos de treino (80%) e teste (20%)

### 3. **Modelo de Deep Learning** (`modelo_dl.py`)
- Treinamento de uma **Rede Neural Artificial (MLP)** com:
  - 2 camadas ocultas (16 e 8 neurônios)
  - Função de ativação ReLU
  - Otimizador Adam
  - Early stopping para evitar overfitting
- Avaliação de desempenho no conjunto de teste
- Relatório de métricas: Acurácia, Matriz de Confusão, Classificação Detalhada

---

## Resultados Esperados

Ao executar o projeto completo, você obtém:

| Resultado | Descrição |
|---|---|
| `fluxo_regional.csv` | Proporção de compras intra vs inter-regionais por região |
| `influencia_frete.csv` | Correlação entre frete e tipo de compra |
| Visualizações | Gráficos de análise exploratória |
| Dados ML | Conjuntos de treino/teste normalizados |
| Modelo Treinado | Rede Neural com acurácia reportada |

---

## Tecnologias Utilizadas

- **Análise de Dados:** pandas, numpy
- **Visualizações:** matplotlib, seaborn
- **Machine Learning:** scikit-learn
- **Deep Learning:** scikit-learn MLPClassifier
- **Versionamento:** Git & GitHub

---

## Conceitos Principais

### Compras Intra vs Inter-Regionais
- **Intra-Regional:** Comprador e vendedor na mesma região (ex: cliente SP comprando de vendedor SP)
- **Inter-Regional:** Comprador e vendedor em regiões diferentes (ex: cliente SP comprando de vendedor SP)

### Features do Modelo
1. **Preço** — Valor do produto
2. **Valor do Frete** — Custo de envio
3. **Ratio Frete/Preço** — Proporção do frete em relação ao preço

### Target do Modelo
- **0:** Compra Inter-Regional
- **1:** Compra Intra-Regional

---

## Autor

**Samira Vieira** - Análise de dados e Machine Learning  
GitHub: [@samiravieira16-ui](https://github.com/samiravieira16-ui)

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

## Referências

- [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- [Documentação scikit-learn](https://scikit-learn.org/)
- [Documentação pandas](https://pandas.pydata.org/)
```
