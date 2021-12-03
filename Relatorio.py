import fpdf
from fpdf import FPDF
import time
import matplotlib.pyplot as plt
import dataframe_image as dfi
import pandas as pd
import numpy as np

df = pd.read_csv("arquivocsv.csv", encoding = "ISO-8859-1",sep=';')

df.head()
print(df.head(20))

#DADOS DE ENTRADA
empresa = "BRUMATTI MOBILI LTDA"
endereco = "RUA ALFREDO CHAVES 757, 29148-030 VILA CAPIXABA / CARIACICA - ES"
concessionaria = "EDP ESCELSA"

########### DEMANDA REGISTRADA #############
demandacontratada = 115
a1 = demandacontratada
############### PREÇO ATUAL ################
pcp = round(1.68883129, 2)
pcfp = round(0.34724388, 2)
pdemanda = round(32.20806452, 2)
pmulta = round(0, 2)
pdemandar = round(0, 2)
eexcedente = round(0.27609742, 2)
################ TRIBUTOS ##################
pis = 0.0111
cofins = 0.0511
icms = 0.25
tributos = 1 / (1-(pis+cofins+icms))
print(tributos)
# Apply styling to dataframe
styled_df = df.style.format({
                      'EA ponta': "{:.2f}",
                      'EA Fponta': "{:.2f}",'Demanda ponta': "{:.2f}",
                      'Demanda Fponta': "{:.2f}",'Ultrapassagem ponta': "{:.2f}",
                      'Ultrapassagem Fponta': "{:.2f}",'Demanda Reat exc Ponta': "{:.2f}",
                      'Demanda Reat exc Fponta': "{:.2f}",'Energia Reat Excedente': "{:.2f}",
                      'Fatura': "{:.2f}",
                     })

dfi.export(styled_df, 'Resumo historico.png')

listames = []
listasoma = []
listasoma1 =[]
listasoma2 = []
listasoma3 = []
listasoma4 = []
listasoma5 = []
listasoma6 = []
listasoma7 = []
listasoma8 = []
listasoma9 = []

def geragrafico(filename):
    plt.figure(figsize=(16, 4))
    # Quantidade de vendas para o Produto A
    valores_produto_A = df['EA ponta'].values

    # Quantidade de vendas para o Produto B
    valores_produto_B = df['EA Fponta'].values

    # Cria eixo x para produto A e produto B com uma separação de 0.25 entre as barras
    x1 =  np.arange(len(valores_produto_A))
    x2 = [x + 0.25 for x in x1]

    # Plota as barras
    plt.bar(x1, valores_produto_A, width=0.25, label = 'Consumo Energia horário PONTA (KWH)', color = 'b')
    plt.bar(x2, valores_produto_B, width=0.25, label = 'Consumo Energia horário FORA DE PONTA (KWH)', color = 'y')

    # coloca o nome dos meses como label do eixo x
    meses = df['Mês'].values
    plt.xticks([x + 0.25 for x in range(len(valores_produto_A))], meses)

    # inseri uma legenda no gráfico
    plt.legend()

    plt.title("RELAÇÃO DO CONSUMO DE ENERGIA EM HORÁRIO DE PONTA E FORA DE PONTA")

    plt.savefig(filename, dpi=300, pad_inches=0)
    plt.show()

geragrafico('barrasconsumo.png')

###################################################ULTRAPASSAGEM ##############

def geragrafico2(filename):
    plt.figure(figsize=(16, 4))
    # Quantidade de vendas para o Produto A
    valores_produto_A = df['Ultrapassagem ponta'].values

    # Quantidade de vendas para o Produto B
    valores_produto_B = df['Ultrapassagem Fponta'].values

    # Cria eixo x para produto A e produto B com uma separação de 0.25 entre as barras
    x1 =  np.arange(len(valores_produto_A))
    x2 = [x + 0.25 for x in x1]

    # Plota as barras
    plt.bar(x1, valores_produto_A, width=0.25, label = 'Ultrapassagem em horário de PONTA (KW)', color = 'b')
    plt.bar(x2, valores_produto_B, width=0.25, label = 'Ultrapassagem em horário FORA DE PONTA (KW)', color = 'y')

    # coloca o nome dos meses como label do eixo x
    meses = df['Mês'].values
    plt.xticks([x + 0.25 for x in range(len(valores_produto_A))], meses)

    # inseri uma legenda no gráfico
    plt.legend()

    plt.title("MULTAS POR ULTRAPASSSAGEM DE DEMANDA")

    plt.savefig(filename, dpi=300, pad_inches=0)
    plt.show()

