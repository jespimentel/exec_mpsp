# Importações e configuração inicial
import streamlit as st
import plotly.express as px
import requests
import xmltodict
import warnings
import pandas as pd
import datetime
import locale

#locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

warnings.filterwarnings("ignore")
pd.set_option('display.float_format', lambda x: '%.2f' % x) # Exibição de duas casas decimais

# Funções
@st.cache_data
def consulta_despesas(orgao, ano):
  url = "https://webservices.fazenda.sp.gov.br/WSTransparencia/TransparenciaServico.asmx?op=ConsultarDespesas"
  headers = {'Content-Type': 'text/xml'}

  # Define o corpo da requisição SOAP
  body = """<?xml version=\"1.0\" encoding=\"utf-8\"?>\n
        <soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\n
        <soap:Body>\n
        <ConsultarDespesas xmlns=\"http://fazenda.sp.gov.br/wstransparencia\">\n
        <ano>ANO</ano>\n
        <codigoOrgao>CODIGO_ORGAO</codigoOrgao>\n
        <codigoFonteRecursos>Detalhado</codigoFonteRecursos>\n
        <flagCredor>1</flagCredor>\n
        <flagEmpenhado>1</flagEmpenhado>\n
        <flagLiquidado>1</flagLiquidado>\n
        <flagPago>1</flagPago>\n
        </ConsultarDespesas>\n
        </soap:Body>\n
        </soap:Envelope>"""
  
  # Substitui os placeholders (SEU_USUARIO, SUA_SENHA, ANO, etc.) pelos valores reais
  body = body.replace("ANO", str(ano))  # Exemplo com o ano atual
  body = body.replace("CODIGO_ORGAO", str(orgao))

  # Envia a requisição POST
  response = requests.post(url, headers=headers, data=body, verify=False)

  # Verifica o status da requisição
  if response.status_code == 200:
      print(f"Requisição para ano {ano}: Cód. {response.status_code}")
  else:
      print(f"Erro na requisição para o ano {ano}: {response.status_code}")

  return response.content

@st.cache_data
def consulta_despesas_dotacao(orgao, ano):
  url = "https://webservices.fazenda.sp.gov.br/WSTransparencia/TransparenciaServico.asmx?op=ConsultarDespesasDotacao"
  headers = {'Content-Type': 'text/xml'}

  # Define o corpo da requisição SOAP
  body = """<?xml version=\"1.0\" encoding=\"utf-8\"?>\n
        <soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\n
        <soap:Body>\n
        <ConsultarDespesasDotacao xmlns="http://fazenda.sp.gov.br/wstransparencia">\n
        <ano>ANO</ano>\n
        <codigoOrgao>CODIGO_ORGAO</codigoOrgao>\n
        <CodigoNomeFonteRecursos>Detalhado</CodigoNomeFonteRecursos>\n
        <flagCredor>1</flagCredor>\n
        <flagDotacaoInicial>1</flagDotacaoInicial>\n
        <flagDotacaoAtual>1</flagDotacaoAtual>\n
        <flagEmpenhado>1</flagEmpenhado>\n
        <flagLiquidado>1</flagLiquidado>\n
        <flagPago>1</flagPago>\n
        </ConsultarDespesasDotacao>\n
        </soap:Body>\n
        </soap:Envelope>"""
  
  # Substitui os placeholders (SEU_USUARIO, SUA_SENHA, ANO, etc.) pelos valores reais
  body = body.replace("ANO", str(ano))
  body = body.replace("CODIGO_ORGAO", str(orgao))

  # Envia a requisição POST
  response = requests.post(url, headers=headers, data=body, verify=False)

  # Verifica o status da requisição
  if response.status_code == 200:
      print(f"Requisição para ano {ano}: Cód. {response.status_code}")
  else:
      print(f"Erro na requisição para o ano {ano}: {response.status_code}")

  return response.content

def converte (str_numero):
  """Converte a valores monetários em float"""
  try:
      str_numero = str_numero.replace('.', '').replace(',','.')
      float_numero = float(str_numero)
      return float_numero
  except:
      return str_numero

def quanto_ja_passou_do_ano(data_atual, ano):

    # Verifica se o ano atual é bissexto
    if ano % 4 == 0:
      total_dias_no_ano = 366
    else:
      total_dias_no_ano = 365
    
    dias_passados = (data_atual - datetime.datetime(ano, 1, 1)).days + 1   
    return dias_passados, total_dias_no_ano

