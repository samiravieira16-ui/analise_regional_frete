import pandas as pd
import os

def executar_limpeza_passo_a_passo(data_path='data/'):
    """
    Script de Limpeza de Dados (Refatorado)
    Passo a passo documentado estritamente conforme o Relatório de Limpeza de Dados.
    """
    base_url = "https://raw.githubusercontent.com/samiravieira16-ui/analise_regional_frete/main/data/"
    print("Iniciando a limpeza passo a passo dos dados...\n")

    # ==========================================
    # PASSO 1 e 2: ARQUIVOS ORIGINAIS E SELEÇÃO
    # ==========================================
    print("PASSO 1 e 2: Seleção de Arquivos (Deleção de 5 irrelevantes)")
    print("Dos 9 arquivos originais, os seguintes 5 arquivos focados em avaliações, "
          "pagamentos e categorias foram ignorados (deletados da análise):")
    arquivos_ignorados = [
        "olist_order_reviews_dataset.csv", 
        "olist_order_payments_dataset.csv",
        "olist_products_dataset.csv", 
        "olist_sellers_dataset.csv (informações extras)", 
        "product_category_name_translation.csv"
    ]
    for arq in arquivos_ignorados:
        print(f"  - Descartado: {arq}")
    
    print("\nPASSO 3: Ficaram apenas os 4 arquivos primordiais (Clientes, Pedidos, Itens, Vendedores).")

    arquivos_primordiais = {
        'Conjunto_de_dados_de_clientes.csv': 'Clientes',
        'Conjunto_de_dados_de_pedidos.csv': 'Pedidos',
        'Conjunto_de_dados_de_itens_do_pedido.csv': 'Itens do Pedido',
        'Conjunto_de_dados_de_vendedores.csv': 'Vendedores'
    }

    # ==========================================
    # PASSO 4 e 5: FILTRAGEM INTERNA E TRADUÇÃO
    # ==========================================
    print("\nPASSO 4 e 5: Filtragem Interna, Descarte de Colunas Inúteis e Tradução")
    
    # Dicionário mapeando os arquivos para as únicas colunas essenciais que manteremos (e suas traduções)
    # Isso automaticamente descarta status, datas, descrições longas, limites, etc.
    colunas_essenciais_e_traducoes = {
        'Conjunto_de_dados_de_clientes.csv': {
            'customer_id': 'cliente_id', 
            'customer_state': 'estado_cliente'
        },
        'Conjunto_de_dados_de_pedidos.csv': {
            'order_id': 'pedido_id', 
            'customer_id': 'cliente_id'
        },
        'Conjunto_de_dados_de_itens_do_pedido.csv': {
            'order_id': 'pedido_id', 
            'seller_id': 'vendedor_id', 
            'price': 'preco', 
            'freight_value': 'valor_frete'
        },
        'Conjunto_de_dados_de_vendedores.csv': {
            'seller_id': 'vendedor_id', 
            'seller_state': 'estado_vendedor'
        }
    }

    if not os.path.exists(data_path):
        os.makedirs(data_path)

    for arquivo, nome_br in arquivos_primordiais.items():
        print(f"\nProcessando arquivo: {nome_br} ({arquivo})")
        arquivo_local = os.path.join(data_path, arquivo)
        
        try:
            # Baixando arquivo remoto
            df = pd.read_csv(f"{base_url}{arquivo}")
            
            # Obtendo as colunas essenciais e a tradução correspondente
            mapa_traducoes = colunas_essenciais_e_traducoes[arquivo]
            colunas_essenciais = list(mapa_traducoes.keys())
            colunas_traduzidas = list(mapa_traducoes.values())
            
            # Algumas bases podem já estar com a coluna em português
            colunas_presentes_en = [col for col in colunas_essenciais if col in df.columns]
            colunas_presentes_pt = [col for col in colunas_traduzidas if col in df.columns]

            if colunas_presentes_en:
                # PASSO 4: Descartar colunas inúteis
                df = df[colunas_presentes_en]
                # PASSO 5 e 1: Traduzir para português
                df = df.rename(columns=mapa_traducoes)
                print(f"  ✓ Colunas inúteis descartadas.")
                print(f"  ✓ Colunas essenciais mantidas e traduzidas: {list(df.columns)}")
                df.to_csv(arquivo_local, index=False)
            
            elif colunas_presentes_pt:
                # Já estava traduzido
                df = df[colunas_presentes_pt]
                print(f"  ✓ Colunas inúteis descartadas.")
                print(f"  ✓ Colunas essenciais mantidas (já em PT): {list(df.columns)}")
                df.to_csv(arquivo_local, index=False)
                
            else:
                print(f"  ⚠ Não foi possível encontrar colunas vitais no arquivo.")
        
        except Exception as e:
            print(f"  ⚠ Erro ao processar {arquivo}: {e}")

    print("\n===========================================")
    print("Processo de Limpeza de Dados Finalizado!")
    print("===========================================")

if __name__ == "__main__":
    executar_limpeza_passo_a_passo()