geragrafico2('barrasultrapassagem.png')


def geragrafico3(filename):
    plt.figure(figsize=(16, 4))
    # Quantidade de vendas para o Produto A
    valores_produto_A = df['Energia Reat Excedente'].values

    # Cria eixo x para produto A e produto B com uma separação de 0.25 entre as barras
    x1 = np.arange(len(valores_produto_A))

    # Plota as barras
    plt.bar(x1, valores_produto_A, width=0.5, label='Energia Reat Excedente (KWH)', color='b')

    # coloca o nome dos meses como label do eixo x
    meses = df['Mês'].values
    plt.xticks([x + 0 for x in range(len(valores_produto_A))], meses)

    # inseri uma legenda no gráfico
    plt.legend()

    plt.title("ENERGIA REATIVA EXCEDENTE")

    plt.savefig(filename, dpi=300, pad_inches=0)
    plt.show()

geragrafico3('barrareativo.png')

#####################################################

for x in df['Mês'].values:
    total1 = listames.append(x)

print(df['Mês'].values)


for x in df['EA ponta']:
    total = listasoma.append(x)
    somaconsumop = float(sum(listasoma))
    somaconsumop1 = somaconsumop
    somaconsumop = somaconsumop * pcp * tributos
    somaconsumop = round(somaconsumop, 1)


print(somaconsumop)

for x in df['EA Fponta']:
    total = listasoma1.append(x)
    somaconsumofp = float(sum(listasoma1))
    somaconsumofp1 = somaconsumofp
    somaconsumofp = somaconsumofp * pcfp * tributos
    somaconsumofp = round(somaconsumofp, 1)


print(somaconsumofp)

somaconsumo1 = somaconsumop1 + somaconsumofp1
somaconsumo = str(somaconsumo1)

for x in df['Demanda ponta']:
    total = listasoma2.append(x)
    somademandap = float(sum(listasoma2))
    somademandap = somademandap * pdemanda * tributos
    somademandap = round(somademandap, 1)

print(somademandap)

for x in df['Demanda Fponta']:
    total = listasoma3.append(x)
    somademandafp = float(sum(listasoma3))
    somademandafp = somademandafp * pdemanda * tributos
    somademandafp = round(somademandafp, 1)

print(somademandafp)

for x in df['Ultrapassagem ponta']:
    total = listasoma4.append(x)
    somaultrapassagemp = float(sum(listasoma4))
    somaultrapassagemp1 = somaultrapassagemp
    somaultrapassagemp = somaultrapassagemp * pmulta * tributos
    somaultrapassagemp = round(somaultrapassagemp, 1)


print(somaultrapassagemp)

for x in df['Ultrapassagem Fponta']:
    total = listasoma5.append(x)
    somaultrapassagemfp = float(sum(listasoma5))
    somaultrapassagemfp1 = somaultrapassagemfp
    somaultrapassagemfp = somaultrapassagemfp * pmulta * tributos
    somaultrapassagemfp = round(somaultrapassagemfp, 1)


somaultrapassagemtotalkm = (somaultrapassagemp + somaultrapassagemfp)
somaultrapassagemtotalkm = str(somaultrapassagemtotalkm)
print(somaultrapassagemfp)
print(somaultrapassagemtotalkm)

for x in df['Demanda Reat exc Ponta']:
    total = listasoma6.append(x)
    somademandareatp = float(sum(listasoma6))
    somademandareatp = somademandareatp * pdemandar * tributos

print(somademandareatp)


for x in df['Demanda Reat exc Fponta']:
    total = listasoma7.append(x)
    somademandareatfp = sum(listasoma7)
    somademandareatfp = somademandareatfp * pdemandar * tributos

print(somademandareatfp)


for x in df['Energia Reat Excedente']:
    total = listasoma8.append(x)
    somaenergiareatfp = float(sum(listasoma8))
    somaenergiareatfp1 = (somaenergiareatfp)
    somaenergiareatfp1 = round(somaenergiareatfp1, 1)
    somaenergiareatfp = (somaenergiareatfp * eexcedente * tributos)
    somaenergiareatfp = round(somaenergiareatfp, 1)


