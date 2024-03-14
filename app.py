import streamlit as st
from pipeline_02 import pipeline

st.title('Processador de Arquivos')

if st.button('Processar'):
    with st.spinner('Processando...'):
        logs = pipeline()
        # Exibe os logs no Streamlit
        for log in logs:
            st.write(log)
