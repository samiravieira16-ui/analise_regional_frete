import pandas as pd
import os

def limpar_colunas_csvs(data_path='data/'):
    """
    Este script carrega os 4 arquivos CSV essenciais para o projeto
    e remove todas as colunas desnecessárias, mantendo apenas as chaves
    de ligação (IDs), estados (para cálculo de região), preço e frete.
    """
    print("Iniciando limpeza dos dados...")

    # 1. Itens do pedido
    items_file = os.path.join(data_path, 'Conjunto_de_dados_de_itens_do_pedido.csv')
    if os.path.exists(items_file):
        print(f"Limpando colunas de: {items_file}")
        df_items = pd.read_csv(items_file)
        cols_items = ['order_id', 'seller_id', 'price', 'freight_value']
        df_items = df_items[cols_items]
        df_items.to_csv(items_file, index=False)
    else:
        print(f"Arquivo não encontrado: {items_file}")

    # 2. Pedidos
    orders_file = os.path.join(data_path, 'Conjunto_de_dados_de_pedidos.csv')
    if os.path.exists(orders_file):
        print(f"Limpando colunas de: {orders_file}")
        df_orders = pd.read_csv(orders_file)
        cols_orders = ['order_id', 'customer_id']
        df_orders = df_orders[cols_orders]
        df_orders.to_csv(orders_file, index=False)
    else:
        print(f"Arquivo não encontrado: {orders_file}")

    # 3. Clientes
    customers_file = os.path.join(data_path, 'Conjunto_de_dados_de_clientes.csv')
    if os.path.exists(customers_file):
        print(f"Limpando colunas de: {customers_file}")
        df_customers = pd.read_csv(customers_file)
        cols_customers = ['customer_id', 'customer_state']
        df_customers = df_customers[cols_customers]
        df_customers.to_csv(customers_file, index=False)
    else:
        print(f"Arquivo não encontrado: {customers_file}")

    # 4. Vendedores
    sellers_file = os.path.join(data_path, 'Conjunto_de_dados_de_vendedores.csv')
    if os.path.exists(sellers_file):
        print(f"Limpando colunas de: {sellers_file}")
        df_sellers = pd.read_csv(sellers_file)
        cols_sellers = ['seller_id', 'seller_state']
        df_sellers = df_sellers[cols_sellers]
        df_sellers.to_csv(sellers_file, index=False)
    else:
        print(f"Arquivo não encontrado: {sellers_file}")

    print("Limpeza concluída com sucesso! Os arquivos CSV originais foram sobrescritos com as versões otimizadas.")

if __name__ == "__main__":
    limpar_colunas_csvs()
