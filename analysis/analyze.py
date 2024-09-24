import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import binom, poisson, norm, expon, shapiro, ttest_ind
import statsmodels.api as sm
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def explorar_dados(df):

    print("Informações sobre o DataFrame:")
    print(df.info())
    print("\nEstatísticas descritivas:")
    print(df.describe())

    sns.histplot(df['satisfacao'], kde=True)
    plt.title('Distribuição da Satisfação')
    plt.xlabel('Satisfação')
    plt.ylabel('Frequência')
    plt.show()

    sns.boxplot(x=df['tempo_medio_atendimento'])
    plt.title('Dispersão do Tempo Médio de Atendimento')
    plt.xlabel('Tempo Médio de Atendimento (minutos)')
    plt.show()


def medidas_tendencia(df):

    media_satisfacao = df['satisfacao'].mean()
    mediana_satisfacao = df['satisfacao'].median()
    moda_satisfacao = df['satisfacao'].mode()[0]

    print(f"Média da Satisfação: {media_satisfacao:.2f}")
    print(f"Mediana da Satisfação: {mediana_satisfacao:.2f}")
    print(f"Moda da Satisfação: {moda_satisfacao:.2f}")


def medidas_dispersao(df):

    variancia_satisfacao = df['satisfacao'].var()
    desvio_padrao_satisfacao = df['satisfacao'].std()
    iqr_satisfacao = df['satisfacao'].quantile(0.75) - df['satisfacao'].quantile(0.25)

    print(f"Variância da Satisfação: {variancia_satisfacao:.2f}")
    print(f"Desvio Padrão da Satisfação: {desvio_padrao_satisfacao:.2f}")
    print(f"Intervalo Interquartil da Satisfação: {iqr_satisfacao:.2f}")


def calcular_probabilidades(df):

    prob_resolucao = df['resolucao_primeiro_contato'].mean()
    print(f"Probabilidade de Resolução no Primeiro Contato: {prob_resolucao:.2f}")

    prob_pico = df['horario_pico'].mean()
    print(f"Probabilidade de Atendimento em Horário de Pico: {prob_pico:.2f}")

    prob_satisfacao_alta = (df['satisfacao'] > 4).mean()
    print(f"Probabilidade de Satisfação Alta: {prob_satisfacao_alta:.2f}")

    satisfacao_alta_pico = df[df['horario_pico'] == True]['satisfacao'] > 4
    prob_condicional = satisfacao_alta_pico.mean()
    print(f"Probabilidade de Satisfação Alta dado Atendimento em Horário de Pico: {prob_condicional:.2f}")


def modelar_variaveis_discretas(df):

    n = 100
    p = df['resolucao_primeiro_contato'].mean()
    distrib_binomial = binom(n, p)

    lambda_poisson = df['atendimentos'].mean()
    distrib_poisson = poisson(lambda_poisson)


    x_binom = np.arange(0, n + 1)
    x_poisson = np.arange(0, df['atendimentos'].max() + 1)

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.bar(x_binom, distrib_binomial.pmf(x_binom), color='skyblue')
    plt.title('Distribuição Binomial (n=100, p={:.2f})'.format(p))
    plt.xlabel('Número de Sucessos')
    plt.ylabel('Probabilidade')

    plt.subplot(1, 2, 2)
    plt.bar(x_poisson, distrib_poisson.pmf(x_poisson), color='salmon')
    plt.title('Distribuição de Poisson (λ={:.2f})'.format(lambda_poisson))
    plt.xlabel('Número de Atendimentos')
    plt.ylabel('Probabilidade')

    plt.tight_layout()
    plt.show()


def modelar_variaveis_continuas(df):

    media_tempo = df['tempo_medio_atendimento'].mean()
    std_tempo = df['tempo_medio_atendimento'].std()
    distrib_normal = norm(media_tempo, std_tempo)


    lambda_expon = 1 / df['tempo_medio_atendimento'].mean()
    distrib_expon = expon(scale=1 / lambda_expon)


    x = np.linspace(df['tempo_medio_atendimento'].min(), df['tempo_medio_atendimento'].max(), 100)

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    sns.histplot(df['tempo_medio_atendimento'], bins=20, kde=False, stat='density', color='green', alpha=0.6)
    plt.plot(x, distrib_normal.pdf(x), 'r-', label='Normal')
    plt.title('Distribuição Normal do Tempo Médio de Atendimento')
    plt.xlabel('Tempo Médio de Atendimento (minutos)')
    plt.ylabel('Densidade')
    plt.legend()

    plt.subplot(1, 2, 2)
    sns.histplot(df['tempo_medio_atendimento'], bins=20, kde=False, stat='density', color='purple', alpha=0.6)
    plt.plot(x, distrib_expon.pdf(x), 'b-', label='Exponencial')
    plt.title('Distribuição Exponencial do Tempo Médio de Atendimento')
    plt.xlabel('Tempo Médio de Atendimento (minutos)')
    plt.ylabel('Densidade')
    plt.legend()

    plt.tight_layout()
    plt.show()


    stat, p = shapiro(df['tempo_medio_atendimento'])
    print('Shapiro-Wilk Test: stat=%.3f, p=%.3f' % (stat, p))
    if p > 0.05:
        print('A distribuição parece ser normal.')
    else:
        print('A distribuição não é normal.')


def testes_de_hipotese(df):

    satisfacao_pico = df[df['horario_pico'] == True]['satisfacao']
    satisfacao_nao_pico = df[df['horario_pico'] == False]['satisfacao']


    stat, p = ttest_ind(satisfacao_pico, satisfacao_nao_pico, equal_var=False)
    print('Teste t: stat=%.3f, p=%.3f' % (stat, p))
    if p < 0.05:
        print('Há diferença significativa na satisfação entre horário de pico e não pico.')
    else:
        print('Não há diferença significativa na satisfação entre horário de pico e não pico.')


    from statsmodels.stats.weightstats import DescrStatsW
    dsw = DescrStatsW(df['satisfacao'])
    conf_int = dsw.tconfint_mean()
    print(f'Intervalo de Confiança de 95% para a média da satisfação: {conf_int}')


def regressao_linear(df):
    try:
        Y = df['Pontuacao']

        X = df[['satisfacao', 'resolucao_primeiro_contato', 'atendimentos', 'horario_pico']].copy()

        X['horario_pico'] = pd.to_numeric(X['horario_pico'], errors='coerce').fillna(0)

        X['horario_pico'] = X['horario_pico'].astype(int)

        X = sm.add_constant(X)

        modelo = sm.OLS(Y, X).fit()

        print(modelo.summary())

        previsoes = modelo.predict(X)
        df['Previsao_Pontuacao'] = previsoes

        plt.figure(figsize=(6, 6))
        plt.scatter(df['Pontuacao'], df['Previsao_Pontuacao'], color='blue')
        plt.xlabel('Pontuação Real')
        plt.ylabel('Pontuação Prevista')
        plt.title('Pontuação Real vs Prevista')
        plt.plot([Y.min(), Y.max()], [Y.min(), Y.max()], 'r--')
        plt.show()

    except Exception as e:
        print(f"Ocorreu um erro durante a regressão linear: {e}")