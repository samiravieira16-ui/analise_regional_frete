import pandas as pd
import os

def limpar_colunas_csvs(data_path='data/'):
    """
    Este script carrega os 4 arquivos CSV essenciais para o projeto
    e remove todas as colunas desnecessárias, mantendo apenas as chaves
    de ligação (IDs), estados (para cálculo de região), preço e frete.
    """
    base_url = "https://raw.githubusercontent.com/samiravieira16-ui/analise_regional_frete/main/data/"
    print(f"Iniciando limpeza dos dados obtidos de {base_url}...")

    # 1. Itens do pedido
    items_file = os.path.join(data_path, 'Conjunto_de_dados_de_itens_do_pedido.csv')
    try:
        print(f"Baixando e limpando colunas de: Conjunto_de_dados_de_itens_do_pedido.csv")
        df_items = pd.read_csv(f"{base_url}Conjunto_de_dados_de_itens_do_pedido.csv")
        # Tenta usar colunas em português, se não existir usa inglês
        cols_items = ['pedido_id', 'vendedor_id', 'preco', 'valor_frete'] if 'pedido_id' in df_items.columns else ['order_id', 'seller_id', 'price', 'freight_value']
        cols_items = [col for col in cols_items if col in df_items.columns]
        if cols_items:
            df_items = df_items[cols_items]
            df_items.to_csv(items_file, index=False)
            print(f"  ✓ Colunas mantidas e arquivo salvo localmente: {cols_items}")
    except Exception as e:
        print(f"Erro ao processar: {e}")

    # 2. Pedidos
    orders_file = os.path.join(data_path, 'Conjunto_de_dados_de_pedidos.csv')
    try:
        print(f"Baixando e limpando colunas de: Conjunto_de_dados_de_pedidos.csv")
        df_orders = pd.read_csv(f"{base_url}Conjunto_de_dados_de_pedidos.csv")
        cols_orders = ['pedido_id', 'cliente_id'] if 'pedido_id' in df_orders.columns else ['order_id', 'customer_id']
        cols_orders = [col for col in cols_orders if col in df_orders.columns]
        if cols_orders:
            df_orders = df_orders[cols_orders]
            df_orders.to_csv(orders_file, index=False)
            print(f"  ✓ Colunas mantidas e arquivo salvo localmente: {cols_orders}")
    except Exception as e:
        print(f"Erro ao processar: {e}")

    # 3. Clientes
    customers_file = os.path.join(data_path, 'Conjunto_de_dados_de_clientes.csv')
    try:
        print(f"Baixando e limpando colunas de: Conjunto_de_dados_de_clientes.csv")
        df_customers = pd.read_csv(f"{base_url}Conjunto_de_dados_de_clientes.csv")
        cols_customers = ['cliente_id', 'estado_cliente'] if 'cliente_id' in df_customers.columns else ['customer_id', 'customer_state']
        cols_customers = [col for col in cols_customers if col in df_customers.columns]
        if cols_customers:
            df_customers = df_customers[cols_customers]
            df_customers.to_csv(customers_file, index=False)
            print(f"  ✓ Colunas mantidas e arquivo salvo localmente: {cols_customers}")
    except Exception as e:
        print(f"Erro ao processar: {e}")

    # 4. Vendedores
    sellers_file = os.path.join(data_path, 'Conjunto_de_dados_de_vendedores.csv')
    try:
        print(f"Baixando e limpando colunas de: Conjunto_de_dados_de_vendedores.csv")
        df_sellers = pd.read_csv(f"{base_url}Conjunto_de_dados_de_vendedores.csv")
        cols_sellers = ['vendedor_id', 'estado_vendedor'] if 'vendedor_id' in df_sellers.columns else ['seller_id', 'seller_state']
        cols_sellers = [col for col in cols_sellers if col in df_sellers.columns]
        if cols_sellers:
            df_sellers = df_sellers[cols_sellers]
            df_sellers.to_csv(sellers_file, index=False)
            print(f"  ✓ Colunas mantidas e arquivo salvo localmente: {cols_sellers}")
    except Exception as e:
        print(f"Erro ao processar: {e}")

    print("Limpeza concluída com sucesso!")


