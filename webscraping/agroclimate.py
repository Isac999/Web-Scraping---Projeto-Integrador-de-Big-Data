import requests
from bs4 import BeautifulSoup
import mysql.connector

# Clima-Tempo nesse exato momento
url01 = "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/519/pompeia-sp"
response01 = requests.get(url01)
# informações de agora
if response01:
    soup01 = BeautifulSoup(response01.content, 'html.parser') 
    dados_agora = {}
    # temperatura atual
    temperatura_agora = soup01.find('span', class_='-bold -gray-dark-2 -font-55 _margin-l-20 _center').text.strip('\n')
    temperatura_agora = temperatura_agora.replace('º','°')
    dados_agora['Temperatura_Agora'] = temperatura_agora
    # sensação atual
    path01_sensacao_agora = soup01.find('div', class_='no-gutters -gray _flex _justify-center _margin-t-20 _padding-b-20 _border-b-light-1')
    sensacao_agora = path01_sensacao_agora.find_all('span')[1].text
    # vento atual
    path01_vento_agora = soup01.find('ul', class_='variables-list _border-b-light-1').find_all('li')
    vento_agora = path01_vento_agora[0].text.strip('\n')
    # umidade atual
    umidade_agora = path01_vento_agora[1].text.strip('\n')
    # removendo caracteres indesejados da string (formatação)
    remover_caracteres = '\nSensação -VentoUmidadeE'
    for item in remover_caracteres:
        if item in sensacao_agora:
            sensacao_agora = sensacao_agora.replace(item,'')
    for item in remover_caracteres:
        if item in vento_agora:
            vento_agora = vento_agora.replace(item,'')
    for item in remover_caracteres:
        if item in umidade_agora:
            umidade_agora = umidade_agora.replace(item,'')
    # adicionando caracteres formatados ao dict
    dados_agora['Sensação_Agora'] = sensacao_agora
    dados_agora['Vento_Agora'] = vento_agora
    dados_agora['Umidade_Agora'] = umidade_agora
    # printando resultados
    print('---------------------------------------')
    print('----INFORMAÇÕES CLIMÁTICAS DE AGORA----')
    for key,values in dados_agora.items():
        print(f'{key} = {values}')
else:
    print('Algo deu errado! (ESTRUTURA 01)')
# previsão do Clima-Tempo para hoje
url02 = "https://www.climatempo.com.br/previsao-do-tempo/cidade/519/pompeia-sp"
response02 = requests.get(url02)
if response02:
    soup02 = BeautifulSoup(response02.content, 'html.parser')
    dados_hoje = {}
    # dia atual (formatado)
    dia_hoje = soup02.find('h1', class_='-bold -font-18 -dark-blue _margin-r-10 _margin-b-sm-5').text.strip(' ')
    excluir_caracteres07 = 'Previsão de Hoje Pompéia - SP\n'
    for item in excluir_caracteres07:
        if item in dia_hoje:
            dia_hoje = dia_hoje.replace(item,'')
    dados_hoje['Dia_Hoje'] = dia_hoje
    ordered_list = soup02.find('ul', class_='variables-list').find_all('li', class_='item')
    # temperatura mínima (formatado)
    minima_e_maxima = ordered_list[0].text.split('°')
    minima_hoje = minima_e_maxima[0].strip('\n')
    excluir_caracteres05 = 'Temperatura\n'
    for item in excluir_caracteres05:
        if item in minima_hoje:
            minima_hoje = minima_hoje.replace(item, '')
    minima_hoje = minima_hoje + '°'
    dados_hoje['Temperatura_Mínima'] = minima_hoje
    # temperatura máxima (farmatado)
    maxima_hoje = minima_e_maxima[1].strip('\n')
    maxima_hoje = maxima_hoje + '°'
    dados_hoje['Temperatura_Máxima'] = maxima_hoje
    # previsão de chuva em milímetros e porcentagem (formatado)
    chuva_hoje = ordered_list[1].text.strip('\n')
    excluir_caracteres04 = 'Chuva\n'
    for item in excluir_caracteres04:
        if item in chuva_hoje:
            chuva_hoje = chuva_hoje.replace(item, '')
    dados_hoje['Chuva_Hoje'] = chuva_hoje
    # estimativa da velocidade do vento (formatado)
    vento_hoje = ordered_list[2].text.strip('\n')
    excluir_caracteres06 = '\nVentoN'
    for item in excluir_caracteres06:
        if item in vento_hoje:
            vento_hoje = vento_hoje.replace(item,'')
    dados_hoje['Vento_Hoje'] = vento_hoje
    # umidade do ar mínima (formatado)
    umidade_hoje = ordered_list[3].text.strip('\n')
    excluir_caracteres01 = 'Umidade\n'
    for item in excluir_caracteres01:
        if item in umidade_hoje:
            umidade_hoje = umidade_hoje.replace(item, ' ')
    umidade_list = umidade_hoje.split(' ')
    minima_hoje = umidade_list[11]
    dados_hoje['Umidade_Mínima'] = minima_hoje
    # umidade máxima (formatado)
    maxima_hoje = umidade_list[13]
    dados_hoje['Umidade_Máxima'] = maxima_hoje
    # horário do nascimento do sol (formatado)
    nasce_some = ordered_list[4].text.strip('\n')
    excluir_caracteres02 = 'Sol\n '
    for item in excluir_caracteres02:
        if item in nasce_some:
            nasce_some = nasce_some.replace(item,' ')
    nasce_some_list = nasce_some.split(' ')
    nasce_hoje = nasce_some_list[5]
    dados_hoje['Nascimento_Sol'] = nasce_hoje
    # horário em que o sol se põe (formatado)
    some_hoje = nasce_some_list[7]
    dados_hoje['Pôr_do_Sol'] = some_hoje
    print('---------------------------------------')
    print('------PREVISÃO CLIMÁTICA DE HOJE-------')
    for key,values in dados_hoje.items():
        print(f'{key} = {values}')
