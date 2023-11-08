import streamlit as st
from PIL import Image
import emoji

st.set_page_config(
    page_title="Home",
    page_icon="🎲"
)

image_path = 'logo.jpg' # carregando imagem para dentro da pagina.
image = Image.open( image_path)
st.sidebar.image ( image, width=120)


st.sidebar.markdown ('## Cury Company') 

st.sidebar.markdown ('## Fastest Delivery in Town')

st.sidebar.markdown ("""---""")

st.write( "#Curry Company Growt Dashboard" )

st.markdown(
    """
    Growth dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Entregador:
        -Acompanhamento dos indicadores semanais de crescimento
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes

    ### Ask for help
    - Time de Data Science no Discord
        - @Mugica
""" )
    


