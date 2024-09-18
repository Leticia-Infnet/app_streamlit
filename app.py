import streamlit as st
import pandas as pd
import time
import plotly.express as px


@st.cache_data
def csv_to_dataframe(csv_file):
    '''
    Transforma um arquivo csv em um dataframe 

    Args:
    Caminho do arquivo csv
    '''
    df = pd.read_csv(csv_file, delimiter=';')
    return df


def color_picker():
    '''
    Função para escolher a cor de fundo do app
    '''

    background_color = st.selectbox('Escolha uma cor de fundo', ['Hunyadi yellow',
                                                                 'Linen',
                                                                 'Tea rose (red)',
                                                                 'Cambridge blue',
                                                                 'Light coral'])
    colormap = {
        'Hunyadi yellow': '#F6BD60',
        'Linen': '#F7EDE2',
        'Tea rose (red)': '#F5CAC3',
        'Cambridge blue': '#84A59D',
        'Light coral': '#F28482'
    }

    st.markdown(f'''
        <style>
        .stApp {{
            background-color: {colormap[background_color]};
        }}
        </style>
        ''', unsafe_allow_html=True)


def main():
    '''
    Função principal do app
    '''

    st.title(
        'Número de visitantes por mês em trilhas no Parque Nacional da Tijuca :deciduous_tree:')

    st.subheader(
        'Análise do número de visitantes em trilhas, podendo serem utilizados os datasets dos anos de 2018 e 2019')

    # Upload de arquivos csv
    st.header('Upload :open_file_folder:')
    st.write('Faça upload do arquivo .csv')
    csv_file = st.file_uploader('Upload arquivo .csv', type=['csv'])

    # Verifica se o arquivo CSV foi carregado e ainda não está no session state
    if csv_file and 'df' not in st.session_state:
        # Mostra o spinner apenas quando o dataframe está sendo processado inicialmente
        with st.spinner('Carregando dados...'):
            df = csv_to_dataframe(csv_file)
            df.set_index('Mês', inplace=True)
            time.sleep(5)
            st.session_state['df'] = df  # Guarda do dataframe em session state

    # Se o dataframe já existe em session state:
    if 'df' in st.session_state:
        df = st.session_state['df']

        # Mostrando o Dataframe
        if st.button('Mostrar Dataframe'):
            st.dataframe(df)

        # Mostrando resumo dos dados
        st.header('Resumo Dados :clipboard:')
        if st.button('Mostrar resumo dos dados do DataFrame'):
            st.dataframe(df.describe())

        # Fazendo filtragem dos dados
        st.header('Filtrando Dados :pushpin:')
        selected_columns = st.multiselect(
            'Selecione as trilhas para exibir', df.columns)

        # Filtrando por linha (usando 'Mês')
        selected_rows = st.multiselect(
            'Selecione os meses para exibir', df.index)

        # Lógica do filtro:
        if selected_columns and selected_rows:
            # Filtrar por coluna e linha
            filtered_df = df.loc[selected_rows, selected_columns]
        elif selected_columns:
            # Filtrar por coluna
            filtered_df = df[selected_columns]
        elif selected_rows:
            # Filtrar por linha
            filtered_df = df.loc[selected_rows]
        else:
            # Se não houve filtros, mostrar o dataframe inteiro
            filtered_df = df

        st.dataframe(filtered_df)

        # Fazendo download dos dados filtrados
        csv = filtered_df.to_csv()
        st.download_button(label='Baixar dados',
                           data=csv,
                           file_name='filtered_data.csv',
                           mime='text/csv')

        # Fazendo um gráfico de pizza

        st.header('Gráfico de pizza')
        pie_data = df.sum()
        fig = px.pie(values=pie_data, names=pie_data.index,
                     title='Distribuição dos Visitantes por Trilha')

        st.plotly_chart(fig)

        # Fazendo um heatmap
        st.header('Heatmap')
        fig_heatmap = px.imshow(df,
                                labels=dict(x='Trilha',
                                            y='Mês',
                                            color='Visitantes'),
                                title='Heatmap de Visitantes por Trilha e Mês')

        st.plotly_chart(fig_heatmap)

        # Escolhendo a cor de fundo do app

        color_picker()


if __name__ == "__main__":
    main()