print(somaenergiareatfp)
print(somaenergiareatfp1)


for x in df['Fatura']:
    total = listasoma9.append(x)
    fatura = sum(listasoma9)
    fatura = round(fatura, 1)
    fatura = str(fatura)

print(fatura)

def geragrafico1(filename):


    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'CONSUMO PONTA', 'CONSUMO FORA PONTA', 'DEMANDA PONTA', 'DEMANDA FORA PONTA', 'ULTRAPASSAGEM PONTA', 'ULTRAPASSAGEM FORAPONTA', 'DEMANDA REATIVA EXCEDENTE PONTA', 'DEMANDA REATIVA EXCEDENTE FORA PONTA', 'ENERGIA REATIVA EXCEDENTE'
    sizes = [somaconsumop, somaconsumofp, somademandap, somademandafp, somaultrapassagemp, somaultrapassagemfp, somademandareatp, somademandareatfp,somaenergiareatfp ]
    explode = (0, 0, 0, 0, 0, 0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots(figsize=(8, 8))

    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=30)

    ax1.set_title('COMPOSIÇÃO DE CUSTO ANUAL')

    # Save the plot as a PNG
    plt.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.show()

geragrafico1('pizzacustoanual1.png')

#########################TEST
fig, ax = plt.subplots(figsize=(12, 6), subplot_kw=dict(aspect="equal"))

data = [somaconsumop, somaconsumofp, somademandap, somademandafp, somaultrapassagemp, somaultrapassagemfp, somademandareatp, somademandareatfp,somaenergiareatfp]
ingredients = ['CONSUMO PONTA', 'CONSUMO FORA PONTA', 'DEMANDA PONTA', 'DEMANDA FORA PONTA', 'ULTRAPASSAGEM PONTA', 'ULTRAPASSAGEM FORAPONTA', 'DEMANDA REATIVA EXCEDENTE PONTA', 'DEMANDA REATIVA EXCEDENTE FORA PONTA', 'ENERGIA REATIVA EXCEDENTE']


def func(pct, allvals):
    absolute = int(round(pct/100.*np.sum(allvals)))
    return "{:.1f}%".format(pct, absolute)


wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                  textprops=dict(color="w"))

ax.legend(wedges, ingredients,
          title="Ingredients",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=10, weight="bold")

ax.set_title("COMPOSIÇÃO DE CUSTO ANUAL")
plt.savefig('pizzacustoanual.png', dpi=300, bbox_inches='tight', pad_inches=0)

plt.show()
################FIM TEST
# Data
plt.figure(figsize=(16, 4))
df = pd.DataFrame(
    {'x_values': df['Mês'].values, 'DEMANDA CONTRATADA': [a1,a1,a1,a1,a1,a1,a1,a1,a1,a1,a1,a1,a1], 'DEMANDA REGISTRADA': df['Demanda Fponta'].values})

# multiple line plots
plt.plot('x_values', 'DEMANDA CONTRATADA', data=df, marker='o', markerfacecolor='blue', markersize=12, color='skyblue',
         linewidth=4)
plt.plot('x_values', 'DEMANDA REGISTRADA', data=df, marker='', color='olive', linewidth=2)

# show legend
plt.legend()
plt.savefig('demandahist.png', dpi=300, pad_inches=0)
# show graph
plt.show()

#########################PDF

def create_letterhead(pdf, WIDTH):
    pdf.image("logoist.png", 0, 0, WIDTH)


def create_title(title, pdf):
    # Add main title
    pdf.set_font('Helvetica', 'b', 30)
    pdf.ln(40)
    pdf.write(10, title)
    pdf.ln(10)

    # Add date of report
    pdf.set_font('Helvetica', '', 6)
    pdf.set_text_color(r=128, g=128, b=128)
    today = time.strftime("%d/%m/%Y")
    pdf.write(4, f'{today}')

    # Add line break
    pdf.ln(2)

def create_subtitle(subtitle, pdf):
    # Add main title
    pdf.set_font('Helvetica', 'b', 14)
    pdf.ln(0)
    pdf.write(10, subtitle)
    pdf.ln(15)

