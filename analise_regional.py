import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
from src.utils import get_region
# ==============================================================================
# CARGA E PROCESSAMENTO DOS DADOS
# ==============================================================================

def carregar_e_processar_dados(data_path='data/'):
    print("Carregando datasets...")
    
    files = {
        'orders': 'Conjunto_de_dados_de_pedidos.csv',
        'items': 'Conjunto_de_dados_de_itens_do_pedido.csv',
        'customers': 'Conjunto_de_dados_de_clientes.csv',
        'sellers': 'Conjunto_de_dados_de_vendedores.csv'
    }
    
    for key, filename in files.items():
        if not os.path.exists(os.path.join(data_path, filename)):
            raise FileNotFoundError(f"Arquivo '{filename}' não encontrado em '{data_path}'")
    
    df_orders   = pd.read_csv(os.path.join(data_path, files['orders']))
    df_items    = pd.read_csv(os.path.join(data_path, files['items']))
    df_customers= pd.read_csv(os.path.join(data_path, files['customers']))
    df_sellers  = pd.read_csv(os.path.join(data_path, files['sellers']))
    
    print("Mesclando dados...")
    df = pd.merge(df_items,    df_orders,    on='pedido_id')
    df = pd.merge(df,          df_customers, on='cliente_id')
    df = pd.merge(df,          df_sellers,   on='vendedor_id', suffixes=('_cust', '_sell'))
    
    print("Mapeando regiões...")
    df['regiao_cliente'] = df['estado_cliente'].apply(get_region)
    df['regiao_vendedor']   = df['estado_vendedor'].apply(get_region)
    
    # Classificar como INTRA-regional (mesma região) ou INTER-regional (regiões diferentes)
    df['tipo_compra'] = np.where(
        df['regiao_cliente'] == df['regiao_vendedor'],
        'Intra-Regional',
        'Inter-Regional'
    )
    
    # Calcular ratio frete/preço do produto (percentual que o frete representa no preço)
    df['ratio_frete_preco'] = (df['valor_frete'] / df['preco'].replace(0, np.nan)) * 100
    
    return df


# ==============================================================================
# ANÁLISE 1: PERCENTUAL DE COMPRAS INTRA vs INTER-REGIONAL
# ==============================================================================

def analise_percentual_compras(df):
    """
    Calcula a % de compras dentro da mesma região (intra) vs fora (inter).
    Também detalha, por região do comprador, de onde ele mais compra.
    """
    # --- Visão Geral ---
    total_geral = len(df)
    resumo_geral = df['tipo_compra'].value_counts().reset_index()
    resumo_geral.columns = ['tipo_compra', 'total']
    resumo_geral['percentual (%)'] = (resumo_geral['total'] / total_geral * 100).round(2)

    print("\n" + "="*60)
    print("ANÁLISE 1: Compras Intra-Regional vs Inter-Regional (Geral)")
    print("="*60)
    print(resumo_geral.to_string(index=False))

    # --- Detalhado por Região do Comprador ---
    por_regiao = df.groupby(['regiao_cliente', 'tipo_compra']).size().reset_index(name='total')
    total_por_regiao = por_regiao.groupby('regiao_cliente')['total'].transform('sum')
    por_regiao['percentual (%)'] = (por_regiao['total'] / total_por_regiao * 100).round(2)

    print("\n--- Detalhado por Região do Comprador ---")
    print(por_regiao.sort_values(['regiao_cliente', 'tipo_compra']).to_string(index=False))
    
    return resumo_geral, por_regiao


# ==============================================================================
# ANÁLISE 2: FRETE E VOLUME POR FLUXO REGIONAL
# ==============================================================================

def analise_fluxo_e_frete(df):
    """Calcula frete médio e volume de vendas por cada par (vendedor -> comprador)."""
    fluxo = df.groupby(['regiao_vendedor', 'regiao_cliente']).agg(
        total_vendas = ('pedido_id', 'count'),
        frete_medio  = ('valor_frete', 'mean'),
        preco_medio  = ('preco', 'mean'),
        ratio_medio  = ('ratio_frete_preco', 'mean')
    ).reset_index()
    
    total = fluxo['total_vendas'].sum()
    fluxo['perc_total (%)'] = (fluxo['total_vendas'] / total * 100).round(2)
    
    print("\n" + "="*60)
    print("ANÁLISE 2: Fluxo de Frete entre Regiões (Top 10 por volume)")
    print("="*60)
    print(fluxo.sort_values('total_vendas', ascending=False).head(10).to_string(index=False))
    
    return fluxo


# ==============================================================================
# ANÁLISE 3: FRETE COMO FATOR DE ESCOLHA POR PROXIMIDADE
# ==============================================================================

def analise_influencia_frete_proximidade(df):
    """
    Compara o ratio frete/preço médio para compras intra vs inter-regional,
    por região do comprador. Responde: o frete mais baixo induz o cliente
    a comprar de vendedores mais próximos?
    """
    comparacao = df.groupby(['regiao_cliente', 'tipo_compra']).agg(
        frete_medio         = ('valor_frete', 'mean'),
        ratio_frete_preco   = ('ratio_frete_preco', 'mean'),
        total_pedidos       = ('pedido_id', 'count')
    ).reset_index()
    
    print("\n" + "="*60)
    print("ANÁLISE 3: Frete Médio e Ratio Frete/Preço (Intra vs Inter)")
    print("Quanto maior o ratio, mais o frete 'pesa' no preço final.")
    print("="*60)
    print(comparacao.sort_values(['customer_region', 'tipo_compra']).to_string(index=False))
    
    return comparacao


