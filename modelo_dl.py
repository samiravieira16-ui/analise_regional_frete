import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import joblib

from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

def treinar_modelo_neural():
    print("Carregando os dados de Treino e Teste...")
    
    # Carregar dados
    X_treino = pd.read_csv('outputs/X_treino.csv')
    X_teste = pd.read_csv('outputs/X_teste.csv')
    y_treino = pd.read_csv('outputs/y_treino.csv')['tipo_compra_codificado']
    y_teste = pd.read_csv('outputs/y_teste.csv')['tipo_compra_codificado']
    
    print(f"Dados carregados. Treinando a Rede Neural com {len(X_treino)} exemplos...")
    
    # Definindo a arquitetura da Rede Neural (MLP)
    # hidden_layer_sizes=(16, 8) -> 1 camada oculta com 16 neurônios, 1 camada com 8 neurônios
    # activation='relu' -> Função de ativação padrão para hidden layers
    # solver='adam' -> Otimizador padrão e rápido
    # max_iter=200 -> Número máximo de épocas
    mlp = MLPClassifier(
        hidden_layer_sizes=(16, 8), 
        activation='relu', 
        solver='adam', 
        max_iter=300, 
        random_state=42,
        verbose=True,      # Para imprimir o progresso de cada época
        early_stopping=True # Previne overfitting parando cedo se a loss não melhorar
    )
    
    # Inicia o Treinamento
    mlp.fit(X_treino, y_treino)
    
    print("\nTreinamento Concluído!")
    
    # Previsões no conjunto de teste (onde o modelo nunca viu os dados)
    print("Avaliando o modelo no conjunto de testes...")
    y_pred = mlp.predict(X_teste)
    
    # Métricas de Avaliação
    acuracia = accuracy_score(y_teste, y_pred)
    print(f"\n=============================================")
    print(f"ACURÁCIA FINAL: {acuracia * 100:.2f}%")
    print(f"=============================================\n")
    
    print("Relatório de Classificação Detalhado:")
    print(classification_report(y_teste, y_pred, target_names=['Inter-Regional (0)', 'Intra-Regional (1)']))
    
    # ==========================================
    # VISUALIZAÇÕES
    # ==========================================
    sns.set_theme(style="whitegrid", font_scale=1.1)
    
    # 1. Curva de Loss (Curva de Aprendizagem)
    plt.figure(figsize=(8, 5))
    plt.plot(mlp.loss_curve_, color='blue', linewidth=2)
    plt.title('Curva de Aprendizado (Loss) da Rede Neural', fontsize=14, fontweight='bold')
    plt.xlabel('Épocas (Epochs)')
    plt.ylabel('Loss (Erro)')
    plt.tight_layout()
    plt.savefig('outputs/modelo_loss_curve.png', dpi=150)
    plt.close()
    
    # 2. Matriz de Confusão
    cm = confusion_matrix(y_teste, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=['Inter-Regional (0)', 'Intra-Regional (1)'],
                yticklabels=['Inter-Regional (0)', 'Intra-Regional (1)'])
    plt.title('Matriz de Confusão', fontsize=14, fontweight='bold')
    plt.xlabel('Previsão do Modelo')
    plt.ylabel('Realidade')
    plt.tight_layout()
    plt.savefig('outputs/modelo_matriz_confusao.png', dpi=150)
    plt.close()
    
    print("Gráficos de avaliação salvos em 'outputs/'!")
    print("- outputs/modelo_loss_curve.png")
    print("- outputs/modelo_matriz_confusao.png")
    
    # Salvar o modelo final treinado para ser usado no Artigo/Produção
    joblib.dump(mlp, 'outputs/modelo_mlp_tipo_compra.pkl')
    print("\nModelo treinado salvo com sucesso em 'outputs/modelo_mlp_tipo_compra.pkl'")

if __name__ == '__main__':
    treinar_modelo_neural()
