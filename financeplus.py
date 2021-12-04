import streamlit as st
import pandas as pd
pd.set_option('display.float_format', lambda x: '%.2f' % x)
import numpy as np
import datetime
import time
import pandas_datareader.data as web
import yfinance as yf
yf.pdr_override()
import matplotlib.pyplot as plt
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))
import telegram
from binance.client import Client
import json



api_key = 'VMcjzDusoLH0C3e3rqPqyQyyOlUGk7IxJR0Ncy3ysh00hNzBtCZSz3KcFYxcIH2M'
api_secret = 'Qsy4QGQhS5JyXy5yF9y2bZKuNhrQIiXdRleMuSVBamXl8VbEmm8QJAjV3Wju9oLN'

client = Client(api_key=api_key, api_secret=api_secret)
precos = client.get_all_tickers()

#TELEGRAM
my_token = '1983878362:AAF_rCuuehuKeIb9g2aK_-lFlwQ4oogWg1g'
chat_id = '1081112075'

#DATAFRAME ACOES
prices = pd.DataFrame()
a=pd.DataFrame()

start = datetime.datetime(2021, 4, 1)
end = datetime.datetime(2022, 1, 30)

##### INSERINDO BARRA ####
st.sidebar.title("OPERAÇÕES: DIA")

col = st.sidebar.selectbox("SELECIONE UMA OPÇÃO:", ["","CARTEIRA - INDICADORES: NÍVEL I","CARTEIRA - INDICADORES: NÍVEL II", "ANÁLISE TÉCNICA" , "INDICADORES NÍVEL I", "INDICADORES: NÍVEL II"])

##### INSERINDO BARRA 2 ####
st.sidebar.title("OPERAÇÕES: HORA")

col2 = st.sidebar.selectbox("SELECIONE UMA OPÇÃO:", ["","CARTEIRA - INDICADORES: NÍVEL I","CARTEIRA - INDICADORES: NÍVEL II", "ANÁLISE TÉCNICA" , "INDICADORES NÍVEL I", "INDICADORES NÍVEL II "])


##### INSERINDO BARRA 3 CRIPTOMOEDAS ####
st.sidebar.title("CRIPTO-OPERAÇÕES: DIA")

col3 = st.sidebar.selectbox("SELECIONE UMA OPÇÃO:", ["","INDICADORES NÍVEL I", "INDICADORES NÍVEL II"])

##### INSERINDO BARRA 4 CRIPTOMOEDAS ####
st.sidebar.title("CRIPTO-OPERAÇÕES: SEMANA")

col4 = st.sidebar.selectbox("SELECIONE UMA OPÇÃO:", ["","INDICADORES NÍVEL I ", "INDICADORES NÍVEL II "])

###########
def envia_mensagem(msg, chat_id, token = my_token):
  bot = telegram.Bot(token = token)
  bot.sendMessage(chat_id = chat_id, text = msg)
##########ABAS#############


if col == "CARTEIRA - INDICADORES: NÍVEL I":
    st.write(
        """
            "CARTEIRA - INDICADORES: NÍVEL I"
        """
    )
    acoes = ['BEEF3.SA', 'ETER3.SA', 'GGBR4.SA', 'NGRD3.SA', 'SAPR11.SA', 'VIIA3.SA', 'SUZB3.SA', 'CIEL3.SA',
             'KLBN11.SA', 'MNPR3.SA', 'OIBR3.SA']

    listasigla = []
    listaindicador = []

    for acao in acoes:

        listasigla.append(acao)
        acao = web.get_data_yahoo(acao, start, end)
        sinal_preco = acao['Adj Close'].iloc[-1]


        def computeRSI(data, time_window):
            diff = data.diff(1).dropna()  # diff in one field(one day)

            # this preservers dimensions off diff values
            up_chg = 0 * diff
            down_chg = 0 * diff

            # up change is equal to the positive difference, otherwise equal to zero
            up_chg[diff > 0] = diff[diff > 0]

            # down change is equal to negative deifference, otherwise equal to zero
            down_chg[diff < 0] = diff[diff < 0]

            # check pandas documentation for ewm
            # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
            # values are related to exponential decay
            # we set com=time_window-1 so we get decay alpha=1/time_window
            up_chg_avg = up_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
            down_chg_avg = down_chg.ewm(com=time_window - 1, min_periods=time_window).mean()

            rs = abs(up_chg_avg / down_chg_avg)
            rsi = 100 - 100 / (1 + rs)
            return rsi


        acao['RSI'] = computeRSI(acao['Adj Close'], 14)


        def stochastic(data, k_window, d_window, window):

            # input to function is one column from df
            # containing closing price or whatever value we want to extract K and D from

            min_val = data.rolling(window=window, center=False).min()
            max_val = data.rolling(window=window, center=False).max()

            stoch = ((data - min_val) / (max_val - min_val)) * 100

            K = stoch.rolling(window=k_window, center=False).mean()
            # K = stoch

            D = K.rolling(window=d_window, center=False).mean()
            return K, D


        acao['K'], acao['D'] = stochastic(acao['RSI'], 3, 3, 14)

        if acao['RSI'].iloc[-1] > 65 and acao['K'].iloc[-1] > 85:
            if acao['K'].iloc[-1] < acao['D'].iloc[-1]:
                indicador = 10
                msg = f'{listasigla[-1]} VENDA/D-N1 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        elif acao['RSI'].iloc[-1] < 35 and acao['K'].iloc[-1] < 25:
            if acao['K'].iloc[-1] > acao['D'].iloc[-1]:
                indicador = 4
                msg = f'{listasigla[-1]} COMPRA/D-N1 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        else:
            indicador = 0

        print(indicador)
        listaindicador.append(indicador)

    st.markdown("INDICATORS")

    # Figuras

    fig1, fig2 = st.columns(2)

    with fig1:
        st.markdown("Ações Bloco 1")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[0:5], listaindicador[0:5])
        st.pyplot(plt)

    with fig2:
        st.markdown("Ações Bloco 2")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[5:11], listaindicador[5:11])
        st.pyplot(plt)

    st.markdown("<hr/>", unsafe_allow_html=True)

if col == "CARTEIRA - INDICADORES: NÍVEL II":
    st.write(
        """
            "CARTEIRA - INDICADORES: NÍVEL II"
        """
    )
    acoes = ['BEEF3.SA', 'ETER3.SA', 'GGBR4.SA', 'NGRD3.SA', 'SAPR11.SA', 'VIIA3.SA', 'SUZB3.SA', 'CIEL3.SA',
             'KLBN11.SA', 'MNPR3.SA', 'OIBR3.SA']

    listasigla = []
    listaindicador = []

    for acao in acoes:

        listasigla.append(acao)
        acao = web.get_data_yahoo(acao, start, end)  # Ambev
        sinal_preco = acao['Adj Close'].iloc[-1]


        def computeRSI(data, time_window):
            diff = data.diff(1).dropna()  # diff in one field(one day)

            # this preservers dimensions off diff values
            up_chg = 0 * diff
            down_chg = 0 * diff

            # up change is equal to the positive difference, otherwise equal to zero
            up_chg[diff > 0] = diff[diff > 0]

            # down change is equal to negative deifference, otherwise equal to zero
            down_chg[diff < 0] = diff[diff < 0]

            # check pandas documentation for ewm
            # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
            # values are related to exponential decay
            # we set com=time_window-1 so we get decay alpha=1/time_window
            up_chg_avg = up_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
            down_chg_avg = down_chg.ewm(com=time_window - 1, min_periods=time_window).mean()

            rs = abs(up_chg_avg / down_chg_avg)
            rsi = 100 - 100 / (1 + rs)
            return rsi


        acao['RSI'] = computeRSI(acao['Adj Close'], 14)


        def stochastic(data, k_window, d_window, window):

            # input to function is one column from df
            # containing closing price or whatever value we want to extract K and D from

            min_val = data.rolling(window=window, center=False).min()
            max_val = data.rolling(window=window, center=False).max()

            stoch = ((data - min_val) / (max_val - min_val)) * 100

            K = stoch.rolling(window=k_window, center=False).mean()
            # K = stoch

            D = K.rolling(window=d_window, center=False).mean()
            return K, D


        acao['K'], acao['D'] = stochastic(acao['RSI'], 3, 3, 14)

        if acao['RSI'].iloc[-1] > 70 and acao['K'].iloc[-1] > 90:
            if acao['K'].iloc[-1] < acao['D'].iloc[-1]:
                indicador = 10
                msg = f'{listasigla[-1]} VENDA/D-N2 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        elif acao['RSI'].iloc[-1] < 30 and acao['K'].iloc[-1] < 20:
            if acao['K'].iloc[-1] > acao['D'].iloc[-1]:
                indicador = 4
                msg = f'{listasigla[-1]} COMPRA/D-N2 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        else:
            indicador = 0

        print(indicador)
        listaindicador.append(indicador)

    st.markdown("INDICATORS")

    # Figuras

    fig1, fig2 = st.columns(2)

    with fig1:
        st.markdown("Ações Bloco 1")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[0:5], listaindicador[0:5])
        st.pyplot(plt)

    with fig2:
        st.markdown("Ações Bloco 2")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[5:11], listaindicador[5:11])
        st.pyplot(plt)

    st.markdown("<hr/>", unsafe_allow_html=True)