def create_subtitle1(pdf, subtitle):
    # Add main title
    pdf.set_font('Helvetica', 'b', 10)
    pdf.set_text_color(r=0, g=0, b=0)
    pdf.write(10, subtitle)


def write_to_pdf(pdf, words):
    # Set text colour, font size, and font type
    pdf.set_text_color(r=0, g=0, b=0)
    pdf.set_font('Helvetica', '', 12)

    pdf.write(5, words)

def write_to_pdf1(pdf, words):
    # Set text colour, font size, and font type
    pdf.set_text_color(r=0, g=0, b=0)
    pdf.set_font('Helvetica', '', 10)

    pdf.write(5, words)

class PDF(FPDF):

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

# Global Variables
TITLE = "EFICIÊNCIA ENERGÉTICA"
SUBTITLE = "Análise Tarifária"
WIDTH = 210
HEIGHT = 297

# Create PDF
pdf = PDF() # A4 (210 by 297 mm)


'''
First Page of PDF
'''
# Add Page
pdf.add_page()

# Add lettterhead and title
create_letterhead(pdf, WIDTH)
create_title(TITLE, pdf)
create_subtitle(SUBTITLE, pdf)

# Add some words to PDF
create_subtitle1(pdf, "1 - DIAGNÓSTICO ENERGÉTICO PRELIMINAR")
pdf.ln(10)

# Add some words to PDF
write_to_pdf1(pdf, "O presente diagnóstico tem como objetivo avaliar potenciais oportunidades de redução do custo energético na conta de energia.")
pdf.ln(8)

# Add some words to PDF
create_subtitle1(pdf, "2 - IDENTIFICAÇÃO DA EMPRESA")
pdf.ln(10)

# Add some words to PDF
write_to_pdf1(pdf, "O fornecimento de energia elétrica da empresa ")
write_to_pdf1(pdf, empresa)
write_to_pdf1(pdf, " , localizada em, ")
write_to_pdf1(pdf, endereco)
write_to_pdf1(pdf, " , é realizado pela concessionária  ")
write_to_pdf1(pdf, concessionaria)
pdf.ln(8)

# Add some words to PDF
create_subtitle1(pdf, "3 - HISTÓRICO DE USO")
pdf.ln(10)
# Add some words to PDF
write_to_pdf1(pdf, "O histórico de uso refere-se as informações de consumo dos últimos 12 meses da conta de  energia.")
pdf.ln(10)
# Add table
pdf.image("Resumo historico.png", w=180)
pdf.ln(3)

# Add some words to PDF
create_subtitle1(pdf, "4 - CONCEITOS")
pdf.ln(10)
# Add some words to PDF
write_to_pdf1(pdf, "· Consumo de energia ou energia ativa: Quantidade de potência elétrica ativa consumida em um intervalo de tempo, expresso em quilowatt-hora (kWh).")
pdf.ln(8)
write_to_pdf1(pdf, "· Demanda Contratada: Potência elétrica ativa a ser obrigatoriamente e continuamente disponibilizada pela concessionária, no ponto de entrega.")
pdf.ln(8)
write_to_pdf1(pdf, "· Demanda aferida: Maior demanda de potência ativa, verificada por medição, integralizada no intervalo de 15 minutos durante o período de faturamento.")
pdf.ln(8)
write_to_pdf1(pdf, "· Energia Reativa: Energia necessária para magnetizar motores e geradores e carregar campos elétricos e magnéticos. ")
pdf.ln(8)
write_to_pdf1(pdf, ". Ultrapassagem:  Estouro de demanda ou multa de demanda, momento em  que a demanda contratada é inferior a aferida.  ")
pdf.ln(8)
pdf.add_page()

# Add some words to PDF
create_subtitle1(pdf, "5 - RELAÇÃO DE CUSTO ANUAL")
pdf.ln(10)
# Add some words to PDF
write_to_pdf1(pdf, " A relação de custo anual refere-se a proporção gasta pela empresa entre os custos de consumo em horário de ponta, fora de ponta, reativos, multas e demanda.")
# Add table
pdf.ln(10)
pdf.image("pizzacustoanual.png", w=110)