def main():
    orgao = '27000'
    data_atual = datetime.datetime.now()
    ano = data_atual.year
    st.title("Execução orçamentária do MPSP")
    st.subheader('Pimentel - 2024')
    st.text(f"Data/hora atual: {data_atual}")

    despesas = consulta_despesas(orgao, str(ano))
    dados_despesas = xmltodict.parse(despesas)
    despesas = dados_despesas['soap:Envelope']['soap:Body']['ConsultarDespesasResponse']['ConsultarDespesasResult']['ListaItensDespesa']['ItemDespesa']

    dotacao = consulta_despesas_dotacao(orgao, str(ano))
    dados_dotacao = xmltodict.parse(dotacao)
    dotacao = dados_dotacao['soap:Envelope']['soap:Body']['ConsultarDespesasDotacaoResponse']['ConsultarDespesasDotacaoResult']['ListaItensDespesa']['ItemDespesa']

    # Dataframes
    df_despesas = pd.DataFrame(despesas)
    df_dotacao = pd.DataFrame(dotacao)

    # Deleta a linha de totalização
    df_despesas = df_despesas.drop(df_despesas.index[-1])

    # Conversão dos valores monetários em float
    df_despesas = df_despesas.applymap(converte)
    df_dotacao = df_dotacao.applymap(converte)

    # Criação do campo comum
    df_despesas['CodigoElemento'] = df_despesas['NaturezaDespesaNomeItem'].str.split(' ').str[0].str[:6]
    df_dotacao['CodigoElemento'] = df_dotacao['CodigoNomeElemento'].str.split(' ').str[0]

    # Colunas de interesse
    df_despesas = df_despesas[['CodigoElemento', 'CodigoNomeFonteRecursos','CodigoNomeTipoLicitacao', 'CgcCpfFavorecido', 
                            'NaturezaDespesaNomeItem', 'ValorEmpenhado','ValorLiquidado', 'ValorPago', 
                            'ValorPagoAnosAnteriores']]

    df_dotacao = df_dotacao[['CodigoElemento', 'CodigoNomeElemento', 'ValorDotacaoInicial', 'ValorDotacaoAtual', 
                            'ValorEmpenhado', 'ValorLiquidado', 'ValorPago', 'ValorPagoAnosAnteriores']]

    dotacao_inicial_total = df_dotacao.iloc[-1]['ValorDotacaoInicial']
    dotacao_atual = df_dotacao.iloc[-1]['ValorDotacaoAtual']

    df_dotacao['Pago total'] = df_dotacao['ValorPago'] + df_dotacao['ValorPagoAnosAnteriores']
    df_dotacao['% do Total Dot. Inic.'] = df_dotacao['Pago total']/dotacao_inicial_total * 100
    df_dotacao['% da Dot. Inicial (Elemento)'] = df_dotacao['Pago total']/df_dotacao['ValorDotacaoInicial'] * 100
    df_dotacao['% da Dot. Atual'] = df_dotacao['Pago total']/dotacao_atual * 100
    df_dotacao['% da Dot. Atual (Elemento)'] = df_dotacao['Pago total']/df_dotacao['ValorDotacaoAtual'] * 100

    pago_total = df_dotacao.iloc[-1]['Pago total']

    # Filtra o dataframe
    elemento = st.sidebar.selectbox("Elemento", df_dotacao['CodigoNomeElemento'].unique(), index=len(df_dotacao) - 1)
    df_dotacao_filtrado = df_dotacao[df_dotacao['CodigoNomeElemento'] == elemento]

    # Filtra o dataframe de despesas 
    df_despesas_filtrado = pd.merge(df_dotacao_filtrado, df_despesas, on='CodigoElemento', how='inner')

    # Adiciona coluna
    df_despesas_filtrado['Pg Total'] = df_despesas_filtrado['ValorPago_y'] + df_despesas_filtrado['ValorPagoAnosAnteriores_y']

    # Cria as colunas do dashboard
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5 = st.empty() # Não cria o container

    # Gráfico pizza - Quanto do ano já passou
    valores = quanto_ja_passou_do_ano(data_atual, ano) 
    categorias = ['Já passou', 'Ainda faltam']
    fig_1 = px.pie(values=valores, names=categorias, title='Quanto do ano já passou')
    col1.plotly_chart(fig_1, use_container_width=True)

    # Gráfico pizza - Quanto do orçamento atual já foi pago
    valores = [pago_total, dotacao_atual] 
    categorias = ['Pago total', 'Dotação atual']
    fig_2 = px.pie(values=valores, names=categorias, title='Quanto já foi executado (pago)')
    col2.plotly_chart(fig_2,use_container_width=True)

    # Gráfico de barras - com valores filtrados
    dot_ini = df_dotacao_filtrado['ValorDotacaoInicial'].iloc[0]
    dot_atual = df_dotacao_filtrado['ValorDotacaoAtual'].iloc[0]
    pg_total = df_dotacao_filtrado['Pago total'].iloc[0]
    print(dot_ini)
    grupos = ['Dotação inicial', 'Dotação atual', 'Pago + Anos anteriores']
    valores = [dot_ini, dot_atual, pg_total]
    fig_3 = px.bar(x=grupos, y=valores, title='Valores relativos ao elemento')
    col3.plotly_chart(fig_3, use_container_width=True)

    # Gráfico pizza - Quanto já foi pago (elemento selecionado)
    valores = [dot_atual-pg_total, pg_total]
    categorias = ['Sobra da dotação atual', 'Pagamento total']
    fig_4 = px.pie(values=valores, names=categorias, title='Quanto já foi executado (pago) desse elemento')
    col4.plotly_chart(fig_4,use_container_width=True)

    # Gráfico de barras - Exibe os beneficiários
    fig5 = px.bar(df_despesas_filtrado, x='NaturezaDespesaNomeItem', y='Pg Total', color='CgcCpfFavorecido', barmode='group')
    col5.plotly_chart(fig5, use_container_width=True)

    if st.button('Nova consulta à API'):
       st.experimental_rerun()

    return

if __name__ == "__main__":
    main()