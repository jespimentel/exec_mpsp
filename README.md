# Execução orçamentária do MPSP em tempo real
### José Eduardo de Souza Pimentel (criado em: 20 abr. 2024)

## Visão geral
O programa utiliza Python e Streamlit, principalmente, para criar uma interface web interativa para visualização de dados em tempo real da execução orçamentária do Ministério Público de São Paulo (MPSP).
Os dados são obtidos das APIs da Secretaria da Fazenda do Estado de São Paulo.

## Estratégias da aplicação

### Streamlit:
- Criação de Interface de Usuário: o Streamlit é responsável pela interface web interativa. Ele oferece uma maneira simples e eficaz de desenvolver aplicativos web com Python.
- Componentes Interativos: o programa utiliza componentes do Streamlit, como st.title, st.subheader, st.sidebar, st.button e st.columns.

### xmltodict:
- Parsing de XML: a biblioteca xmltodict é usada para analisar e converter as respostas XML das requisições SOAP em um dicionário Python, facilitando o trabalho de conversão dos dados retornados pela API da SEFAZ em dataframes.

### Plotly Express:
- Visualizações Gráficas Interativas: o Plotly Express é utilizado para criar visualizações gráficas interativas, como gráficos de pizza e de barras. Ele oferece uma interface simples para criar gráficos com boa qualidade estética e interatividade.

### Pandas:
- Manipulação de Dados Tabulares: o Pandas é fundamental para manipular os dados retornados pelas consultas à API, após sua conversão em dicionário (com xmltodict). Ele é usado para criar DataFrames, realizar operações de filtragem, agregação e transformação de dados.
- Limpeza e Transformação de Dados: o programa utiliza funcionalidades do Pandas, como applymap, merge e manipulação de índices, para limpar e transformar os dados, garantindo que estejam prontos para as plotagens.

### Referências
- SEFAZ (web services): https://portal.fazenda.sp.gov.br/acessoinformacao/Paginas/Web-Services.aspx
- Streamlit: criando aplicações web (live do Eduardo “Dunossauro” Mendes): https://www.youtube.com/live/Ie5ef_R_k6I?si=j_1R4BZJ3mVhZqcN
- Streamlit: https://streamlit.io/
- Plotly: https://plotly.com/python/