# Add some words to PDF
create_subtitle1(pdf, "6 - HISTÓRICO DE CONSUMO")
pdf.ln(10)
# Add some words to PDF
write_to_pdf1(pdf, " O histórico de consumo representa o uso mês a mês da energia em horário ponta e fora de ponta.")
# Add table
pdf.ln(10)
# Add table
pdf.image("barrasconsumo.png", w=200)
pdf.ln(12)


# Add some words to PDF
create_subtitle1(pdf, "7 - ENERGIA REATIVA EXCEDENTE")
pdf.ln(10)
# Add some words to PDF
write_to_pdf1(pdf, " Este item refere-se ao histórico de consumo da energia reativa excedente.")
# Add table
pdf.ln(10)
# Add table
pdf.image("barrareativo.png", w=200)
pdf.ln(8)


pdf.add_page()
# Add some words to PDF
create_subtitle1(pdf, "8 - MULTA POR ULTRAPASSAGEM")
pdf.ln(10)
# Add some words to PDF
write_to_pdf1(pdf, " Este item refere-se ao histórico de multas e ultrapassagens de demanda.")
# Add table
pdf.ln(10)
# Add table
pdf.image("barrasultrapassagem.png", w=200)
pdf.ln(8)

# Add some words to PDF
create_subtitle1(pdf, "9 - DEMANDA")
pdf.ln(10)
# Add some words to PDF
write_to_pdf1(pdf, " Este item refere-se a relação entre a demanda contratada e registrada pela unidade consumidora.")
# Add table
pdf.ln(10)
# Add table
pdf.image("demandahist.png", w=200)
pdf.ln(8)

# Add some words to PDF
create_subtitle1(pdf, "10 - MODALIDADE TARIFÁRIA")
pdf.ln(10)


# Add some words to PDF
create_subtitle1(pdf, "11 - CONCLUSÃO")
pdf.ln(10)

# Add some words to PDF
write_to_pdf1(pdf, "             O Histórico de uso da energia da empresa ")
write_to_pdf1(pdf, empresa)
write_to_pdf1(pdf, " permitiu levantarmos durante os 12 últimos meses um custo de R$ ")
write_to_pdf1(pdf, fatura)
write_to_pdf1(pdf, " com consumo total de ")
write_to_pdf1(pdf, somaconsumo)
write_to_pdf1(pdf, " KWH , multas por utrapassagem de ")
write_to_pdf1(pdf, somaultrapassagemtotalkm)
write_to_pdf1(pdf, " KW, e uso de energia excedente de ")
write_to_pdf1(pdf, str(somaenergiareatfp1))
write_to_pdf1(pdf, " KWH. Com relação ao uso energético, pontuamos sempre o dever quanto ao uso consciente e as avaliações em máquinas e equipamentos na busca por melhor eficiência e possíveis desperdícios")
write_to_pdf1(pdf, ". O consumo energético é medido e caracterizado pelo perfil de consumo de cada empresa. Sendo assim indicamos utilizar corretamente os ativos, prever o uso apenas quando necessário e orientar seus colaboradores quanto ao uso correto. ")
pdf.ln(3)
write_to_pdf1(pdf, "'\n          Multas por ultrapassagens , não há. No caso a demanda registrada contínue a baixar com o passar dos meses, indico a reavaliação do valor de demanda contratada. Com relação ao uso de energia reativa excedente, é notável o aumento crescente de seu uso nos ultimos 10 meses e aconselhamos a verificação deste item que não deveria existir.")
pdf.ln(3)
write_to_pdf1(pdf, "'\n          Considerando o histórico de uso dos últimos 12 meses, considero que poderiamos ter evitado um custo de R$ ")
write_to_pdf1(pdf, str(somaconsumop))
write_to_pdf1(pdf, " da utilização em horários de ponta, R$ ")
write_to_pdf1(pdf, str(somaenergiareatfp))
write_to_pdf1(pdf, " com o excesso do uso de energia reativa. Em caso de dúvidas e/ou suporte, entre em contato conosco.")

pdf.ln(30)

write_to_pdf1(pdf, "                               RESPONSÁVEL: Felipe Segundo Marçal - CONSULTOR")
pdf.ln(6)
write_to_pdf1(pdf, "                               Contato: 27 999290521 - EMAIL: fmarcal@findes.org.br")



# Generate the PDF
pdf.output("Análise tarifaria.pdf", 'F')