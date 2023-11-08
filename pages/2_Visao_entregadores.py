#Libraries

from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

#bibliotecas necessárias 
import folium
import pandas as pd
from datetime import datetime
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config( page_title='Visão Entregadores', page_icon='🚚', layout= 'wide' )

# -------------------------------------------
# Funções
# -------------------------------------------

def top_delivers (df1, top_asc):
    df2 = (df1.loc[: , ['Delivery_person_ID', 'City', 'Time_taken(min)']]
              .groupby ( ['City', 'Delivery_person_ID'])
              .mean()
              .sort_values( ['City', 'Time_taken(min)'], ascending = top_asc ).reset_index() )
    df_aux01 = df2.loc[df2['City'] == 'Metropolitian ' , : ].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban ', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban ' , :].head(10)

    df3 = pd.concat ([df_aux01, df_aux02, df_aux03]).reset_index( drop=True )
            
    return df3
                

def clean_code (df1): # Dentro do parenteses eu preciso utilizar o Df1 que esta em toda linha de comando se não pode dar errado.
    """ Esta função tem a responsabilidade de limpar o dataframe

        Tipos de Limpeza:
        1. Remoção dos dados NaN
        2. Mudançã do tipo da coluna de dados
        3. Remoção dos espaços das váriaveis de texto
        4. Formatação da coluna de datas
        5. Limpeza da coluna de tempo ( Remoção do texto da variável numérica )

        Input: Dataframe
        Output: Dataframe
    """