def renomear_colunas_para_portugues(data_path='data/'):
    """
    Renomeia as colunas dos CSVs de inglês para português.
    Esta etapa é parte da limpeza e preparação dos dados.
    """
    print("\nRenomeando colunas para português...")

    # Mapeamento de tradução (inglês → português)
    traducoes = {
        'customer_id': 'cliente_id',
        'customer_state': 'estado_cliente',
        'order_id': 'pedido_id',
        'seller_id': 'vendedor_id',
        'price': 'preco',
        'freight_value': 'valor_frete',
        'seller_state': 'estado_vendedor'
    }

    # Lista de arquivos CSV
    arquivos = [
        'Conjunto_de_dados_de_pedidos.csv',
        'Conjunto_de_dados_de_itens_do_pedido.csv',
        'Conjunto_de_dados_de_clientes.csv',
        'Conjunto_de_dados_de_vendedores.csv'
    ]

    base_url = "https://raw.githubusercontent.com/samiravieira16-ui/analise_regional_frete/main/data/"

    # Processar cada arquivo
    for arquivo in arquivos:
        caminho = os.path.join(data_path, arquivo)
        
        try:
            print(f"  Baixando e renomeando colunas: {arquivo}")
            
            # Ler CSV remoto
            df = pd.read_csv(f"{base_url}{arquivo}")
            
            # Renomear apenas as colunas que existem
            renomeacoes = {col: traducoes[col] for col in df.columns if col in traducoes}
            if renomeacoes:
                df = df.rename(columns=renomeacoes)
                df.to_csv(caminho, index=False)
                print(f"    ✓ Colunas renomeadas e salvas localmente: {list(renomeacoes.values())}")
            else:
                print(f"    ℹ Nenhuma coluna para traduzir neste arquivo")
        except Exception as e:
            print(f"  ⚠ Erro ao baixar ou processar {arquivo}: {e}")

    print("Renomeação concluída com sucesso!")



def renomear_colunas_para_portugues(data_path='data/'):
    """
    Renomeia as colunas dos CSVs de inglês para português.
    Esta etapa é parte da limpeza e preparação dos dados.
    """
    print("\nRenomeando colunas para português...")

    # Mapeamento de tradução (inglês → português)
    traducoes = {
        'customer_id': 'cliente_id',
        'customer_state': 'estado_cliente',
        'order_id': 'pedido_id',
        'seller_id': 'vendedor_id',
        'price': 'preco',
        'freight_value': 'valor_frete',
        'seller_state': 'estado_vendedor'
    }

    # Lista de arquivos CSV
    arquivos = [
        'Conjunto_de_dados_de_pedidos.csv',
        'Conjunto_de_dados_de_itens_do_pedido.csv',
        'Conjunto_de_dados_de_clientes.csv',
        'Conjunto_de_dados_de_vendedores.csv'
    ]

    # Processar cada arquivo
    for arquivo in arquivos:
        caminho = os.path.join(data_path, arquivo)
        
        if os.path.exists(caminho):
            print(f"  Renomeando colunas: {arquivo}")
            
            # Ler CSV
            df = pd.read_csv(caminho)
            
            # Renomear apenas as colunas que existem
            renomeacoes = {col: traducoes[col] for col in df.columns if col in traducoes}
            if renomeacoes:
                df = df.rename(columns=renomeacoes)
                df.to_csv(caminho, index=False)
                print(f"    ✓ Colunas renomeadas: {list(renomeacoes.values())}")
            else:
                print(f"    ℹ Nenhuma coluna para traduzir neste arquivo")
        else:
            print(f"  ⚠ Arquivo não encontrado: {arquivo}")

    print("Renomeação concluída com sucesso!")


if __name__ == "__main__":
    limpar_colunas_csvs()
    renomear_colunas_para_portugues()
