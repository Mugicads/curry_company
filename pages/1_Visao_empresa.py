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

st.set_page_config( page_title='Visão Empresa', page_icon='📈', layout= 'wide' )

# -------------------------------------------
# Funções
# -------------------------------------------

def country_maps (df1):
        
       
    cols = ['City', 'Road_traffic_density', 'Delivery_location_latitude' , 'Delivery_location_longitude' ]
        
        
    df_aux = (df1.loc[:, cols].groupby(['City', 'Road_traffic_density'] ).median().reset_index())
        
    #Pego a mediana e não a média, a mediana é o próprio número no conjunto de dados.
                
    map = folium.Map() #porem é o mapa vazio, preciso colocar os pontos
                
    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'], 
                       location_info['Delivery_location_longitude']], 
                       popup=location_info[['City', 'Road_traffic_density']]).add_to(map)
    folium_static ( map, width=1024 , height =600 ) #exibir mapa , se não ele não vai funcionar

        

def order_share_by_week (df1):
           
    cols = ['ID' ,'week_of_year']
    df_aux01 = df1.loc[:, cols].groupby(['week_of_year' ] ).count().reset_index()      
    cols01 = ['week_of_year', 'Delivery_person_ID']
    df_aux02 = (df1.loc[:, cols01]
                .groupby(['week_of_year' ] )
                .nunique()
                .reset_index())
            
    #Eu preciso juntar as coisas, é uma coisa nova que não sei, vou juntar dois Dataframes
    #Vamos usar uma biblioteca e o comando HOW, como eu vou juntar duas coisas
            
    df_aux= pd.merge(df_aux01 , df_aux02, how='inner')
            
    #Agora eu posso dividir e criar uma nova coluna que é a Order_by_deliver
            
    df_aux['Order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
            
    #Gráfico
            
    fig = px.line(df_aux, x='week_of_year' , y= 'Order_by_deliver')

    return fig
       

def order_by_week(df1):
            
    #aqui eu preciso calcular a semana, não tenho a coluna que indica o número da semana, preciso fazer isso
            
    #cria a coluna de semana do ano, no caso o número, ai faço o df1['week_of_year']
    #Depois o Df1 vai receber o resultado da operação df1['Order_Date'].dt.strftime( '%U' )
    #Onde dt é para transformar de series em data, strftime formata Order_Data no tempo o %U a semana começa  no Domingo se for %W começa na segunda
            
    df1['week_of_year'] = df1['Order_Date'].dt.strftime( '%U' )
            
    cols = ['ID' ,'week_of_year']
    df_aux = df1.loc[:, cols].groupby(['week_of_year' ] ).count().reset_index()
            
    fig = px.line(df_aux, x= 'week_of_year' , y='ID')

    return fig

def traffic_order_city(df1):
                
    cols = ['ID' ,'City', 'Road_traffic_density' ]
    
    df_aux = (df1.loc[:, cols]
                 .groupby(['City', 'Road_traffic_density'] )
                 .count()
                 .reset_index())          
                
    fig = px.scatter(df_aux, x='City', y= 'Road_traffic_density' , size='ID', color='City') #Size da o tamanho da bolha

    return fig

def traffic_order_share (df1):
                
    #aqui preciso fazer uma manobra para cálcular
    
    cols = ['ID' ,'Road_traffic_density']
                
    df_aux = (df1.loc[:, cols]
                 .groupby(['Road_traffic_density'] )
                 .count()
                 .reset_index())
                
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN' , :]
                
    #Eu quero em %, logo eu crio uma nova coluna dentro do df_aux
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum() #aqui vou somar as colunas e dividir pelas linhas e vai me dar um valor
                
    fig = px.pie(df_aux, values = 'entregas_perc' , names = 'Road_traffic_density') # aqui é o gráfico de pizza com a sua nomenclatura

    return fig

def order_metric (df1):
    #Colunas
    cols = ['ID' , 'Order_Date']
    
    # Selecao de linhas
    df_aux = df1.loc[:, cols].groupby(['Order_Date'] ).count().reset_index() # Reseto o index para transformar o ORDER_DATE em coluna para na criação do gráfico ele ficar direitinho.
        
        
    #desenhar o Gráfico e linhas
    
    fig = px.bar( df_aux , x='Order_Date' , y= 'ID'  ) # -> passo a variável de dados (df_aux), depois as coordenadas dos eixos x e Y, o que vai ficar em cada eixo

    return fig

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
    
    #6. Limpando a coluna de time taken
    
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply (lambda  x: x.split ( '(min) ' )[1])
    
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype ( int )

    return df1

#---------------------------- Inicio da Estrutura lógica do código ------------------------------
#----------------------
#Import dataset
#----------------------
df = pd.read_csv('dataset/train.csv') # Leitura

#--------------------------
#Limpando os Dados
#--------------------------
df1 = clean_code (df) #Limpeza

#================================================================
#Barra Lateral
#================================================================
st.header('Marketplace - Visão Cliente')

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


st.dataframe (df1)

#================================================================

#LAYOUT NO STREAMLIT

#================================================================


#criando abas

tab1, tab2, tab3 = st.tabs ( ['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

#Usando uma cláusula que é uma palavra reservada do Python com identação (with), tudo que estiver dentro da identação de cada with vai ficar ali dentro.

with tab1: #dentro dessa tab
    with st.container():
        # Order Metric
        fig = order_metric (df1) #chamo a função que vai fazer o gráfico
        st.markdown(' Orders by Day') #Titulo
        st.plotly_chart (fig, use_container_width = True) # Função prórpia do streamlit que vai mostrar o gráfico, ele gaurda o fig=px.    
        
        
            #use container é width é para caber dentro da página.
    with st.container():
        #Criando colunas
        col1 , col2 = st.columns ( 2 ) #crio a coluna e guardo dentro de col1 e col2, e depois preciso colocar dentro do with mas antes eu preciso criar um container la no ínicio para isso aqui aparecer.
        with col1:
            fig = traffic_order_share ( df1 ) #Desenho a figura
            st.header ( 'Traffic Order Share') #Desenho o Titulo 
            st.plotly_chart (fig, use_container_width = True) #Coloco o desenho dentro do Container
                            
        with col2:
            fig = traffic_order_city (df1)
            st.header ( 'Traffic Order City')
            st.plotly_chart (fig, use_container_width = True)                         

with tab2:
    with st.container():
        st.markdown ('# Order by Week')
        fig = order_by_week (df1)
        st.plotly_chart (fig, use_container_width = True)
                                        
    with st.container():
         #aqui precisa fazer uma nova função
        
#Quantidade de pedidos por semana / Número único de entregadores por semana , preciso fazer em duas partes
        
        # Primeira parte
        st.markdown ('Order Share by Week')
        fig = order_share_by_week(df1)
        st.plotly_chart (fig, use_container_width = True)

#consigo ver o número de pedidos feito por entregadores. se preciso aumentar o número de entregadores

with tab3:
    st.markdown ('#Country Maps ')
    country_maps (df1)
        
        
       
        
        

