else: 
    print('Algo deu errado! (ESTRUTURA 02)')
# Clima-Tempo nos próximos 15 dias (semana)
url03 = "https://www.climatempo.com.br/previsao-do-tempo/15-dias/cidade/519/pompeia-sp"
response03 = requests.get(url03)
if response03:
    soup03 = BeautifulSoup(response03.content, 'html.parser')
    dados_semana_dict = {}
    dados_semana = []
    dias_semana = []
    # encontrando temperaturas mínimas, máximas e probabilidade de chuva nos próximos 15 dias
    lista_semana = soup03.find_all('div', class_='_flex _padding-l-sm-10')
    # formatando strings e adicionando a uma lista
    excluir_caracteres08 = '\n'
    for value in lista_semana:
        for item in excluir_caracteres08:
            if item in value.text:
                result01 = value.text
                result01 = result01.replace(item,'')
                dados_semana.append(result01)
            else: 
                result01 = value.text
                dados_semana.append(result01)
    # buscando os dias da semana e adicionando a uma lista
    respectivos_dias = soup03.find_all('div', class_='date-inside-circle')
    for value in respectivos_dias:
        for item in excluir_caracteres08:
            if item in value.text:
                result02 = value.text
                result02 = result02.replace(item,'')
                dias_semana.append(result02)
            else:
                result02 = value.text
                dias_semana.append(result02)
    # criando dict de dias da semana (keys) e respectivas previsões (values)
    cont = 0
    for item in dias_semana:
        dados_semana_dict[item] = dados_semana[cont]
        cont = cont + 1 
    # printando resultados
    print('---------------------------------------')
    print('--PREVISÃO CLIMÁTICA PRÓXIMOS 15 DIAS--')
    for key,values in dados_semana_dict.items():
        print(f'{key} = {values}')
else:
    print('Algo deu errado! (ESTRUTURA 03)')
#conectando ao Banco de dados
try:
    db = mysql.connector.connect(
        host = "opmy0013.servidorwebfacil.com",
        user = "desqu_agrocota",
        password = " ",
        database = "desquinela_sqlserver"
    )
except Exception as erro:
    print(f'Erro na conexão com Banco de Dados -> {erro.__cause__}')
    db.close()
#inserindo dados nas tabelas
else:
    cursor = db.cursor()
    #limpando dados desatualizados
    truncate_agora = "TRUNCATE TABLE agora"
    truncate_hoje = "TRUNCATE TABLE hoje"
    truncate_semana = "TRUNCATE TABLE semana"
    cursor.execute(truncate_agora), cursor.execute(truncate_hoje), cursor.execute(truncate_semana)
    db.commit()
    #informações climáticas de agora
    insert =  "INSERT INTO agora (temperatura, sensacao, vento, umidade) VALUES (%s, %s, %s, %s)"
    values = (dados_agora['Temperatura_Agora'], dados_agora['Sensação_Agora'], dados_agora['Vento_Agora'], dados_agora['Umidade_Agora'])
    cursor.execute(insert, values)
    db.commit()
    #informações climáticas de hoje
    insert = """INSERT INTO hoje (data, temperaturaminima, temperaturamaxima, probabilidade, estimativa, umidademinima, umidademaxima, nascesol , poesol)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (dados_hoje['Dia_Hoje'], 
    dados_hoje['Temperatura_Mínima'], 
    dados_hoje['Temperatura_Máxima'], 
    dados_hoje['Chuva_Hoje'], 
    dados_hoje['Vento_Hoje'], 
    dados_hoje['Umidade_Mínima'], 
    dados_hoje['Umidade_Máxima'], 
    dados_hoje['Nascimento_Sol'], 
    dados_hoje['Pôr_do_Sol'])
    cursor.execute(insert, values)
    db.commit()
    #informações climáticas da semana e quinzena
    for item in dados_semana_dict:	
        insert = "INSERT INTO semana (semana, valor) VALUES (%s, %s)"
        values = (item, dados_semana_dict[item])
        cursor.execute(insert, values)
        db.commit()
    db.close()