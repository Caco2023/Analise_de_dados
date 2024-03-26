# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 10:53:40 2024

@author: Rafael
"""



import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns
import datetime as dt


"Carregando o dataframe"

DATA = pd.read_csv("dados/dataset.csv")
print("Inicio do data set.")
print(DATA.head())


"Fazendo a Análise Exploratoria"

"COLUNAS"
print("\nColunas do dataset")
print(DATA.columns)

"Tipos de dados de cada coluna"
print("\nTipos de dados de cada coluna")
print(DATA.dtypes)

"Resumo estatístico da coluna com valor de vendas"
print("\nResumo estatístico da coluna com valor de vendas")
print(DATA["Valor_Venda"].describe())

"Verificando se ha registros duplicados"
print("\nVerificando se ha registros duplicados")
print(DATA[DATA.duplicated()])

"Verificando se tem células com valores ausentes"
print("\nVerificando se tem células com valores ausentes")
print(DATA.isnull().sum())


"PERGUNTA DE NEGÓCIO 01: Qual Cidade com Maior Valor de Venda de Produtos da Categoria 'Office Supplies'?"
print("\nPERGUNTA DE NEGÓCIO 01: Qual Cidade com Maior Valor de Venda de Produtos da Categoria 'Office Supplies'?")
PN_01 = DATA[DATA["Categoria"] == "Office Supplies"]
PN_01_TOTAL = PN_01.groupby("Cidade")["Valor_Venda"].sum()
PN_01_FINAL = PN_01_TOTAL.sort_values(ascending = False)
PN_01_MAX = PN_01_TOTAL.idxmax()
print(PN_01_FINAL)
print("A Cidade com Maior Valor de Venda de Produtos da Categoria 'Office Supplies' é: " + PN_01_MAX)


"Pergunta de Negócio 2: Qual o Total de Vendas Por Data do Pedido?"
print("\nPergunta de Negócio 2:Qual o Total de Vendas Por Data do Pedido?")
PN_02 = DATA.groupby("Data_Pedido")["Valor_Venda"].sum()
plt.figure(figsize = (20,6))
PN_02.plot(x = "Data_Pedido", y = "Valor_Venda", color = "red")
plt.title("Gráfico de venda por período")
plt.show()
print(PN_02)


"Pergunta de Negócio 3: Qual o Total de Vendas por Estado?"
print("\nPergunta de Negócio 3: Qual o Total de Vendas por Estado?")
PN_03 = DATA.groupby("Estado")["Valor_Venda"].sum()
plt.figure(figsize = (20, 6))
PN_03.plot(kind = "bar", x = "Estado", y = "Valor_Venda")
plt.title("Gráfico de vendas por estado")
plt.show()
print(PN_03)


"Pergunta de Negócio 4: Quais São as 10 Cidades com Maior Total de Vendas?"
print("\nPergunta de Negócio 4: Quais São as 10 Cidades com Maior Total de Vendas?")
PN_04 = DATA.groupby("Cidade")["Valor_Venda"].sum()
PN_04_ORDENADO = PN_04.sort_values(ascending = False)
PN_04_FINAL = PN_04_ORDENADO.head(10)
print(PN_04_FINAL)
plt.figure(figsize = (20,6))
PN_04_FINAL.plot(kind = "bar", x = "Cidade", y = "Valor_Venda")
plt.title("Gráfico das 10 cidades com maior total de vendas")
plt.show()


"Pergunta de Negócio 5: Qual Segmento Teve o Maior Total de Vendas?"
print("\nPergunta de Negócio 5: Qual Segmento Teve o Maior Total de Vendas?")
PN_05 = DATA.groupby("Segmento")["Valor_Venda"].sum().reset_index().sort_values(by = "Valor_Venda", ascending = False)

"Transformando para valores absolutos"
def autopct_format(values): 
    def my_format(pct): 
        total = sum(values) 
        val = int(round(pct * total / 100.0))
        return ' $ {v:d}'.format(v = val)
    return my_format

"Gráfico"
plt.figure(figsize = (16,6))
plt.pie(PN_05["Valor_Venda"], labels = PN_05["Segmento"], autopct = autopct_format(PN_05["Valor_Venda"]), startangle=90)
center_cicle = plt.Circle((0,0), 0.82, fc = "white")
fig = plt.gcf()
fig.gca().add_artist(center_cicle)
plt.annotate(text = "Total de vendas: " + "$" + str(int(sum(DATA["Valor_Venda"]))), xy = (-0.25,0))
plt.title("Gráfico de vendas por segmento")
plt.show()
print(PN_05)


"Pergunta de Negócio 6: Qual o Total de Vendas Por Segmento e Por Ano?"
print("\nQual o Total de Vendas Por Segmento e Por Ano?")
"Convertendo os valores Data_Pedido para um formato adequado"
DATA["Data_Pedido"] = pd.to_datetime(DATA["Data_Pedido"], dayfirst=True)
DATA["Ano"] = DATA["Data_Pedido"].dt.year
PN_06 = DATA.groupby(["Ano", "Segmento"])["Valor_Venda"].sum()
print(PN_06)


"Pergunta de Negócio 7: Os gestores da empresa estão considerando conceder diferentes faixas de descontos e gostariam de fazer uma simulação com base na regra abaixo: Se o Valor_Venda for maior que 1000 recebe 15% de desconto. Se o Valor_Venda for menor que 1000 recebe 10% de desconto. Quantas Vendas Receberiam 15% de Desconto?"
DATA["Desconto"] = np.where(DATA["Valor_Venda"]>1000, 0.15, 0.10)
print("")
print(DATA["Desconto"].value_counts())
print("\nA quantidade de vendas com 15% de desconto foi: 457") 


"Pergunta de Negócio 8: Considere Que a Empresa Decida Conceder o Desconto de 15% do Item Anterior. Qual Seria a Média do Valor de Venda Antes e Depois do Desconto?"
print("\nConsidere Que a Empresa Decida Conceder o Desconto de 15% do Item Anterior. Qual Seria a Média do Valor de Venda Antes e Depois do Desconto?")
"Média do valor de vendas antes de dar o desconto"
PN_08_SEM_DESCONTO = DATA["Valor_Venda"].mean()
print("A média de valores de venda antes do desconto é: " + str(PN_08_SEM_DESCONTO))
"Média de vendas com desconto de 15%"
DATA["VENDAS_COM_DESCONTO"] = DATA["Valor_Venda"] - DATA["Valor_Venda"] * DATA["Desconto"]
PN_08_COM_DESCONTO = np.where(DATA["Desconto"]==0.1, DATA["Valor_Venda"], DATA["VENDAS_COM_DESCONTO"]).mean()
print("A média das vendas com desconto planejado de 15% é: " + str(PN_08_COM_DESCONTO)) 


"Pergunta de Negócio 9: Qual o Média de Vendas Por Segmento, Por Ano e Por Mês?¶"
print("\nQual é a média de vendas por segmento, por ano e por mes?")
DATA["Mes"] = DATA["Data_Pedido"].dt.month 
PN_09 = DATA.groupby(["Ano", "Mes", "Segmento"])["Valor_Venda"].agg([np.mean])
print(PN_09)
"Gráfico"
ano = PN_09.index.get_level_values(0)
mes = PN_09.index.get_level_values(1)
segmento = PN_09.index.get_level_values(2)

plt.figure(figsize = (12,6))

fig1 = sns.relplot(kind = 'line',
                   data = PN_09,
                   y = 'mean', 
                   x = mes,
                   hue = segmento, 
                   col = ano,
                   col_wrap = 4)
sns.set()

                                                                         