if col == "ANÁLISE TÉCNICA":
    st.write(
        """
            "ANÁLISE TÉCNICA"
        """
    )

    abev3 = web.get_data_yahoo('ABEV3.SA', start, end)  # Ambev
    bbas3 = web.get_data_yahoo('BBAS3.SA', start, end)  # Banco do Brasil
    beef3 = web.get_data_yahoo('BEEF3.SA', start, end)  # Beef
    eter3 = web.get_data_yahoo('ETER3.SA', start, end)  # Eternit
    ggbr4 = web.get_data_yahoo('GGBR4.SA', start, end)  # Gerdau
    intb3 = web.get_data_yahoo('INTB3.SA', start, end)  # Intelbras
    klbn3 = web.get_data_yahoo('KLBN3.SA', start, end)  # Klabin3
    lame4 = web.get_data_yahoo('LAME4.SA', start, end)  # Lojas americanas
    ngrd3 = web.get_data_yahoo('NGRD3.SA', start, end)  # Neogrid
    dmmo3 = web.get_data_yahoo('DMMO3.SA', start, end)  # Dmmo
    prio3 = web.get_data_yahoo('PRIO3.SA', start, end)  # Prio
    sapr11 = web.get_data_yahoo('SAPR11.SA', start, end)  # Sanepar11
    tasa4 = web.get_data_yahoo('TASA4.SA', start, end)  # Taurus
    viia3 = web.get_data_yahoo('VIIA3.SA', start, end)  # Via Varejo
    petr4 = web.get_data_yahoo('PETR4.SA', start, end)  # Petrobras
    elet3 = web.get_data_yahoo('ELET3.SA', start, end)  # Eletrobras
    mglu3 = web.get_data_yahoo('MGLU3.SA', start, end)  # MagazineLuisa
    sula11 = web.get_data_yahoo('SULA11.SA', start, end)  # Sula11
    bbse3 = web.get_data_yahoo('BBSE3.SA', start, end)  # BB seguridade
    usim5 = web.get_data_yahoo('USIM5.SA', start, end)  # USiminas
    csna3 = web.get_data_yahoo('CSNA3.SA', start, end)  # CSN
    itub4 = web.get_data_yahoo('ITUB4.SA', start, end)  # Itau
    enbr3 = web.get_data_yahoo('ENBR3.SA', start, end)  # EDP
    ciel3 = web.get_data_yahoo('CIEL3.SA', start, end)  # Cielo
    teka4 = web.get_data_yahoo('TEKA4.SA', start, end)  # Teka
    cvcb3 = web.get_data_yahoo('CVCB3.SA', start, end)  # CVC
    oibr3 = web.get_data_yahoo('OIBR3.SA', start, end)  # OI
    brml3 = web.get_data_yahoo('BRML3.SA', start, end)  # BRMALLS
    posi3 = web.get_data_yahoo('POSI3.SA', start, end)  # Positivo
    brfs3 = web.get_data_yahoo('BRFS3.SA', start, end)  # BRF
    jbss3 = web.get_data_yahoo('JBSS3.SA', start, end)  # JBS
    bbdc4 = web.get_data_yahoo('BBDC4.SA', start, end)  # BBDC4
    cogn3 = web.get_data_yahoo('COGN3.SA', start, end)  # Cogna
    itsa4 = web.get_data_yahoo('ITSA4.SA', start, end)  # Itausa
    lwsa3 = web.get_data_yahoo('LWSA3.SA', start, end)  # Localweb
    vivr3 = web.get_data_yahoo('VIVR3.SA', start, end)  # VIVER
    cimn3 = web.get_data_yahoo('CMIN3.SA', start, end)  # CMIN
    irbr3 = web.get_data_yahoo('IRBR3.SA', start, end)  # IRBR
    wege3 = web.get_data_yahoo('WEGE3.SA', start, end)  # WEG
    cxse3 = web.get_data_yahoo('CXSE3.SA', start, end)  # CAIXA SEG
    mrfg3 = web.get_data_yahoo('MRFG3.SA', start, end)  # MARFRIG
    embr3 = web.get_data_yahoo('EMBR3.SA', start, end)  # Embratel
    rail3 = web.get_data_yahoo('RAIL3.SA', start, end)  # Rail
    azul4 = web.get_data_yahoo('AZUL4.SA', start, end)  # AZul
    lupa3 = web.get_data_yahoo('LUPA3.SA', start, end)  # Lupatech
    pomo4 = web.get_data_yahoo('POMO4.SA', start, end)  # Marcopolo
    suzb3 = web.get_data_yahoo('SUZB3.SA', start, end)  # Suzano
    tots3 = web.get_data_yahoo('TOTS3.SA', start, end)  # Tots
    goll4 = web.get_data_yahoo('GOLL4.SA', start, end)  # GOL
    rcsl4 = web.get_data_yahoo('RCSL4.SA', start, end)  # Recrusul4
    klbn11 = web.get_data_yahoo('KLBN11.SA', start, end)  # Klbn11
    b3sa3 = web.get_data_yahoo('B3SA3.SA', start, end)  # B3
    ibov = web.get_data_yahoo('^BVSP', start, end)  # Ibovespa

    #################### IMPRIME CABEÇALHO
    petr4.head()
    print(petr4)


    def computeRSI(data, time_window):
        diff = data.diff(1).dropna()  # diff in one field(one day)

        # this preservers dimensions off diff values
        up_chg = 0 * diff
        down_chg = 0 * diff

        # up change is equal to the positive difference, otherwise equal to zero
        up_chg[diff > 0] = diff[diff > 0]

        # down change is equal to negative deifference, otherwise equal to zero
        down_chg[diff < 0] = diff[diff < 0]

        # check pandas documentation for ewm
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
        # values are related to exponential decay
        # we set com=time_window-1 so we get decay alpha=1/time_window
        up_chg_avg = up_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
        down_chg_avg = down_chg.ewm(com=time_window - 1, min_periods=time_window).mean()

        rs = abs(up_chg_avg / down_chg_avg)
        rsi = 100 - 100 / (1 + rs)
        return rsi


    abev3['RSI'] = computeRSI(abev3['Adj Close'], 14)
    bbas3['RSI'] = computeRSI(bbas3['Adj Close'], 14)
    beef3['RSI'] = computeRSI(beef3['Adj Close'], 14)
    eter3['RSI'] = computeRSI(eter3['Adj Close'], 14)
    ggbr4['RSI'] = computeRSI(ggbr4['Adj Close'], 14)
    intb3['RSI'] = computeRSI(intb3['Adj Close'], 14)
    klbn3['RSI'] = computeRSI(klbn3['Adj Close'], 14)
    lame4['RSI'] = computeRSI(lame4['Adj Close'], 14)
    ngrd3['RSI'] = computeRSI(ngrd3['Adj Close'], 14)
    dmmo3['RSI'] = computeRSI(dmmo3['Adj Close'], 14)
    prio3['RSI'] = computeRSI(prio3['Adj Close'], 14)
    sapr11['RSI'] = computeRSI(sapr11['Adj Close'], 14)
    tasa4['RSI'] = computeRSI(tasa4['Adj Close'], 14)
    viia3['RSI'] = computeRSI(viia3['Adj Close'], 14)
    petr4['RSI'] = computeRSI(petr4['Adj Close'], 14)
    elet3['RSI'] = computeRSI(elet3['Adj Close'], 14)
    mglu3['RSI'] = computeRSI(mglu3['Adj Close'], 14)
    sula11['RSI'] = computeRSI(sula11['Adj Close'], 14)
    bbse3['RSI'] = computeRSI(bbse3['Adj Close'], 14)
    usim5['RSI'] = computeRSI(usim5['Adj Close'], 14)
    csna3['RSI'] = computeRSI(csna3['Adj Close'], 14)
    itub4['RSI'] = computeRSI(itub4['Adj Close'], 14)
    enbr3['RSI'] = computeRSI(enbr3['Adj Close'], 14)
    ciel3['RSI'] = computeRSI(ciel3['Adj Close'], 14)
    teka4['RSI'] = computeRSI(teka4['Adj Close'], 14)
    cvcb3['RSI'] = computeRSI(cvcb3['Adj Close'], 14)
    oibr3['RSI'] = computeRSI(oibr3['Adj Close'], 14)
    brml3['RSI'] = computeRSI(brml3['Adj Close'], 14)
    posi3['RSI'] = computeRSI(posi3['Adj Close'], 14)
    brfs3['RSI'] = computeRSI(brfs3['Adj Close'], 14)
    jbss3['RSI'] = computeRSI(jbss3['Adj Close'], 14)
    bbdc4['RSI'] = computeRSI(bbdc4['Adj Close'], 14)
    cogn3['RSI'] = computeRSI(cogn3['Adj Close'], 14)
    itsa4['RSI'] = computeRSI(itsa4['Adj Close'], 14)
    lwsa3['RSI'] = computeRSI(lwsa3['Adj Close'], 14)
    vivr3['RSI'] = computeRSI(vivr3['Adj Close'], 14)
    cimn3['RSI'] = computeRSI(cimn3['Adj Close'], 14)
    irbr3['RSI'] = computeRSI(irbr3['Adj Close'], 14)
    wege3['RSI'] = computeRSI(wege3['Adj Close'], 14)
    cxse3['RSI'] = computeRSI(cxse3['Adj Close'], 14)
    mrfg3['RSI'] = computeRSI(mrfg3['Adj Close'], 14)
    embr3['RSI'] = computeRSI(embr3['Adj Close'], 14)
    rail3['RSI'] = computeRSI(rail3['Adj Close'], 14)
    azul4['RSI'] = computeRSI(azul4['Adj Close'], 14)
    lupa3['RSI'] = computeRSI(lupa3['Adj Close'], 14)
    pomo4['RSI'] = computeRSI(pomo4['Adj Close'], 14)
    suzb3['RSI'] = computeRSI(suzb3['Adj Close'], 14)
    tots3['RSI'] = computeRSI(tots3['Adj Close'], 14)
    goll4['RSI'] = computeRSI(goll4['Adj Close'], 14)
    rcsl4['RSI'] = computeRSI(rcsl4['Adj Close'], 14)
    klbn11['RSI'] = computeRSI(klbn11['Adj Close'], 14)
    b3sa3['RSI'] = computeRSI(b3sa3['Adj Close'], 14)
    ibov['RSI'] = computeRSI(ibov['Adj Close'], 14)


    def stochastic(df, k_window=13, mma_window=3):
        n_highest_high = df["High"].rolling(k_window).max()
        n_lowest_low = df["Low"].rolling(k_window).min()

        df["%K"] = (
                           (df["Adj Close"] - n_lowest_low) /
                           (n_highest_high - n_lowest_low)
                   ) * 100
        df["%D"] = df['%K'].rolling(mma_window).mean()

        df["Slow %K"] = df["%D"]
        df["Slow %D"] = df["Slow %K"].rolling(mma_window).mean()

        return df


    stochastic(abev3)
    stochastic(bbas3)
    stochastic(beef3)
    stochastic(eter3)
    stochastic(ggbr4)
    stochastic(intb3)
    stochastic(klbn3)
    stochastic(lame4)
    stochastic(ngrd3)
    stochastic(dmmo3)
    stochastic(prio3)
    stochastic(sapr11)
    stochastic(tasa4)
    stochastic(viia3)
    stochastic(petr4)
    stochastic(elet3)
    stochastic(mglu3)
    stochastic(sula11)
    stochastic(bbse3)
    stochastic(usim5)
    stochastic(csna3)
    stochastic(itub4)
    stochastic(enbr3)
    stochastic(ciel3)
    stochastic(teka4)
    stochastic(cvcb3)
    stochastic(oibr3)
    stochastic(brml3)
    stochastic(posi3)
    stochastic(brfs3)
    stochastic(jbss3)
    stochastic(bbdc4)
    stochastic(cogn3)
    stochastic(itsa4)
    stochastic(lwsa3)
    stochastic(vivr3)
    stochastic(cimn3)
    stochastic(irbr3)
    stochastic(wege3)
    stochastic(cxse3)
    stochastic(mrfg3)
    stochastic(embr3)
    stochastic(rail3)
    stochastic(azul4)
    stochastic(lupa3)
    stochastic(pomo4)
    stochastic(suzb3)
    stochastic(tots3)
    stochastic(goll4)
    stochastic(rcsl4)
    stochastic(klbn11)
    stochastic(b3sa3)
    stochastic(ibov)

    # AMBEV
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(abev3.index, abev3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(abev3.index, abev3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(abev3.index, abev3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('AMBEV (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(abev3.index, abev3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(abev3.index, abev3["%D"], alpha=0.9, color='orange')
    plt.plot(abev3.index, abev3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(abev3.index, abev3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # BBAS3
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(bbas3.index, bbas3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(bbas3.index, bbas3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(bbas3.index, bbas3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.title('BBAS3 (Adj Close)')
    plt.grid()
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(bbas3.index, bbas3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(bbas3.index, bbas3["%D"], alpha=0.9, color='orange')
    plt.plot(bbas3.index, bbas3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(bbas3.index, bbas3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # BEEF3
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(beef3.index, beef3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(beef3.index, beef3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(beef3.index, beef3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.title('BEEF3 (Adj Close)')
    plt.grid()
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(beef3.index, beef3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(beef3.index, beef3["%D"], alpha=0.9, color='orange')
    plt.plot(beef3.index, beef3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(beef3.index, beef3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # ETER3
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(eter3.index, eter3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(eter3.index, eter3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(eter3.index, eter3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.title('ETER3 (Adj Close)')
    plt.grid()
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(eter3.index, eter3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(eter3.index, eter3["%D"], alpha=0.9, color='orange')
    plt.plot(eter3.index, eter3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(eter3.index, eter3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # GGBR4
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(ggbr4.index, ggbr4['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(ggbr4.index, ggbr4['Adj Close'], alpha=0.9, color='orange')
    plt.plot(ggbr4.index, ggbr4['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('GERDAU (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(ggbr4.index, ggbr4["Slow %D"], alpha=0.9, color='blue')
    plt.plot(ggbr4.index, ggbr4["%D"], alpha=0.9, color='orange')
    plt.plot(ggbr4.index, ggbr4["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(ggbr4.index, ggbr4['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # INTELBRAS
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(intb3.index, intb3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(intb3.index, intb3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(intb3.index, intb3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('INTELBRAS (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(intb3.index, intb3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(intb3.index, intb3["%D"], alpha=0.9, color='orange')
    plt.plot(intb3.index, intb3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(intb3.index, intb3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # KLABIN3
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(klbn3.index, klbn3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(klbn3.index, klbn3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(klbn3.index, klbn3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('KLABIN 3 (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(klbn3.index, klbn3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(klbn3.index, klbn3["%D"], alpha=0.9, color='orange')
    plt.plot(klbn3.index, klbn3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(klbn3.index, klbn3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # LOJAS AMERICANAS
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(lame4.index, lame4['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(lame4.index, lame4['Adj Close'], alpha=0.9, color='orange')
    plt.plot(lame4.index, lame4['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('LOJAS AMERICANAS (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(lame4.index, lame4["Slow %D"], alpha=0.9, color='blue')
    plt.plot(lame4.index, lame4["%D"], alpha=0.9, color='orange')
    plt.plot(lame4.index, lame4["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(lame4.index, lame4['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # NEOGRID
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(ngrd3.index, ngrd3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(ngrd3.index, ngrd3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(ngrd3.index, ngrd3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('NEOGRID (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(ngrd3.index, ngrd3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(ngrd3.index, ngrd3["%D"], alpha=0.9, color='orange')
    plt.plot(ngrd3.index, ngrd3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(ngrd3.index, ngrd3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # DMMO3
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(dmmo3.index, dmmo3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(dmmo3.index, dmmo3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(dmmo3.index, dmmo3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('DMMO3 (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(dmmo3.index, dmmo3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(dmmo3.index, dmmo3["%D"], alpha=0.9, color='orange')
    plt.plot(dmmo3.index, dmmo3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(dmmo3.index, dmmo3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # PRIO
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(prio3.index, prio3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(prio3.index, prio3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(prio3.index, prio3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('PRIO (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(prio3.index, prio3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(prio3.index, prio3["%D"], alpha=0.9, color='orange')
    plt.plot(prio3.index, prio3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(prio3.index, prio3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # SANEPAR 11
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(sapr11.index, sapr11['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(sapr11.index, sapr11['Adj Close'], alpha=0.9, color='orange')
    plt.plot(sapr11.index, sapr11['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('SANEPAR 11 (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(sapr11.index, sapr11["Slow %D"], alpha=0.9, color='blue')
    plt.plot(sapr11.index, sapr11["%D"], alpha=0.9, color='orange')
    plt.plot(sapr11.index, sapr11["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(sapr11.index, sapr11['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # TAURUS
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(tasa4.index, tasa4['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(tasa4.index, tasa4['Adj Close'], alpha=0.9, color='orange')
    plt.plot(tasa4.index, tasa4['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('TAURUS (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(tasa4.index, tasa4["Slow %D"], alpha=0.9, color='blue')
    plt.plot(tasa4.index, tasa4["%D"], alpha=0.9, color='orange')
    plt.plot(tasa4.index, tasa4["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(tasa4.index, tasa4['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # VIA VAREJO
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(viia3.index, viia3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(viia3.index, viia3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(viia3.index, viia3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('VIA VAREJO (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(viia3.index, viia3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(viia3.index, viia3["%D"], alpha=0.9, color='orange')
    plt.plot(viia3.index, viia3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(viia3.index, viia3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # PETROBRAS
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(petr4.index, petr4['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(petr4.index, petr4['Adj Close'], alpha=0.9, color='orange')
    plt.plot(petr4.index, petr4['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('PETROBRAS (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(petr4.index, petr4["Slow %D"], alpha=0.9, color='blue')
    plt.plot(petr4.index, petr4["%D"], alpha=0.9, color='orange')
    plt.plot(petr4.index, petr4["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(petr4.index, petr4['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # ELETROBRAS
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(elet3.index, elet3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(elet3.index, elet3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(elet3.index, elet3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('ELETROBRAS (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(elet3.index, elet3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(elet3.index, elet3["%D"], alpha=0.9, color='orange')
    plt.plot(elet3.index, elet3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(elet3.index, elet3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # MAGAZINE LUIZA
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(mglu3.index, mglu3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(mglu3.index, mglu3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(mglu3.index, mglu3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('MAGAZINE LUIZA (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(mglu3.index, mglu3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(mglu3.index, mglu3["%D"], alpha=0.9, color='orange')
    plt.plot(mglu3.index, mglu3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(mglu3.index, mglu3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # SULA11
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(sula11.index, sula11['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(sula11.index, sula11['Adj Close'], alpha=0.9, color='orange')
    plt.plot(sula11.index, sula11['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('SULA 11 (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(sula11.index, sula11["Slow %D"], alpha=0.9, color='blue')
    plt.plot(sula11.index, sula11["%D"], alpha=0.9, color='orange')
    plt.plot(sula11.index, sula11["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(sula11.index, sula11['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # BB SEGURIDADE
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(bbse3.index, bbse3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(bbse3.index, bbse3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(bbse3.index, bbse3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('BB SEGURIDADE (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(bbse3.index, bbse3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(bbse3.index, bbse3["%D"], alpha=0.9, color='orange')
    plt.plot(bbse3.index, bbse3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(bbse3.index, bbse3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # USIMINAS
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(usim5.index, usim5['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(usim5.index, usim5['Adj Close'], alpha=0.9, color='orange')
    plt.plot(usim5.index, usim5['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('USiMINAS (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(usim5.index, usim5["Slow %D"], alpha=0.9, color='blue')
    plt.plot(usim5.index, usim5["%D"], alpha=0.9, color='orange')
    plt.plot(usim5.index, usim5["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(usim5.index, usim5['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # CSN
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(csna3.index, csna3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(csna3.index, csna3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(csna3.index, csna3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('CSN (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(csna3.index, csna3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(csna3.index, csna3["%D"], alpha=0.9, color='orange')
    plt.plot(csna3.index, csna3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(csna3.index, csna3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # ITAU
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(itub4.index, itub4['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(itub4.index, itub4['Adj Close'], alpha=0.9, color='orange')
    plt.plot(itub4.index, itub4['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('ITAU (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(itub4.index, itub4["Slow %D"], alpha=0.9, color='blue')
    plt.plot(itub4.index, itub4["%D"], alpha=0.9, color='orange')
    plt.plot(itub4.index, itub4["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(itub4.index, itub4['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # EDP
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(enbr3.index, enbr3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(enbr3.index, enbr3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(enbr3.index, enbr3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('EDP BRASIL (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(enbr3.index, enbr3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(enbr3.index, enbr3["%D"], alpha=0.9, color='orange')
    plt.plot(enbr3.index, enbr3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(enbr3.index, enbr3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # CIELO
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(ciel3.index, ciel3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(ciel3.index, ciel3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(ciel3.index, ciel3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('CIELO (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(ciel3.index, ciel3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(ciel3.index, ciel3["%D"], alpha=0.9, color='orange')
    plt.plot(ciel3.index, ciel3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(ciel3.index, ciel3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # TEKA4
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(teka4.index, teka4['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(teka4.index, teka4['Adj Close'], alpha=0.9, color='orange')
    plt.plot(teka4.index, teka4['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('TEKA 4 (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(teka4.index, teka4["Slow %D"], alpha=0.9, color='blue')
    plt.plot(teka4.index, teka4["%D"], alpha=0.9, color='orange')
    plt.plot(teka4.index, teka4["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(teka4.index, teka4['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # CVC
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(cvcb3.index, cvcb3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(cvcb3.index, cvcb3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(cvcb3.index, cvcb3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('CVC (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(cvcb3.index, cvcb3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(cvcb3.index, cvcb3["%D"], alpha=0.9, color='orange')
    plt.plot(cvcb3.index, cvcb3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(cvcb3.index, cvcb3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # OI BRASIL
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(oibr3.index, oibr3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(oibr3.index, oibr3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(oibr3.index, oibr3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('OI BRASIL (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(oibr3.index, oibr3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(oibr3.index, oibr3["%D"], alpha=0.9, color='orange')
    plt.plot(oibr3.index, oibr3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(oibr3.index, oibr3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # BRMALLS
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(brml3.index, brml3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(brml3.index, brml3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(brml3.index, brml3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('BR MALLS (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(brml3.index, brml3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(brml3.index, brml3["%D"], alpha=0.9, color='orange')
    plt.plot(brml3.index, brml3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(brml3.index, brml3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # POSITIVO
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(posi3.index, posi3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(posi3.index, posi3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(posi3.index, posi3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('POSITIVO (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(posi3.index, posi3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(posi3.index, posi3["%D"], alpha=0.9, color='orange')
    plt.plot(posi3.index, posi3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(posi3.index, posi3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # BRF
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(brfs3.index, brfs3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(brfs3.index, brfs3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(brfs3.index, brfs3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('BRF (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(brfs3.index, brfs3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(brfs3.index, brfs3["%D"], alpha=0.9, color='orange')
    plt.plot(brfs3.index, brfs3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(brfs3.index, brfs3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # JBS
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(jbss3.index, jbss3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(jbss3.index, jbss3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(jbss3.index, jbss3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('JBS (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(jbss3.index, jbss3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(jbss3.index, jbss3["%D"], alpha=0.9, color='orange')
    plt.plot(jbss3.index, jbss3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(jbss3.index, jbss3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # BRADESCO
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(bbdc4.index, bbdc4['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(bbdc4.index, bbdc4['Adj Close'], alpha=0.9, color='orange')
    plt.plot(bbdc4.index, bbdc4['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('BRADESCO (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(bbdc4.index, bbdc4["Slow %D"], alpha=0.9, color='blue')
    plt.plot(bbdc4.index, bbdc4["%D"], alpha=0.9, color='orange')
    plt.plot(bbdc4.index, bbdc4["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(bbdc4.index, bbdc4['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # COGNA
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(cogn3.index, cogn3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(cogn3.index, cogn3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(cogn3.index, cogn3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('COGNA (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(cogn3.index, cogn3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(cogn3.index, cogn3["%D"], alpha=0.9, color='orange')
    plt.plot(cogn3.index, cogn3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(cogn3.index, cogn3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # ITAUSA
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(itsa4.index, itsa4['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(itsa4.index, itsa4['Adj Close'], alpha=0.9, color='orange')
    plt.plot(itsa4.index, itsa4['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('ITAUSA (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(itsa4.index, itsa4["Slow %D"], alpha=0.9, color='blue')
    plt.plot(itsa4.index, itsa4["%D"], alpha=0.9, color='orange')
    plt.plot(itsa4.index, itsa4["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(itsa4.index, itsa4['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # LOCAWEB
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(lwsa3.index, lwsa3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(lwsa3.index, lwsa3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(lwsa3.index, lwsa3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('LOCAWEB (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(lwsa3.index, lwsa3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(lwsa3.index, lwsa3["%D"], alpha=0.9, color='orange')
    plt.plot(lwsa3.index, lwsa3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(lwsa3.index, lwsa3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # VIVER CONSTRUTORA
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(vivr3.index, vivr3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(vivr3.index, vivr3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(vivr3.index, vivr3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('VIVER CONSTRUTORA (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(vivr3.index, vivr3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(vivr3.index, vivr3["%D"], alpha=0.9, color='orange')
    plt.plot(vivr3.index, vivr3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(vivr3.index, vivr3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # CMIN3
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(cimn3.index, cimn3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(cimn3.index, cimn3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(cimn3.index, cimn3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('CMIN3 (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(cimn3.index, cimn3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(cimn3.index, cimn3["%D"], alpha=0.9, color='orange')
    plt.plot(cimn3.index, cimn3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(cimn3.index, cimn3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # IRBR
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(irbr3.index, irbr3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(irbr3.index, irbr3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(irbr3.index, irbr3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('IRBR (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(irbr3.index, irbr3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(irbr3.index, irbr3["%D"], alpha=0.9, color='orange')
    plt.plot(irbr3.index, irbr3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(irbr3.index, irbr3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # WEG
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(wege3.index, wege3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(wege3.index, wege3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(wege3.index, wege3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('WEG (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(wege3.index, wege3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(wege3.index, wege3["%D"], alpha=0.9, color='orange')
    plt.plot(wege3.index, wege3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(wege3.index, wege3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # CAIXA SEGURIDADE
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(cxse3.index, cxse3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(cxse3.index, cxse3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(cxse3.index, cxse3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('CAIXA SEGURIDADE (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(cxse3.index, cxse3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(cxse3.index, cxse3["%D"], alpha=0.9, color='orange')
    plt.plot(cxse3.index, cxse3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(cxse3.index, cxse3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # MARFRIG
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(mrfg3.index, mrfg3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(mrfg3.index, mrfg3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(mrfg3.index, mrfg3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('MARFRIG (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(mrfg3.index, mrfg3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(mrfg3.index, mrfg3["%D"], alpha=0.9, color='orange')
    plt.plot(mrfg3.index, mrfg3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(mrfg3.index, mrfg3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # EMBRATEL
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(embr3.index, embr3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(embr3.index, embr3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(embr3.index, embr3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('EMBRATEL (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(embr3.index, embr3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(embr3.index, embr3["%D"], alpha=0.9, color='orange')
    plt.plot(embr3.index, embr3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(embr3.index, embr3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # RAIL3
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(rail3.index, rail3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(rail3.index, rail3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(rail3.index, rail3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('RAIL3 (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(rail3.index, rail3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(rail3.index, rail3["%D"], alpha=0.9, color='orange')
    plt.plot(rail3.index, rail3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(rail3.index, rail3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # AZUL
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(azul4.index, azul4['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(azul4.index, azul4['Adj Close'], alpha=0.9, color='orange')
    plt.plot(azul4.index, azul4['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('AZUL (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(azul4.index, azul4["Slow %D"], alpha=0.9, color='blue')
    plt.plot(azul4.index, azul4["%D"], alpha=0.9, color='orange')
    plt.plot(azul4.index, azul4["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(azul4.index, azul4['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # LUPA3
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(lupa3.index, lupa3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(lupa3.index, lupa3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(lupa3.index, lupa3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('LUPATECH (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(lupa3.index, lupa3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(lupa3.index, lupa3["%D"], alpha=0.9, color='orange')
    plt.plot(lupa3.index, lupa3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(lupa3.index, lupa3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # POMO4
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(pomo4.index, pomo4['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(pomo4.index, pomo4['Adj Close'], alpha=0.9, color='orange')
    plt.plot(pomo4.index, pomo4['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('POMM4 (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(pomo4.index, pomo4["Slow %D"], alpha=0.9, color='blue')
    plt.plot(pomo4.index, pomo4["%D"], alpha=0.9, color='orange')
    plt.plot(pomo4.index, pomo4["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(pomo4.index, pomo4['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # SUZANO
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(suzb3.index, suzb3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(suzb3.index, suzb3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(suzb3.index, suzb3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('SUZANO (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(suzb3.index, suzb3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(suzb3.index, suzb3["%D"], alpha=0.9, color='orange')
    plt.plot(suzb3.index, suzb3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(suzb3.index, suzb3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # TOTS
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(tots3.index, tots3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(tots3.index, tots3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(tots3.index, tots3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('TOTS (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(tots3.index, tots3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(tots3.index, tots3["%D"], alpha=0.9, color='orange')
    plt.plot(tots3.index, tots3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(tots3.index, tots3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # GOL
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(goll4.index, goll4['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(goll4.index, goll4['Adj Close'], alpha=0.9, color='orange')
    plt.plot(goll4.index, goll4['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('GOL (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(goll4.index, goll4["Slow %D"], alpha=0.9, color='blue')
    plt.plot(goll4.index, goll4["%D"], alpha=0.9, color='orange')
    plt.plot(goll4.index, goll4["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(goll4.index, goll4['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # RECRUSUL
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(rcsl4.index, rcsl4['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(rcsl4.index, rcsl4['Adj Close'], alpha=0.9, color='orange')
    plt.plot(rcsl4.index, rcsl4['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('RECRUSUL (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(rcsl4.index, rcsl4["Slow %D"], alpha=0.9, color='blue')
    plt.plot(rcsl4.index, rcsl4["%D"], alpha=0.9, color='orange')
    plt.plot(rcsl4.index, rcsl4["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(rcsl4.index, rcsl4['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # KLABIN 11
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(klbn11.index, klbn11['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(klbn11.index, klbn11['Adj Close'], alpha=0.9, color='orange')
    plt.plot(klbn11.index, klbn11['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('KLABIN 11 (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(klbn11.index, klbn11["Slow %D"], alpha=0.9, color='blue')
    plt.plot(klbn11.index, klbn11["%D"], alpha=0.9, color='orange')
    plt.plot(klbn11.index, klbn11["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(klbn11.index, klbn11['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # B3
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(b3sa3.index, b3sa3['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(b3sa3.index, b3sa3['Adj Close'], alpha=0.9, color='orange')
    plt.plot(b3sa3.index, b3sa3['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('B3 (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(b3sa3.index, b3sa3["Slow %D"], alpha=0.9, color='blue')
    plt.plot(b3sa3.index, b3sa3["%D"], alpha=0.9, color='orange')
    plt.plot(b3sa3.index, b3sa3["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(b3sa3.index, b3sa3['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # IBOV
    # plot price
    plt.figure(figsize=(16, 5))
    plt.plot(ibov.index, ibov['Adj Close'].rolling(window=9).mean(), color='blue')
    plt.plot(ibov.index, ibov['Adj Close'], alpha=0.9, color='orange')
    plt.plot(ibov.index, ibov['Adj Close'].rolling(window=17).mean(), color='red')
    plt.grid()
    plt.title('IBOV (Adj Close)')
    plt.legend(['Média móvel 9', 'Cotação diária', 'Média móvel 17'])
    st.pyplot(plt)

    # PLOT ESTOCÁSTICO
    plt.figure(figsize=(16, 5))
    plt.title('ESTOCÁSTICO RSI chart')
    plt.plot(ibov.index, ibov["Slow %D"], alpha=0.9, color='blue')
    plt.plot(ibov.index, ibov["%D"], alpha=0.9, color='orange')
    plt.plot(ibov.index, ibov["Slow %K"], alpha=0.9, color='red')

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(16, 5))
    plt.title('RSI chart')
    plt.plot(ibov.index, ibov['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    st.pyplot(plt)

if col == "INDICADORES NÍVEL I":
    st.write(
        """
            "INDICADORES NÍVEL I"
        """
    )
    acoes = ['ABEV3.SA', 'BBAS3.SA', 'BEEF3.SA', 'ETER3.SA', 'GGBR4.SA', 'INTB3.SA', 'KLBN3.SA', 'LAME4.SA',
             'NGRD3.SA',
             'DMMO3.SA', 'PRIO3.SA', 'SAPR11.SA', 'TASA4.SA', 'VIIA3.SA', 'PETR4.SA', 'ELET3.SA', 'MGLU3.SA',
             'SULA11.SA', 'BBSE3.SA', 'USIM5.SA', 'CSNA3.SA', 'ITUB4.SA', 'ENBR3.SA', 'CIEL3.SA', 'TEKA4.SA',
             'CVCB3.SA', 'OIBR3.SA', 'BRML3.SA', 'POSI3.SA', 'BRFS3.SA', 'JBSS3.SA', 'BBDC4.SA', 'COGN3.SA',
             'ITSA4.SA',
             'LWSA3.SA', 'VIVR3.SA', 'CMIN3.SA', 'IRBR3.SA', 'WEGE3.SA', 'CXSE3.SA', 'MRFG3.SA', 'EMBR3.SA',
             'RAIL3.SA',
             'AZUL4.SA', 'LUPA3.SA', 'POMO4.SA', 'SUZB3.SA', 'TOTS3.SA', 'GOLL4.SA', 'RCSL4.SA', 'KLBN11.SA',
             'B3SA3.SA', '^BVSP']

    listasigla = []
    listaindicador = []

    for acao in acoes:

        listasigla.append(acao)
        acao = web.get_data_yahoo(acao, start, end)
        sinal_preco = acao['Adj Close'].iloc[-1]


        def computeRSI(data, time_window):
            diff = data.diff(1).dropna()  # diff in one field(one day)

            # this preservers dimensions off diff values
            up_chg = 0 * diff
            down_chg = 0 * diff

            # up change is equal to the positive difference, otherwise equal to zero
            up_chg[diff > 0] = diff[diff > 0]

            # down change is equal to negative deifference, otherwise equal to zero
            down_chg[diff < 0] = diff[diff < 0]

            # check pandas documentation for ewm
            # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
            # values are related to exponential decay
            # we set com=time_window-1 so we get decay alpha=1/time_window
            up_chg_avg = up_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
            down_chg_avg = down_chg.ewm(com=time_window - 1, min_periods=time_window).mean()

            rs = abs(up_chg_avg / down_chg_avg)
            rsi = 100 - 100 / (1 + rs)
            return rsi


        acao['RSI'] = computeRSI(acao['Adj Close'], 14)


        def stochastic(data, k_window, d_window, window):

            # input to function is one column from df
            # containing closing price or whatever value we want to extract K and D from

            min_val = data.rolling(window=window, center=False).min()
            max_val = data.rolling(window=window, center=False).max()

            stoch = ((data - min_val) / (max_val - min_val)) * 100

            K = stoch.rolling(window=k_window, center=False).mean()
            # K = stoch

            D = K.rolling(window=d_window, center=False).mean()
            return K, D


        acao['K'], acao['D'] = stochastic(acao['RSI'], 3, 3, 14)

        if acao['RSI'].iloc[-1] > 65 and acao['K'].iloc[-1] > 85:
            if acao['K'].iloc[-1] < acao['D'].iloc[-1]:
                indicador = 10
                msg = f'{listasigla[-1]} VENDA/D-N1 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        elif acao['RSI'].iloc[-1] < 35 and acao['K'].iloc[-1] < 25:
            if acao['K'].iloc[-1] > acao['D'].iloc[-1]:
                indicador = 4
                msg = f'{listasigla[-1]} COMPRA/D-N1 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        else:
            indicador = 0

        print(indicador)
        listaindicador.append(indicador)

    st.markdown("INDICATORS")

    # Figuras

    fig1, fig2 = st.columns(2)
    fig3, fig4 = st.columns(2)
    fig5, fig6 = st.columns(2)
    fig7, fig8 = st.columns(2)
    fig9, fig10 = st.columns(2)

    with fig1:
        st.markdown("Ações bloco 1")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[0:5], listaindicador[0:5])
        st.pyplot(plt)

    with fig2:
        st.markdown("Ações Bloco 2")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[5:10], listaindicador[5:10])
        st.pyplot(plt)

    with fig3:
        st.markdown("Ações bloco 3")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[10:15], listaindicador[10:15])
        st.pyplot(plt)

    with fig4:
        st.markdown("Ações Bloco 4")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[15:20], listaindicador[15:20])
        st.pyplot(plt)

    with fig5:
        st.markdown("Ações bloco 5")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[20:25], listaindicador[20:25])
        st.pyplot(plt)

    with fig6:
        st.markdown("Ações Bloco 6")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[25:30], listaindicador[25:30])
        st.pyplot(plt)

    with fig7:
        st.markdown("Ações bloco 7")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[30:35], listaindicador[30:35])
        st.pyplot(plt)

    with fig8:
        st.markdown("Ações Bloco 8")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[35:40], listaindicador[35:40])
        st.pyplot(plt)

    with fig9:
        st.markdown("Ações bloco 9")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[40:45], listaindicador[40:45])
        st.pyplot(plt)

    with fig10:
        st.markdown("Ações Bloco 10")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[45:50], listaindicador[45:50])
        st.pyplot(plt)

    st.markdown("<hr/>", unsafe_allow_html=True)

if col == "INDICADORES: NÍVEL II":
    st.write(
        """
            "INDICADORES NÍVEL II"
        """
    )
    acoes = ['ABEV3.SA', 'BBAS3.SA', 'BEEF3.SA', 'ETER3.SA', 'GGBR4.SA', 'INTB3.SA', 'KLBN3.SA', 'LAME4.SA',
             'NGRD3.SA',
             'DMMO3.SA', 'PRIO3.SA', 'SAPR11.SA', 'TASA4.SA', 'VIIA3.SA', 'PETR4.SA', 'ELET3.SA', 'MGLU3.SA',
             'SULA11.SA', 'BBSE3.SA', 'USIM5.SA', 'CSNA3.SA', 'ITUB4.SA', 'ENBR3.SA', 'CIEL3.SA', 'TEKA4.SA',
             'CVCB3.SA', 'OIBR3.SA', 'BRML3.SA', 'POSI3.SA', 'BRFS3.SA', 'JBSS3.SA', 'BBDC4.SA', 'COGN3.SA',
             'ITSA4.SA',
             'LWSA3.SA', 'VIVR3.SA', 'CMIN3.SA', 'IRBR3.SA', 'WEGE3.SA', 'CXSE3.SA', 'MRFG3.SA', 'EMBR3.SA',
             'RAIL3.SA',
             'AZUL4.SA', 'LUPA3.SA', 'POMO4.SA', 'SUZB3.SA', 'TOTS3.SA', 'GOLL4.SA', 'RCSL4.SA', 'KLBN11.SA',
             'B3SA3.SA', '^BVSP']

    listasigla = []
    listaindicador = []

    for acao in acoes:

        listasigla.append(acao)
        acao = web.get_data_yahoo(acao, start, end)  # Ambev
        sinal_preco = acao['Adj Close'].iloc[-1]


        def computeRSI(data, time_window):
            diff = data.diff(1).dropna()  # diff in one field(one day)

            # this preservers dimensions off diff values
            up_chg = 0 * diff
            down_chg = 0 * diff

            # up change is equal to the positive difference, otherwise equal to zero
            up_chg[diff > 0] = diff[diff > 0]

            # down change is equal to negative deifference, otherwise equal to zero
            down_chg[diff < 0] = diff[diff < 0]

            # check pandas documentation for ewm
            # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
            # values are related to exponential decay
            # we set com=time_window-1 so we get decay alpha=1/time_window
            up_chg_avg = up_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
            down_chg_avg = down_chg.ewm(com=time_window - 1, min_periods=time_window).mean()

            rs = abs(up_chg_avg / down_chg_avg)
            rsi = 100 - 100 / (1 + rs)
            return rsi


        acao['RSI'] = computeRSI(acao['Adj Close'], 14)


        def stochastic(data, k_window, d_window, window):

            # input to function is one column from df
            # containing closing price or whatever value we want to extract K and D from

            min_val = data.rolling(window=window, center=False).min()
            max_val = data.rolling(window=window, center=False).max()

            stoch = ((data - min_val) / (max_val - min_val)) * 100

            K = stoch.rolling(window=k_window, center=False).mean()
            # K = stoch

            D = K.rolling(window=d_window, center=False).mean()
            return K, D


        acao['K'], acao['D'] = stochastic(acao['RSI'], 3, 3, 14)

        if acao['RSI'].iloc[-1] > 70 and acao['K'].iloc[-1] > 90:
            if acao['K'].iloc[-1] < acao['D'].iloc[-1]:
                indicador = 10
                msg = f'{listasigla[-1]} VENDA/D-N2 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        elif acao['RSI'].iloc[-1] < 30 and acao['K'].iloc[-1] < 20:
            if acao['K'].iloc[-1] > acao['D'].iloc[-1]:
                indicador = 4
                msg = f'{listasigla[-1]} COMPRA/D-N2 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        else:
            indicador = 0

        print(indicador)
        listaindicador.append(indicador)

    st.markdown("INDICATORS")

    # Figuras

    fig1, fig2 = st.columns(2)
    fig3, fig4 = st.columns(2)
    fig5, fig6 = st.columns(2)
    fig7, fig8 = st.columns(2)
    fig9, fig10 = st.columns(2)

    with fig1:
        st.markdown("Ações bloco 1")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[0:5], listaindicador[0:5])
        st.pyplot(plt)

    with fig2:
        st.markdown("Ações Bloco 2")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[5:10], listaindicador[5:10])
        st.pyplot(plt)

    with fig3:
        st.markdown("Ações bloco 3")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[10:15], listaindicador[10:15])
        st.pyplot(plt)

    with fig4:
        st.markdown("Ações Bloco 4")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[15:20], listaindicador[15:20])
        st.pyplot(plt)

    with fig5:
        st.markdown("Ações bloco 5")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[20:25], listaindicador[20:25])
        st.pyplot(plt)

    with fig6:
        st.markdown("Ações Bloco 6")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[25:30], listaindicador[25:30])
        st.pyplot(plt)

    with fig7:
        st.markdown("Ações bloco 7")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[30:35], listaindicador[30:35])
        st.pyplot(plt)

    with fig8:
        st.markdown("Ações Bloco 8")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[35:40], listaindicador[35:40])
        st.pyplot(plt)

    with fig9:
        st.markdown("Ações bloco 9")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[40:45], listaindicador[40:45])
        st.pyplot(plt)

    with fig10:
        st.markdown("Ações Bloco 10")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[45:50], listaindicador[45:50])
        st.pyplot(plt)

    st.markdown("<hr/>", unsafe_allow_html=True)

if col2 == "CARTEIRA - INDICADORES: NÍVEL I":
    st.write(
        """
            "CARTEIRA - INDICADORES: NÍVEL I"
        """
    )

    acoes = ['BEEF3.SA', 'ETER3.SA', 'GGBR4.SA', 'NGRD3.SA', 'SAPR11.SA', 'VIIA3.SA', 'SUZB3.SA', 'CIEL3.SA',
             'KLBN11.SA', 'MNPR3.SA', 'OIBR3.SA']

    listasigla = []
    listaindicador = []

    for acao in acoes:

        listasigla.append(acao)
        acao = yf.download(tickers=acao, period="1mo", interval="1h")
        sinal_preco = acao['Adj Close'].iloc[-1]


        def computeRSI(data, time_window):
            diff = data.diff(1).dropna()  # diff in one field(one day)

            # this preservers dimensions off diff values
            up_chg = 0 * diff
            down_chg = 0 * diff

            # up change is equal to the positive difference, otherwise equal to zero
            up_chg[diff > 0] = diff[diff > 0]

            # down change is equal to negative deifference, otherwise equal to zero
            down_chg[diff < 0] = diff[diff < 0]

            # check pandas documentation for ewm
            # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
            # values are related to exponential decay
            # we set com=time_window-1 so we get decay alpha=1/time_window
            up_chg_avg = up_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
            down_chg_avg = down_chg.ewm(com=time_window - 1, min_periods=time_window).mean()

            rs = abs(up_chg_avg / down_chg_avg)
            rsi = 100 - 100 / (1 + rs)
            return rsi


        acao['RSI'] = computeRSI(acao['Adj Close'], 14)


        def stochastic(data, k_window, d_window, window):

            # input to function is one column from df
            # containing closing price or whatever value we want to extract K and D from

            min_val = data.rolling(window=window, center=False).min()
            max_val = data.rolling(window=window, center=False).max()

            stoch = ((data - min_val) / (max_val - min_val)) * 100

            K = stoch.rolling(window=k_window, center=False).mean()
            # K = stoch

            D = K.rolling(window=d_window, center=False).mean()
            return K, D


        acao['K'], acao['D'] = stochastic(acao['RSI'], 3, 3, 14)

        if acao['RSI'].iloc[-1] > 65 and acao['K'].iloc[-1] > 85:
            if acao['K'].iloc[-1] < acao['D'].iloc[-1]:
                indicador = 10
                msg = f'{listasigla[-1]} VENDA/H-N1 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        elif acao['RSI'].iloc[-1] < 35 and acao['K'].iloc[-1] < 25:
            if acao['K'].iloc[-1] > acao['D'].iloc[-1]:
                indicador = 4
                msg = f'{listasigla[-1]} COMPRA/H-N1 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        else:
            indicador = 0

        print(indicador)
        listaindicador.append(indicador)

    st.markdown("INDICATORS")

    # Figuras

    fig1, fig2 = st.columns(2)

    with fig1:
        st.markdown("Indicadores - CARTEIRA Bloco 1")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[0:5], listaindicador[0:5])
        st.pyplot(plt)

    with fig2:
        st.markdown("Indicadores - CARTEIRA Bloco 2")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[5:11], listaindicador[5:11])
        st.pyplot(plt)

    st.markdown("<hr/>", unsafe_allow_html=True)

if col2 == "CARTEIRA - INDICADORES: NÍVEL II":
    st.write(
        """
            "CARTEIRA - INDICADORES: NÍVEL II"
        """
    )

    acoes = ['BEEF3.SA', 'ETER3.SA', 'GGBR4.SA', 'NGRD3.SA', 'SAPR11.SA', 'VIIA3.SA', 'SUZB3.SA', 'CIEL3.SA',
             'KLBN11.SA', 'MNPR3.SA', 'OIBR3.SA']

    listasigla = []
    listaindicador = []

    for acao in acoes:

        listasigla.append(acao)
        acao = yf.download(tickers=acao, period="1mo", interval="1h")
        sinal_preco = acao['Adj Close'].iloc[-1]


        def computeRSI(data, time_window):
            diff = data.diff(1).dropna()  # diff in one field(one day)

            # this preservers dimensions off diff values
            up_chg = 0 * diff
            down_chg = 0 * diff

            # up change is equal to the positive difference, otherwise equal to zero
            up_chg[diff > 0] = diff[diff > 0]

            # down change is equal to negative deifference, otherwise equal to zero
            down_chg[diff < 0] = diff[diff < 0]

            # check pandas documentation for ewm
            # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
            # values are related to exponential decay
            # we set com=time_window-1 so we get decay alpha=1/time_window
            up_chg_avg = up_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
            down_chg_avg = down_chg.ewm(com=time_window - 1, min_periods=time_window).mean()

            rs = abs(up_chg_avg / down_chg_avg)
            rsi = 100 - 100 / (1 + rs)
            return rsi


        acao['RSI'] = computeRSI(acao['Adj Close'], 14)


        def stochastic(data, k_window, d_window, window):

            # input to function is one column from df
            # containing closing price or whatever value we want to extract K and D from

            min_val = data.rolling(window=window, center=False).min()
            max_val = data.rolling(window=window, center=False).max()

            stoch = ((data - min_val) / (max_val - min_val)) * 100

            K = stoch.rolling(window=k_window, center=False).mean()
            # K = stoch

            D = K.rolling(window=d_window, center=False).mean()
            return K, D


        acao['K'], acao['D'] = stochastic(acao['RSI'], 3, 3, 14)

        if acao['RSI'].iloc[-1] > 70 and acao['K'].iloc[-1] > 90:
            if acao['K'].iloc[-1] < acao['D'].iloc[-1]:
                indicador = 10
                msg = f'{listasigla[-1]} VENDA/H-N2 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        elif acao['RSI'].iloc[-1] < 30 and acao['K'].iloc[-1] < 20:
            if acao['K'].iloc[-1] > acao['D'].iloc[-1]:
                indicador = 4
                msg = f'{listasigla[-1]} COMPRA/H-N2 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        else:
            indicador = 0

        print(indicador)
        listaindicador.append(indicador)

    st.markdown("INDICATORS")

    # Figuras

    fig1, fig2 = st.columns(2)

    with fig1:
        st.markdown("Indicadores - CARTEIRA Bloco 1")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[0:5], listaindicador[0:5])
        st.pyplot(plt)

    with fig2:
        st.markdown("Indicadores - CARTEIRA Bloco 2")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[5:11], listaindicador[5:11])
        st.pyplot(plt)

    st.markdown("<hr/>", unsafe_allow_html=True)

if col2 == "ANÁLISE TÉCNICA":
    st.write(
        """
            "ANÁLISE TÉCNICA ------------ ATUALIZAR E INSERIR"
        """
    )

if col2 == "INDICADORES NÍVEL I":
    st.write(
        """
            "INDICADORES NÍVEL I"
        """
    )

    acoes = ['ABEV3.SA', 'BBAS3.SA', 'BEEF3.SA', 'ETER3.SA', 'GGBR4.SA', 'INTB3.SA', 'KLBN3.SA', 'LAME4.SA',
             'NGRD3.SA',
             'DMMO3.SA', 'PRIO3.SA', 'SAPR11.SA', 'TASA4.SA', 'VIIA3.SA', 'PETR4.SA', 'ELET3.SA', 'MGLU3.SA',
             'SULA11.SA', 'BBSE3.SA', 'USIM5.SA', 'CSNA3.SA', 'ITUB4.SA', 'ENBR3.SA', 'CIEL3.SA', 'TEKA4.SA',
             'CVCB3.SA', 'OIBR3.SA', 'BRML3.SA', 'POSI3.SA', 'BRFS3.SA', 'JBSS3.SA', 'BBDC4.SA', 'COGN3.SA',
             'ITSA4.SA',
             'LWSA3.SA', 'VIVR3.SA', 'CMIN3.SA', 'IRBR3.SA', 'WEGE3.SA', 'CXSE3.SA', 'MRFG3.SA', 'EMBR3.SA',
             'RAIL3.SA',
             'AZUL4.SA', 'LUPA3.SA', 'POMO4.SA', 'SUZB3.SA', 'TOTS3.SA', 'GOLL4.SA', 'RCSL4.SA', 'KLBN11.SA',
             'B3SA3.SA', '^BVSP']

    listasigla = []
    listaindicador = []

    for acao in acoes:

        listasigla.append(acao)
        acao = yf.download(tickers=acao, period="1mo", interval="1h")
        sinal_preco = acao['Adj Close'].iloc[-1]


        def computeRSI(data, time_window):
            diff = data.diff(1).dropna()  # diff in one field(one day)

            # this preservers dimensions off diff values
            up_chg = 0 * diff
            down_chg = 0 * diff

            # up change is equal to the positive difference, otherwise equal to zero
            up_chg[diff > 0] = diff[diff > 0]

            # down change is equal to negative deifference, otherwise equal to zero
            down_chg[diff < 0] = diff[diff < 0]

            # check pandas documentation for ewm
            # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
            # values are related to exponential decay
            # we set com=time_window-1 so we get decay alpha=1/time_window
            up_chg_avg = up_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
            down_chg_avg = down_chg.ewm(com=time_window - 1, min_periods=time_window).mean()

            rs = abs(up_chg_avg / down_chg_avg)
            rsi = 100 - 100 / (1 + rs)
            return rsi


        acao['RSI'] = computeRSI(acao['Adj Close'], 14)


        def stochastic(data, k_window, d_window, window):

            # input to function is one column from df
            # containing closing price or whatever value we want to extract K and D from

            min_val = data.rolling(window=window, center=False).min()
            max_val = data.rolling(window=window, center=False).max()

            stoch = ((data - min_val) / (max_val - min_val)) * 100

            K = stoch.rolling(window=k_window, center=False).mean()
            # K = stoch

            D = K.rolling(window=d_window, center=False).mean()
            return K, D


        acao['K'], acao['D'] = stochastic(acao['RSI'], 3, 3, 14)

        if acao['RSI'].iloc[-1] > 65 and acao['K'].iloc[-1] > 85:
            if acao['K'].iloc[-1] < acao['D'].iloc[-1]:
                indicador = 10
                msg = f'{listasigla[-1]} VENDA/H-N1 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        elif acao['RSI'].iloc[-1] < 35 and acao['K'].iloc[-1] < 25:
            if acao['K'].iloc[-1] > acao['D'].iloc[-1]:
                indicador = 4
                msg = f'{listasigla[-1]} COMPRA/H-N1 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        else:
            indicador = 0

        print(indicador)
        listaindicador.append(indicador)

    st.markdown("INDICATORS")

    # Figuras

    fig1, fig2 = st.columns(2)
    fig3, fig4 = st.columns(2)
    fig5, fig6 = st.columns(2)
    fig7, fig8 = st.columns(2)
    fig9, fig10 = st.columns(2)

    with fig1:
        st.markdown("Ações bloco 1")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[0:5], listaindicador[0:5])
        st.pyplot(plt)

    with fig2:
        st.markdown("Ações Bloco 2")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[5:10], listaindicador[5:10])
        st.pyplot(plt)

    with fig3:
        st.markdown("Ações bloco 3")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[10:15], listaindicador[10:15])
        st.pyplot(plt)

    with fig4:
        st.markdown("Ações Bloco 4")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[15:20], listaindicador[15:20])
        st.pyplot(plt)

    with fig5:
        st.markdown("Ações bloco 5")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[20:25], listaindicador[20:25])
        st.pyplot(plt)

    with fig6:
        st.markdown("Ações Bloco 6")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[25:30], listaindicador[25:30])
        st.pyplot(plt)

    with fig7:
        st.markdown("Ações bloco 7")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[30:35], listaindicador[30:35])
        st.pyplot(plt)

    with fig8:
        st.markdown("Ações Bloco 8")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[35:40], listaindicador[35:40])
        st.pyplot(plt)

    with fig9:
        st.markdown("Ações bloco 9")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[40:45], listaindicador[40:45])
        st.pyplot(plt)

    with fig10:
        st.markdown("Ações Bloco 10")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[45:50], listaindicador[45:50])
        st.pyplot(plt)

    st.markdown("<hr/>", unsafe_allow_html=True)

if col2 == "INDICADORES NÍVEL II ":
    st.write(
        """
            "INDICADORES NÍVEL II"
        """
    )

    acoes = ['ABEV3.SA', 'BBAS3.SA', 'BEEF3.SA', 'ETER3.SA', 'GGBR4.SA', 'INTB3.SA', 'KLBN3.SA', 'LAME4.SA',
             'NGRD3.SA',
             'DMMO3.SA', 'PRIO3.SA', 'SAPR11.SA', 'TASA4.SA', 'VIIA3.SA', 'PETR4.SA', 'ELET3.SA', 'MGLU3.SA',
             'SULA11.SA', 'BBSE3.SA', 'USIM5.SA', 'CSNA3.SA', 'ITUB4.SA', 'ENBR3.SA', 'CIEL3.SA', 'TEKA4.SA',
             'CVCB3.SA', 'OIBR3.SA', 'BRML3.SA', 'POSI3.SA', 'BRFS3.SA', 'JBSS3.SA', 'BBDC4.SA', 'COGN3.SA',
             'ITSA4.SA',
             'LWSA3.SA', 'VIVR3.SA', 'CMIN3.SA', 'IRBR3.SA', 'WEGE3.SA', 'CXSE3.SA', 'MRFG3.SA', 'EMBR3.SA',
             'RAIL3.SA',
             'AZUL4.SA', 'LUPA3.SA', 'POMO4.SA', 'SUZB3.SA', 'TOTS3.SA', 'GOLL4.SA', 'RCSL4.SA', 'KLBN11.SA',
             'B3SA3.SA', '^BVSP']

    listasigla = []
    listaindicador = []

    for acao in acoes:

        listasigla.append(acao)
        acao = yf.download(tickers=acao, period="1mo", interval="1h")
        sinal_preco = acao['Adj Close'].iloc[-1]


        def computeRSI(data, time_window):
            diff = data.diff(1).dropna()  # diff in one field(one day)

            # this preservers dimensions off diff values
            up_chg = 0 * diff
            down_chg = 0 * diff

            # up change is equal to the positive difference, otherwise equal to zero
            up_chg[diff > 0] = diff[diff > 0]

            # down change is equal to negative deifference, otherwise equal to zero
            down_chg[diff < 0] = diff[diff < 0]

            # check pandas documentation for ewm
            # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
            # values are related to exponential decay
            # we set com=time_window-1 so we get decay alpha=1/time_window
            up_chg_avg = up_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
            down_chg_avg = down_chg.ewm(com=time_window - 1, min_periods=time_window).mean()

            rs = abs(up_chg_avg / down_chg_avg)
            rsi = 100 - 100 / (1 + rs)
            return rsi


        acao['RSI'] = computeRSI(acao['Adj Close'], 14)


        def stochastic(data, k_window, d_window, window):

            # input to function is one column from df
            # containing closing price or whatever value we want to extract K and D from

            min_val = data.rolling(window=window, center=False).min()
            max_val = data.rolling(window=window, center=False).max()

            stoch = ((data - min_val) / (max_val - min_val)) * 100

            K = stoch.rolling(window=k_window, center=False).mean()
            # K = stoch

            D = K.rolling(window=d_window, center=False).mean()
            return K, D


        acao['K'], acao['D'] = stochastic(acao['RSI'], 3, 3, 14)

        if acao['RSI'].iloc[-1] > 70 and acao['K'].iloc[-1] > 90:
            if acao['K'].iloc[-1] < acao['D'].iloc[-1]:
                indicador = 10
                msg = f'{listasigla[-1]} VENDA/H-N2 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        elif acao['RSI'].iloc[-1] < 30 and acao['K'].iloc[-1] < 20:
            if acao['K'].iloc[-1] > acao['D'].iloc[-1]:
                indicador = 4
                msg = f'{listasigla[-1]} COMPRA/H-N2 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        else:
            indicador = 0

        print(indicador)
        listaindicador.append(indicador)

    st.markdown("INDICATORS")

    # Figuras

    fig1, fig2 = st.columns(2)
    fig3, fig4 = st.columns(2)
    fig5, fig6 = st.columns(2)
    fig7, fig8 = st.columns(2)
    fig9, fig10 = st.columns(2)

    with fig1:
        st.markdown("Ações bloco 1")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[0:5], listaindicador[0:5])
        st.pyplot(plt)

    with fig2:
        st.markdown("Ações Bloco 2")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[5:10], listaindicador[5:10])
        st.pyplot(plt)

    with fig3:
        st.markdown("Ações bloco 3")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[10:15], listaindicador[10:15])
        st.pyplot(plt)

    with fig4:
        st.markdown("Ações Bloco 4")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[15:20], listaindicador[15:20])
        st.pyplot(plt)

    with fig5:
        st.markdown("Ações bloco 5")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[20:25], listaindicador[20:25])
        st.pyplot(plt)

    with fig6:
        st.markdown("Ações Bloco 6")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[25:30], listaindicador[25:30])
        st.pyplot(plt)

    with fig7:
        st.markdown("Ações bloco 7")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[30:35], listaindicador[30:35])
        st.pyplot(plt)

    with fig8:
        st.markdown("Ações Bloco 8")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[35:40], listaindicador[35:40])
        st.pyplot(plt)

    with fig9:
        st.markdown("Ações bloco 9")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[40:45], listaindicador[40:45])
        st.pyplot(plt)

    with fig10:
        st.markdown("Ações Bloco 10")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[45:50], listaindicador[45:50])
        st.pyplot(plt)

    st.markdown("<hr/>", unsafe_allow_html=True)

if col3 == "INDICADORES NÍVEL I":
    st.write(
        """
            "CRIPTOMOEDAS - INDICADORES: NÍVEL I"
        """
    )
    siglas = ['SHIBUSDT', 'DOGEBTC', 'IOTXBTC', 'XRPBTC', 'BTTUSDT', 'ETHBTC', 'GXSBTC', 'ROSEBTC', 'ATOMBTC',
              'MANABTC', 'STXBTC', 'SOLBTC', 'DOTBTC', 'MITHBTC', 'ALICEBTC', 'COCOSBNB', 'REQBTC', 'ALICEBTC',
              'BRDBTC', 'ADABTC', 'BCHUPUSDT', 'SUSHIBTC']

    listasigla = []
    listaindicador = []

    for sigla in siglas:

        listasigla.append(sigla)
        # Pegando preços intervalo de 1 dia
        btcbrl = client.get_klines(symbol=sigla, interval=Client.KLINE_INTERVAL_1DAY)

        # transformando o json
        with open('btc_df.json', 'w') as e:
            json.dump(btcbrl, e)

        for line in btcbrl:
            del line[5:]

        btc_df = pd.DataFrame(btcbrl, columns=['date', 'open', 'high', 'low', 'close'])
        btc_df.set_index('date', inplace=True)
        btc_df.index = pd.to_datetime(btc_df.index, unit='ms')

        btc_df['close'] = pd.to_numeric(btc_df['close'])

        # DATAFRAME
        df = btc_df


        # calculating Stoch RSI
        #  -- Same as the above function but uses EMA, not SMA
        def StochRSI_EMA(series, period=14, smoothK=11, smoothD=6):
            # Calculate RSI
            delta = series.diff().dropna()
            ups = delta * 0
            downs = ups.copy()
            ups[delta > 0] = delta[delta > 0]
            downs[delta < 0] = -delta[delta < 0]
            ups[ups.index[period - 1]] = np.mean(ups[:period])  # first value is sum of avg gains
            ups = ups.drop(ups.index[:(period - 1)])
            downs[downs.index[period - 1]] = np.mean(downs[:period])  # first value is sum of avg losses
            downs = downs.drop(downs.index[:(period - 1)])
            rs = ups.ewm(com=period - 1, min_periods=0, adjust=False, ignore_na=False).mean() / \
                 downs.ewm(com=period - 1, min_periods=0, adjust=False, ignore_na=False).mean()
            rsi = 100 - 100 / (1 + rs)

            # Calculate StochRSI
            stochrsi = (rsi - rsi.rolling(period).min()) / (rsi.rolling(period).max() - rsi.rolling(period).min())
            stochrsi_K = stochrsi.ewm(span=smoothK).mean()
            stochrsi_D = stochrsi_K.ewm(span=smoothD).mean()

            return stochrsi, stochrsi_K, stochrsi_D


        df['Stoc'], df['K'], df['D'] = StochRSI_EMA(df['close'])
        print(df)

        # SINAL PREÇO
        sinal_preco = df.iloc[-1]

        if df['K'].iloc[-1] > 85:
            if df['K'].iloc[-1] < df['D'].iloc[-1]:
                indicador = 10
                msg = f'{listasigla[-1]} VENDA/D-N1 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        elif df['K'].iloc[-1] < 25:
            if df['K'].iloc[-1] > df['D'].iloc[-1]:
                indicador = 4
                msg = f'{listasigla[-1]} COMPRA/D-N1 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        else:
            indicador = 0

        print(indicador)
        listaindicador.append(indicador)

    st.markdown("INDICATORS")

    # Figuras

    fig1, fig2 = st.columns(2)
    fig3, fig4 = st.columns(2)

    with fig1:
        st.markdown("Cripto Bloco 1")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[0:6], listaindicador[0:5])
        st.pyplot(plt)

    with fig2:
        st.markdown("Cripto Bloco 2")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[6:12], listaindicador[5:11])
        st.pyplot(plt)

    with fig3:
        st.markdown("Cripto Bloco 3")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[12:18], listaindicador[11:17])
        st.pyplot(plt)

    with fig4:
        st.markdown("Cripto Bloco 4")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[18:24], listaindicador[17:23])
        st.pyplot(plt)

    st.markdown("<hr/>", unsafe_allow_html=True)

if col3 == "INDICADORES NÍVEL II":
    st.write(
        """
            "CRIPTOMOEDAS - INDICADORES: NÍVEL II"
        """
    )
    siglas = ['SHIBUSDT', 'DOGEBTC', 'IOTXBTC', 'XRPBTC', 'BTTUSDT', 'ETHBTC', 'GXSBTC', 'ROSEBTC', 'ATOMBTC',
              'MANABTC', 'STXBTC', 'SOLBTC', 'DOTBTC', 'MITHBTC', 'ALICEBTC', 'COCOSBNB', 'REQBTC', 'ALICEBTC',
              'BRDBTC', 'ADABTC', 'BCHUPUSDT', 'SUSHIBTC']

    listasigla = []
    listaindicador = []

    for sigla in siglas:

        listasigla.append(sigla)
        # Pegando preços intervalo de 1 dia
        btcbrl = client.get_klines(symbol=sigla, interval=Client.KLINE_INTERVAL_1DAY)

        # transformando o json
        with open('btc_df.json', 'w') as e:
            json.dump(btcbrl, e)

        for line in btcbrl:
            del line[5:]

        btc_df = pd.DataFrame(btcbrl, columns=['date', 'open', 'high', 'low', 'close'])
        btc_df.set_index('date', inplace=True)
        btc_df.index = pd.to_datetime(btc_df.index, unit='ms')

        btc_df['close'] = pd.to_numeric(btc_df['close'])

        # DATAFRAME
        df = btc_df


        # calculating Stoch RSI
        #  -- Same as the above function but uses EMA, not SMA
        def StochRSI_EMA(series, period=14, smoothK=11, smoothD=6):
            # Calculate RSI
            delta = series.diff().dropna()
            ups = delta * 0
            downs = ups.copy()
            ups[delta > 0] = delta[delta > 0]
            downs[delta < 0] = -delta[delta < 0]
            ups[ups.index[period - 1]] = np.mean(ups[:period])  # first value is sum of avg gains
            ups = ups.drop(ups.index[:(period - 1)])
            downs[downs.index[period - 1]] = np.mean(downs[:period])  # first value is sum of avg losses
            downs = downs.drop(downs.index[:(period - 1)])
            rs = ups.ewm(com=period - 1, min_periods=0, adjust=False, ignore_na=False).mean() / \
                 downs.ewm(com=period - 1, min_periods=0, adjust=False, ignore_na=False).mean()
            rsi = 100 - 100 / (1 + rs)

            # Calculate StochRSI
            stochrsi = (rsi - rsi.rolling(period).min()) / (rsi.rolling(period).max() - rsi.rolling(period).min())
            stochrsi_K = stochrsi.ewm(span=smoothK).mean()
            stochrsi_D = stochrsi_K.ewm(span=smoothD).mean()

            return stochrsi, stochrsi_K, stochrsi_D


        df['Stoc'], df['K'], df['D'] = StochRSI_EMA(df['close'])
        print(df)

        # SINAL PREÇO
        sinal_preco = df.iloc[-1]

        if df['K'].iloc[-1] > 90:
            if df['K'].iloc[-1] < df['D'].iloc[-1]:
                indicador = 10
                msg = f'{listasigla[-1]} VENDA/D-N2 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        elif df['K'].iloc[-1] < 20:
            if df['K'].iloc[-1] > df['D'].iloc[-1]:
                indicador = 4
                msg = f'{listasigla[-1]} COMPRA/D-N2 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        else:
            indicador = 0

        print(indicador)
        listaindicador.append(indicador)

    st.markdown("INDICATORS")

    # Figuras

    fig1, fig2 = st.columns(2)
    fig3, fig4 = st.columns(2)

    with fig1:
        st.markdown("Cripto Bloco 1")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[0:6], listaindicador[0:5])
        st.pyplot(plt)

    with fig2:
        st.markdown("Cripto Bloco 2")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[6:12], listaindicador[5:11])
        st.pyplot(plt)

    with fig3:
        st.markdown("Cripto Bloco 3")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[12:18], listaindicador[11:17])
        st.pyplot(plt)

    with fig4:
        st.markdown("Cripto Bloco 4")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[18:24], listaindicador[17:23])
        st.pyplot(plt)

    st.markdown("<hr/>", unsafe_allow_html=True)


if col4 == "INDICADORES NÍVEL I ":
    st.write(
        """
            "CRIPTOMOEDAS - INDICADORES: NÍVEL I"
        """
    )

    siglas = ['SHIBUSDT', 'DOGEBTC', 'IOTXBTC', 'XRPBTC', 'BTTUSDT', 'ETHBTC', 'GXSBTC', 'ROSEBTC', 'ATOMBTC',
              'MANABTC', 'STXBTC', 'SOLBTC', 'DOTBTC', 'MITHBTC', 'ALICEBTC', 'COCOSBNB', 'REQBTC', 'ALICEBTC',
              'BRDBTC', 'ADABTC', 'BCHUPUSDT', 'SUSHIBTC']

    listasigla = []
    listaindicador = []

    for sigla in siglas:

        listasigla.append(sigla)
        # Pegando preços intervalo de 1 semana
        btcbrl = client.get_klines(symbol=sigla, interval=Client.KLINE_INTERVAL_1WEEK)

        # transformando o json
        with open('btc_df.json', 'w') as e:
            json.dump(btcbrl, e)

        for line in btcbrl:
            del line[5:]

        btc_df = pd.DataFrame(btcbrl, columns=['date', 'open', 'high', 'low', 'close'])
        btc_df.set_index('date', inplace=True)
        btc_df.index = pd.to_datetime(btc_df.index, unit='ms')

        btc_df['close'] = pd.to_numeric(btc_df['close'])

        # DATAFRAME
        df = btc_df


        # calculating Stoch RSI
        #  -- Same as the above function but uses EMA, not SMA
        def StochRSI_EMA(series, period=14, smoothK=11, smoothD=6):
            # Calculate RSI
            delta = series.diff().dropna()
            ups = delta * 0
            downs = ups.copy()
            ups[delta > 0] = delta[delta > 0]
            downs[delta < 0] = -delta[delta < 0]
            ups[ups.index[period - 1]] = np.mean(ups[:period])  # first value is sum of avg gains
            ups = ups.drop(ups.index[:(period - 1)])
            downs[downs.index[period - 1]] = np.mean(downs[:period])  # first value is sum of avg losses
            downs = downs.drop(downs.index[:(period - 1)])
            rs = ups.ewm(com=period - 1, min_periods=0, adjust=False, ignore_na=False).mean() / \
                 downs.ewm(com=period - 1, min_periods=0, adjust=False, ignore_na=False).mean()
            rsi = 100 - 100 / (1 + rs)

            # Calculate StochRSI
            stochrsi = (rsi - rsi.rolling(period).min()) / (rsi.rolling(period).max() - rsi.rolling(period).min())
            stochrsi_K = stochrsi.ewm(span=smoothK).mean()
            stochrsi_D = stochrsi_K.ewm(span=smoothD).mean()

            return stochrsi, stochrsi_K, stochrsi_D


        df['Stoc'], df['K'], df['D'] = StochRSI_EMA(df['close'])
        print(df)

        # SINAL PREÇO
        sinal_preco = df.iloc[-1]

        if df['K'].iloc[-1] > 85:
            if df['K'].iloc[-1] < df['D'].iloc[-1]:
                indicador = 10
                msg = f'{listasigla[-1]} VENDA/S-N1 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        elif df['K'].iloc[-1] < 25:
            if df['K'].iloc[-1] > df['D'].iloc[-1]:
                indicador = 4
                msg = f'{listasigla[-1]} COMPRA/S-N1 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        else:
            indicador = 0

        print(indicador)
        listaindicador.append(indicador)

    st.markdown("INDICATORS")

    # Figuras

    fig1, fig2 = st.columns(2)
    fig3, fig4 = st.columns(2)

    with fig1:
        st.markdown("Cripto Bloco 1")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[0:6], listaindicador[0:5])
        st.pyplot(plt)

    with fig2:
        st.markdown("Cripto Bloco 2")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[6:12], listaindicador[5:11])
        st.pyplot(plt)

    with fig3:
        st.markdown("Cripto Bloco 3")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[12:18], listaindicador[11:17])
        st.pyplot(plt)

    with fig4:
        st.markdown("Cripto Bloco 4")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[18:24], listaindicador[17:23])
        st.pyplot(plt)

    st.markdown("<hr/>", unsafe_allow_html=True)

if col4 == "INDICADORES NÍVEL II ":
    st.write(
        """
            "CRIPTOMOEDAS - INDICADORES: NÍVEL II"
        """
    )

    siglas = ['SHIBUSDT','DOGEBTC','IOTXBTC','XRPBTC','BTTUSDT','ETHBTC','GXSBTC','ROSEBTC','ATOMBTC','MANABTC','STXBTC','SOLBTC','DOTBTC','MITHBTC','ALICEBTC', 'COCOSBNB', 'REQBTC', 'ALICEBTC', 'BRDBTC', 'ADABTC']



    listasigla = []
    listaindicador = []

    for sigla in siglas:

        listasigla.append(sigla)
        # Pegando preços intervalo de 1 semana
        btcbrl = client.get_klines(symbol=sigla, interval=Client.KLINE_INTERVAL_1WEEK)



        # transformando o json
        with open('btc_df.json', 'w') as e:
            json.dump(btcbrl, e)

        for line in btcbrl:
            del line[5:]

        btc_df = pd.DataFrame(btcbrl, columns=['date', 'open', 'high', 'low', 'close'])
        btc_df.set_index('date', inplace=True)
        btc_df.index = pd.to_datetime(btc_df.index, unit='ms')

        btc_df['close'] = pd.to_numeric(btc_df['close'])

        # DATAFRAME
        df = btc_df



        # calculating Stoch RSI
        #  -- Same as the above function but uses EMA, not SMA
        def StochRSI_EMA(series, period=14, smoothK=11, smoothD=6):
            # Calculate RSI
            delta = series.diff().dropna()
            ups = delta * 0
            downs = ups.copy()
            ups[delta > 0] = delta[delta > 0]
            downs[delta < 0] = -delta[delta < 0]
            ups[ups.index[period - 1]] = np.mean(ups[:period])  # first value is sum of avg gains
            ups = ups.drop(ups.index[:(period - 1)])
            downs[downs.index[period - 1]] = np.mean(downs[:period])  # first value is sum of avg losses
            downs = downs.drop(downs.index[:(period - 1)])
            rs = ups.ewm(com=period - 1, min_periods=0, adjust=False, ignore_na=False).mean() / \
                 downs.ewm(com=period - 1, min_periods=0, adjust=False, ignore_na=False).mean()
            rsi = 100 - 100 / (1 + rs)

            # Calculate StochRSI
            stochrsi = (rsi - rsi.rolling(period).min()) / (rsi.rolling(period).max() - rsi.rolling(period).min())
            stochrsi_K = stochrsi.ewm(span=smoothK).mean()
            stochrsi_D = stochrsi_K.ewm(span=smoothD).mean()

            return stochrsi, stochrsi_K, stochrsi_D


        df['Stoc'], df['K'], df['D'] = StochRSI_EMA(df['close'])
        print(df)

        #SINAL PREÇO
        sinal_preco = df.iloc[-1]

        if df['K'].iloc[-1] > 90:
            if df['K'].iloc[-1] < df['D'].iloc[-1]:
                indicador = 10
                msg = f'{listasigla[-1]} VENDA/H-N2 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        elif df['K'].iloc[-1] < 20:
            if df['K'].iloc[-1] > df['D'].iloc[-1]:
                indicador = 4
                msg = f'{listasigla[-1]} COMPRA/H-N2 - Preço atual: {sinal_preco}'
                envia_mensagem(msg, chat_id, my_token)
            else:
                indicador = 0
        else:
            indicador = 0

        print(indicador)
        listaindicador.append(indicador)

    st.markdown("INDICATORS")

    # Figuras

    fig1, fig2 = st.columns(2)
    fig3, fig4 = st.columns(2)

    with fig1:
        st.markdown("Cripto Bloco 1")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[0:6], listaindicador[0:5])
        st.pyplot(plt)

    with fig2:
        st.markdown("Cripto Bloco 2")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[6:12], listaindicador[5:11])
        st.pyplot(plt)

    with fig3:
        st.markdown("Cripto Bloco 3")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[12:18], listaindicador[11:17])
        st.pyplot(plt)

    with fig4:
        st.markdown("Cripto Bloco 4")
        fig, ax = plt.subplots()
        # Use automatic FuncFormatter creation
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(listasigla[18:24], listaindicador[17:23])
        st.pyplot(plt)

    st.markdown("<hr/>", unsafe_allow_html=True)

msg = f'#####################################' \
      f' ANÁLISE CONCLUÍDA ' \
      f'#####################################'
envia_mensagem(msg, chat_id, my_token)
