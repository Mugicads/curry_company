#Libraries

from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

#bibliotecas necessárias 
import folium
import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config( page_title='Visão Restaurantes', page_icon='🍴', layout= 'wide' )

# -------------------------------------------
# Funções
# -------------------------------------------
def avg_std_time_on_traffic ( df1):
    df_aux = (df1.loc[: , ['City' , 'Time_taken(min)' , 'Road_traffic_density']]
                 .groupby(['City', 'Road_traffic_density'])
                 .agg( { 'Time_taken(min)': ['mean', 'std']}))

    df_aux.columns = ['avg_time' , 'std_time']
    df_aux = df_aux.reset_index()
    fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values = 'avg_time',
                      color= 'std_time', color_continuous_scale='RdBu',
                      color_continuous_midpoint=np.average(df_aux['std_time']))
    return fig

def avg_std_time_graph (df1):
    df_aux = df1.loc[: , ['City' ,'Time_taken(min)']].groupby('City').agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['avg_time' , 'std_time']
    df_aux = df_aux.reset_index()
    fig= go.Figure()
    fig.add_trace (go.Bar( name='Control', x=df_aux['City'], y=df_aux['avg_time'], error_y=dict(type='data', array=df_aux['std_time'])))
    fig.update_layout(barmode='group')

    return fig

def avg_std_time_delivery(df1, Festival, op):
    """ 
        Esta função calcula o tempo médio e o desvio padrão do tempo de entrega.
             Parâmetros:
             Input:
              - df: Dataframe com os dados necessários para o cálculo
              - op: Tipo de operação que precisa ser calculado
                'avg_time': Calcula o tempo médio
                'std_time': Calcula o desvio padrão do tempo
            Output:
                - df: Dataframe com 2 colunas e 1 linha.
                         
                 
    """
    df_aux = (df1.loc[: , ['Time_taken(min)' , 'Festival']]
                 .groupby('Festival')
                 .agg( {'Time_taken(min)': ['mean', 'std' ]} ) )
    
    df_aux.columns = ['avg_time' , 'std_time']   
    df_aux = df_aux.reset_index() 
    df_aux =np.round(df_aux.loc[df_aux['Festival'] == Festival, op], 2 )

    return df_aux

def distance (df1,fig):
    if fig ==False:
        cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
        df1['distance'] = df1.loc[0:10 , cols].apply( lambda x:
                                        haversine(  (x ['Restaurant_latitude'], x['Restaurant_longitude']),
                                                    (x['Delivery_location_latitude'], x['Delivery_location_longitude'] ) ), axis=1 )
        
        avg_distance = np.round(df1['distance'].mean(), 2)
        return avg_distance
    else:
        cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
        df1['distance'] = df1.loc[0:10 , cols].apply( lambda x:
                                        haversine(  (x ['Restaurant_latitude'], x['Restaurant_longitude']),
                                                    (x['Delivery_location_latitude'], x['Delivery_location_longitude'] ) ), axis=1 )
        
            
        avg_distance = df1.loc[:, ['City', 'distance']].groupby ('City').mean().reset_index() #Calcula a média
        fig = go.Figure(data =[go.Pie( labels= avg_distance['City'], values=avg_distance['distance'], pull=[0, 0.1, 0])]) #Printa o gráfico
            
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

    df1.loc[: , 'Festival'] = df1.loc[ : , 'Festival'].str.strip()

    df1.loc[: , 'City'] = df1.loc[ : , 'City'].str.strip()
    
    #6. Limpando a coluna de time taken
    
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply (lambda  x: x.split ( '(min) ' )[1])
    
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype ( int )

    return df1

#-----------------------------------
#Import dataset
#-----------------------------------
df = pd.read_csv('dataset/train.csv')

#cleaning Code
df1 = clean_code (df)

#================================================================
#Barra Lateral
#================================================================
st.header('Marketplace - Visão Restaurantes')

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
        st.title('Overal Metrics')

        col1, col2, col3, col4, col5, col6 = st.columns (6)
        with col1:
            delivery_unique = len( df1.loc[: , 'Delivery_person_ID'].unique() )
            col1.metric('Entregadores únicos',  delivery_unique )

        with col2:
            avg_distance = distance (df1, fig=False)
            col2.metric('A distancia media das entregas', avg_distance)

        with col3:
            df_aux = avg_std_time_delivery (df1, 'Yes', 'avg_time')    
            col3.metric('tempo médio de entrega com Festival', df_aux)

        with col4:
            df_aux = avg_std_time_delivery (df1, 'Yes', 'std_time')
            col4.metric('desvio padrão médio de entrega com Festival ', df_aux)

        with col5:
            df_aux = avg_std_time_delivery (df1, 'No', 'avg_time')
            col5.metric('Tempo Médio' , df_aux)

        with col6:
            df_aux = avg_std_time_delivery (df1, 'No', 'std_time')
            col6.metric('STD Entrega', df_aux)

    with st.container():
        st.markdown ("""---""")
        col1,col2 = st.columns (2)
        
        with col1:
            fig= avg_std_time_graph (df1)        
            st.plotly_chart ( fig )

        with col2:
            cols = ['City' , 'Time_taken(min)' , 'Type_of_order']
    
            df_aux = (df1.loc[: , ['City' , 'Time_taken(min)' , 'Type_of_order']]
                         .groupby(['City', 'Type_of_order'])
                         .agg( {'Time_taken(min)': ['mean', 'std']}))
    
            df_aux.columns = ['avg_time' , 'std_time']
            df_aux = df_aux.reset_index()
            
            st.dataframe (df_aux)
            
    with st.container():
        st.markdown ("""---""")
        st.title('Distribuição do Tempo')

        col1, col2= st.columns ( 2 )
        with col1:           
            fig = distance (df1, fig=True)
            st.plotly_chart ( fig )

        with col2:   
            fig = avg_std_time_on_traffic (df1)   
            st.plotly_chart (fig)        

      