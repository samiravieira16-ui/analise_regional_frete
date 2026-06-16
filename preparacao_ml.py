import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Importa a função de carregamento já pronta do nosso outro script
from analise_regional import carregar_e_processar_dados

def preparar_dados_para_ml():
    """
    Carrega o dataset, seleciona as features relevantes,
    converte variáveis categóricas, normaliza e divide em Treino e Teste.
    """
    print("Carregando e processando os dados iniciais...")
    df = carregar_e_processar_dados()
    
    # --- DEFINIÇÃO DE FEATURES (X) E TARGET (y) ---
    # Queremos prever o 'tipo_compra' (Intra-Regional vs Inter-Regional).
    # Não podemos incluir as colunas 'regiao_cliente' e 'regiao_vendedor' nas features,
    # pois o tipo_compra é 100% derivado delas (se forem iguais é Intra, senão Inter).
    # Se incluirmos, o modelo "trapaceia" e não precisa aprender nada.
    # Vamos usar apenas os valores numéricos para ver se o preço e frete indicam o tipo da compra.
    
    cols_features = ['preco', 'valor_frete', 'ratio_frete_preco']
    
    # Remover linhas onde ratio_frete_preco não pôde ser calculado (divisão por zero) ou NaN
    df_ml = df.dropna(subset=cols_features + ['tipo_compra'])
    
    X = df_ml[cols_features].copy()
    y_bruto = df_ml['tipo_compra'].copy()
    
    print("\nResumo das Features (X):")
    print(X.head())
    
    # --- CONVERSÃO CATEGÓRICA DO TARGET ---
    # O modelo de Deep Learning precisa de números, não de strings.
    # Intra-Regional = 1, Inter-Regional = 0
    le = LabelEncoder()
    y = le.fit_transform(y_bruto)
    print(f"\nClasses do Target (0 e 1): {le.classes_}")
    
    # --- NORMALIZAÇÃO DAS FEATURES ---
    # Deep Learning (Redes Neurais) convergem muito mais rápido se os dados
    # estiverem na mesma escala (geralmente entre 0 e 1, ou média 0 e desvio 1).
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Transformando de volta para DataFrame para manter os nomes das colunas
    X_scaled = pd.DataFrame(X_scaled, columns=cols_features)
    
    # --- DIVISÃO TREINO / TESTE ---
    print("\nRealizando o Train/Test Split (80% Treino, 20% Teste)...")
    X_treino, X_teste, y_treino, y_teste = train_test_split(
        X_scaled, y, test_size=0.20, random_state=42, stratify=y
    )
    
    print(f"Tamanho do Conjunto de Treino: {len(X_treino)} exemplos")
    print(f"Tamanho do Conjunto de Teste: {len(X_teste)} exemplos")
    
    # --- EXPORTAÇÃO DOS ARQUIVOS ---
    os.makedirs('outputs', exist_ok=True)
    
    # Concatenar X e y para salvar em arquivos mais práticos, ou salvar separado.
    # Vamos salvar separadamente que é o padrão da indústria.
    X_treino.to_csv('outputs/X_treino.csv', index=False)
    X_teste.to_csv('outputs/X_teste.csv', index=False)
    
    # y é um array numpy, vamos converter para DataFrame para salvar facilmente
    pd.DataFrame({'tipo_compra_codificado': y_treino}).to_csv('outputs/y_treino.csv', index=False)
    pd.DataFrame({'tipo_compra_codificado': y_teste}).to_csv('outputs/y_teste.csv', index=False)
    
    print("\nDados separados e exportados com sucesso na pasta 'outputs/'!")
    print("- outputs/X_treino.csv")
    print("- outputs/X_teste.csv")
    print("- outputs/y_treino.csv")
    print("- outputs/y_teste.csv")

if __name__ == '__main__':
    preparar_dados_para_ml()