# ==============================================================================
# VISUALIZAÇÕES
# ==============================================================================

def plotar_todas_visualizacoes(resumo_geral, por_regiao, fluxo, comparacao):
    
    sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
    os.makedirs('outputs', exist_ok=True)

    # ---- FIG 1: Pizza + Barras empilhadas ----
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Análise 1: Compras Intra vs Inter-Regional', fontsize=14, fontweight='bold')

    # Pizza geral
    axes[0].pie(resumo_geral['percentual (%)'], labels=resumo_geral['tipo_compra'],
                autopct='%1.1f%%', startangle=90,
                colors=['#4CAF50', '#FF7043'], wedgeprops=dict(edgecolor='white', linewidth=2))
    axes[0].set_title('Proporção Geral de Compras')

    # Barras empilhadas por região do comprador
    pivot = por_regiao.pivot(index='regiao_cliente', columns='tipo_compra', values='percentual (%)').fillna(0)
    pivot.plot(kind='bar', stacked=True, ax=axes[1], color=['#4CAF50', '#FF7043'], edgecolor='white')
    axes[1].set_title('Percentual por Região do Comprador')
    axes[1].set_xlabel('Região do Comprador')
    axes[1].set_ylabel('Percentual (%)')
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=30, ha='right')
    axes[1].yaxis.set_major_formatter(mticker.PercentFormatter())
    axes[1].legend(title='Tipo de Compra')

    plt.tight_layout()
    plt.savefig('outputs/analise1_percentual_compras.png', dpi=150)
    print("\nSalvo: outputs/analise1_percentual_compras.png")

    # ---- FIG 2: Heatmaps de Volume e Frete ----
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Análise 2: Heatmaps de Fluxo Regional', fontsize=14, fontweight='bold')

    matrix_vendas = fluxo.pivot(index='regiao_vendedor', columns='regiao_cliente', values='perc_total (%)').fillna(0)
    sns.heatmap(matrix_vendas, annot=True, fmt=".1f", cmap="YlGnBu", ax=axes[0],
                linewidths=.5, cbar_kws={'label': '% do Total'})
    axes[0].set_title('% de Pedidos por Fluxo\n(Linha: Vendedor | Coluna: Comprador)')
    axes[0].set_xlabel('Região do Comprador')
    axes[0].set_ylabel('Região do Vendedor')

    matrix_frete = fluxo.pivot(index='regiao_vendedor', columns='regiao_cliente', values='frete_medio').fillna(0)
    sns.heatmap(matrix_frete, annot=True, fmt=".2f", cmap="Reds", ax=axes[1],
                linewidths=.5, cbar_kws={'label': 'R$ Frete Médio'})
    axes[1].set_title('Frete Médio (R$) por Fluxo\n(Linha: Vendedor | Coluna: Comprador)')
    axes[1].set_xlabel('Região do Comprador')
    axes[1].set_ylabel('Região do Vendedor')

    plt.tight_layout()
    plt.savefig('outputs/analise2_heatmaps_fluxo_frete.png', dpi=150)
    print("Salvo: outputs/analise2_heatmaps_fluxo_frete.png")

    # ---- FIG 3: Frete e Ratio Intra vs Inter ----
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Análise 3: Influência do Frete na Escolha por Proximidade', fontsize=14, fontweight='bold')

    # Frete médio por tipo de compra e região
    pivot_frete = comparacao.pivot(index='regiao_cliente', columns='tipo_compra', values='frete_medio').fillna(0)
    pivot_frete.plot(kind='bar', ax=axes[0], color=['#1565C0', '#EF6C00'], edgecolor='white', width=0.7)
    axes[0].set_title('Frete Médio (R$): Intra vs Inter por Região')
    axes[0].set_xlabel('Região do Comprador')
    axes[0].set_ylabel('Frete Médio (R$)')
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=30, ha='right')
    axes[0].legend(title='Tipo de Compra')

    # Ratio frete/preço por tipo de compra e região
    pivot_ratio = comparacao.pivot(index='regiao_cliente', columns='tipo_compra', values='ratio_frete_preco').fillna(0)
    pivot_ratio.plot(kind='bar', ax=axes[1], color=['#1565C0', '#EF6C00'], edgecolor='white', width=0.7)
    axes[1].set_title('Frete como % do Preço do Produto\nIntra vs Inter por Região')
    axes[1].set_xlabel('Região do Comprador')
    axes[1].set_ylabel('Frete / Preço (%)')
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=30, ha='right')
    axes[1].legend(title='Tipo de Compra')

    plt.tight_layout()
    plt.savefig('outputs/analise3_influencia_frete_proximidade.png', dpi=150)
    print("Salvo: outputs/analise3_influencia_frete_proximidade.png")


# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================

if __name__ == "__main__":
    try:
        df = carregar_e_processar_dados()

        resumo_geral, por_regiao = analise_percentual_compras(df)
        fluxo                    = analise_fluxo_e_frete(df)
        comparacao               = analise_influencia_frete_proximidade(df)

        plotar_todas_visualizacoes(resumo_geral, por_regiao, fluxo, comparacao)

        # Exportar resultados em CSV para uso posterior no modelo de Deep Learning
        os.makedirs('outputs', exist_ok=True)
        fluxo.to_csv('outputs/fluxo_regional.csv', index=False)
        comparacao.to_csv('outputs/influencia_frete.csv', index=False)
        print("\nCSVs de resultado salvos em 'outputs/'.")
        
    except FileNotFoundError as e:
        print(f"\nERRO: {e}")
        print("Baixe o dataset em https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce")
        print("e coloque os arquivos CSV na pasta 'data/' do projeto.")
