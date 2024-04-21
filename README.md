# Execução orçamentária do MPSP em tempo real
### José Eduardo de Souza Pimentel (criado em: 20 abr. 2024)

## Visão geral
O programa utiliza Python e Streamlit para criar uma interface web interativa para visualização de dados em tempo real da execução orçamentária do Ministério Público de São Paulo (MPSP).
Os dados são obtidos das APIs do SIGEO, da Secretaria da Fazenda do Estado de São Paulo.

## Estratégias da aplicação

### Streamlit:
- Criação de Interface de Usuário: O Streamlit é a peça central para criar uma interface web interativa. Ele oferece uma maneira simples e eficaz de desenvolver aplicativos web com Python.
- Componentes Interativos: O programa utiliza os componentes do Streamlit, como st.title, st.subheader, st.sidebar, st.button e st.columns, para criar uma interface de usuário interativa e responsiva.

### xmltodict:
- Parsing de XML: A biblioteca xmltodict é usada para analisar e converter as respostas XML das requisições SOAP em estruturas de dados Python, facilitando o trabalho com os dados retornados pela API de transparência da Secretaria da Fazenda de São Paulo.

### Plotly Express:
- Visualizações Gráficas Interativas: O Plotly Express é utilizado para criar visualizações gráficas interativas, como gráficos de pizza e de barras. Ele oferece uma interface simples para criar gráficos com boa qualidade estética e interatividade.
- Customização de Gráficos: O programa utiliza recursos do Plotly Express para customizar os gráficos, como títulos, legendas, cores e estilo dos gráficos.

### Pandas:
- Manipulação de Dados Tabulares: O Pandas é fundamental para manipular os dados retornados pelas consultas à API. Ele é usado para criar e manipular DataFrames, realizar operações de filtragem, agregação e transformação de dados.
- Limpeza e Transformação de Dados: O programa utiliza funcionalidades do Pandas, como applymap, merge e manipulação de índices, para limpar e transformar os dados, garantindo que estejam prontos para serem visualizados.