#1. convertendo a coluna Age de Texto para numero

    linhas_selecionadas = (df1[ 'Delivery_person_Age'] !='NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1[ 'Road_traffic_density'] !='NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1[ 'City'] !='NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1[ 'Festival'] !='NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    df1['Delivery_person_Age'] = df1 ['Delivery_person_Age'].astype ( int )


#2. Convertendo a coluna Ratings de texto para numero decimal ( FLOAT ) 

    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'] .astype( float )

#3. Convertendo a coluna order_date de texto para data

    df1['Order_Date'] = pd.to_datetime (df1['Order_Date'], format = '%d-%m-%Y')

#4. Convertendo multiple_deliveries de texto para numero inteiro ( INT ) 

    linhas_selecionadas = (df1[ 'multiple_deliveries'] !='NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    df1['multiple_deliveries'] = df1 ['multiple_deliveries'].astype ( int )

#5. removendo espaços pelo comando strip

    df1.loc[: , 'ID'] = df1.loc[ : , 'ID'].str.strip()
    
    df1.loc[: , 'Weatherconditions'] = df1.loc[ : , 'Weatherconditions'].str.strip()
    
    df1.loc[: , 'Road_traffic_density'] = df1.loc[ :, 'Road_traffic_density'].str.strip()
    
    df1.loc[: , 'Type_of_order'] = df1.loc[ : , 'Type_of_order'].str.strip()
    
    df1.loc[: , 'Type_of_vehicle'] = df1.loc[ : , 'Type_of_vehicle'].str.strip()
    
    df1.loc[: , 'Festival'] = df1.loc[ : , 'Festival'].str.strip()

#6. Limpando a coluna de time taken

    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply (lambda  x: x.split ( '(min) ' )[1])
    
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype ( int )

    return df1

#Import dataset

df = pd.read_csv('dataset/train.csv')

#Cleaning dataset
df1 = clean_code(df) 


#================================================================

#Barra Lateral

#================================================================
st.header('Marketplace - Visão Entregadores')

image_path = 'logo.jpg' # carregando imagem para dentro da pagina.
image = Image.open( image_path)
st.sidebar.image ( image, width=120)

st.sidebar.markdown ('# Cury Company') # Criando uma side bar do lado, um botão que retrai e expande a barra.

st.sidebar.markdown ('## Fastest Delivery in Town')

st.sidebar.markdown ("""---""") # cria uma linha para separar um item do outro.

st.sidebar.markdown ('## Selecione uma data limite')

date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=datetime( 2022 , 4, 13),
    min_value=datetime( 2022, 2, 11),
    max_value=datetime( 2022, 4, 6),
    format= 'DD-MM-YYYY')
st.sidebar.markdown ("""---""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default = ['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown ("""---""")
st.sidebar.markdown ('### Powered by Comunidade DS')

# Filtro de Data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de transito

linhas_selecionadas = df1 ['Road_traffic_density'].isin ( traffic_options )
df1 = df1.loc[linhas_selecionadas, :] #ISIN = passa uma lista e verifica se o número que passou esta dentro da lista, no caso o tráfico options.


#================================================================

#LAYOUT NO STREAMLIT

#================================================================


tab1, tab2, tab3 = st.tabs ( ['Visão Gerencial', '_', '_'])


with tab1:
    with st.container():
        st.title ( 'Overall Metrics' )

        col1, col2, col3, col4 = st.columns ( 4 , gap = 'large') # procurar o que essa linhda de comando faz
        with col1:
            # A maior idade dos Entregadores
            maior_idade =  df1.loc[: , 'Delivery_person_Age'].max()
            col1.metric ( ' Maior de idade', maior_idade ) #essa linha serve para exibir

        with col2:
            # A menor idade dos Entregadores
            menor_idade = df1.loc[: , 'Delivery_person_Age'].min()
            col2.metric ( 'Menor de idade' , menor_idade)
            
        with col3:
            melhor_condicao = df1.loc[: , 'Vehicle_condition'].max()
            col3.metric ( 'Melhor condicao' , melhor_condicao)

        with col4:
            pior_condicao = df1.loc[: , 'Vehicle_condition'].min()
            col4.metric ( 'pior condicao' , pior_condicao)

    with st.container():
        st.markdown ("""---""")
        st.title( 'Avaliacoes' )

        col1 , col2 = st.columns (2) #criando duas colunas
        with col1:
            st.markdown('##### Avaliacao medias por entregador')
            df_avg_ratings_per_deliver = (df1.loc[: , ['Delivery_person_Ratings','Delivery_person_ID']]
                                             .groupby('Delivery_person_ID')
                                             .mean()
                                             .reset_index())
            st.dataframe( df_avg_ratings_per_deliver) #Exibir o dataframe

        with col2:
            st.markdown('##### Avaliacao medias por transito')
            df_avg_std_ratings_by_traffic = (df1.loc[: , ['Delivery_person_Ratings', 'Road_traffic_density']]
                                             .groupby('Road_traffic_density')
                                             .agg({'Delivery_person_Ratings': ['mean', 'std']} ) )
            #mudanca de nome das colunas
            df_avg_std_ratings_by_traffic.columns = ['delivery_mean', 'delivery_std']

            #reset do index
            df_avg_std_ratings_by_traffic=df_avg_std_ratings_by_traffic.reset_index()
            
            st.dataframe (df_avg_std_ratings_by_traffic)

            st.markdown('##### Avaliacao media por clima')
            df_avg_std_ratings_by_Weather = (df1.loc[: , ['Delivery_person_Ratings', 'Weatherconditions']]
                                             .groupby('Weatherconditions')
                                             .agg({'Delivery_person_Ratings': ['mean', 'std']} ) )
            # mudanca de nome das colunas
            df_avg_std_ratings_by_Weather.columns = ['Delivery_mean', 'Delivery_std']
            #reset do index
            df_avg_std_ratings_by_Weather= df_avg_std_ratings_by_Weather.reset_index()
            st.dataframe( df_avg_std_ratings_by_Weather )

    with st.container():
        st.markdown ("""---""")
        st.title( ' Velocidade de Entrega ' )

        col1 , col2 = st.columns (2) #criando duas colunas

        with col1:
            st.subheader('Top entregadores mais Rapidos')
            df3 = top_delivers (df1, top_asc=True)
            st.dataframe (df3)


        with col2:
            st.subheader('Top entregadores mais lentos')
            df3 = top_delivers (df1, top_asc=False)
            st.dataframe (df3)