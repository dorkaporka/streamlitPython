import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Wczytanie danych
df = pd.read_csv("ev_charging_patterns.csv")  #

# Podział strony na kolumny
col1, col2 = st.columns([0.25, 0.75])

# Tytuł
col2.subheader("Pierwszy wykres")

# Wykres: jeśli jest kolumna liczbową, pokazujemy histogram
liczbowe = df.select_dtypes(include=['int64','float64']).columns.tolist()
tekstowe = df.select_dtypes(include=['object']).columns.tolist()

if liczbowe:
    plt.figure(figsize=(6,4)) # w calach
    sns.histplot(df[liczbowe[0]], kde=True) #dla pierwszej kolumny liczbowej
    col2.pyplot(plt)

#Górna część do poruszania sie itd
st.sidebar.header("Wybór interakcji")

#która kolumna do wykresu
wybrana_kolumna = st.sidebar.selectbox("Wybierz kolumnę do wykresu", df.columns)

#dla tekstowych filtrowanie
if tekstowe:
    filtr_tekst = st.sidebar.text_input("Filtruj po tekście (kolumny tekstowe)")
else:
    filtr_tekst = ""

#slider dla liczbowych
if wybrana_kolumna in liczbowe:
    min_val = float(df[wybrana_kolumna].min())
    max_val = float(df[wybrana_kolumna].max())
    zakres = st.sidebar.slider("Wybierz zakres wartości", min_val, max_val, (min_val, max_val))
else:
    zakres = None

#checkbox do wykresu interaktywnego
interaktywny = st.sidebar.checkbox("Pokaż wykres Plotly")

#filtrowanie danych
df_filtered = df.copy()

if filtr_tekst and tekstowe:
    for kol in tekstowe:
        df_filtered = df_filtered[df_filtered[kol].astype(str).str.contains(filtr_tekst, case=False, na=False)]

if zakres and wybrana_kolumna in liczbowe:
    df_filtered = df_filtered[(df_filtered[wybrana_kolumna] >= zakres[0]) &
                            #góra = wartosci w kolumnie wieksze lub rowne dolnej granicy slidera
                              (df_filtered[wybrana_kolumna] <= zakres[1])]
                            #góra = górną granice sprawddza
#df_filtered = wybiera wiersze, spełniające kryteria
#wykresy
col2.subheader("Histogram / Wykres liczbowy")
if wybrana_kolumna in liczbowe:
    fig, ax = plt.subplots()
    sns.histplot(df_filtered[wybrana_kolumna], kde=True, ax=ax)
    #Kernel Density Estimate - przyblizony rozklad wartosci w kolumnie
    col2.pyplot(fig)

if interaktywny:
    if wybrana_kolumna in liczbowe:
        fig_px = px.histogram(df_filtered, x=wybrana_kolumna, nbins=20, title=f"Interaktywny histogram {wybrana_kolumna}")
    #nbins=20 - ilosc słupków w histogramie
    else:
        fig_px = px.histogram(df_filtered, x=wybrana_kolumna, title=f"Interaktywny wykres {wybrana_kolumna}")
    col2.plotly_chart(fig_px)