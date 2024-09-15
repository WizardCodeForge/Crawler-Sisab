from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import os
import time

# Configurar o ChromeDriver usando WebDriver Manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Caminho onde o CSV será salvo
pasta_download = 'caminho/para/pasta/downloads'
os.makedirs(pasta_download, exist_ok=True)

try:
    # Abra o site
    driver.get('https://sisab.saude.gov.br/paginas/acessoRestrito/relatorio/federal/indicadores/indicadorCadastro.xhtml')

    # Imprimir o HTML da página para depuração
    print(driver.page_source)

    # Aguarde e selecione a caixa "Nível de visualização"
    try:
        nivel_visualizacao = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#selectLinha'))
        )
        select_nivel_visualizacao = Select(nivel_visualizacao)
        select_nivel_visualizacao.select_by_value('ibge')  # Seleciona a opção com o valor 'ibge'
    except Exception as e:
        print("Erro ao selecionar 'Nível de visualização':", e)

    # Aguarde e selecione a caixa "Condição das Equipes"
    try:
        condicao_equipes = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#opacao-capitacao'))
        )
        select_condicao_equipes = Select(condicao_equipes)
        select_condicao_equipes.select_by_value('|HM|')  # Seleciona a opção com o valor '|HM|'
    except Exception as e:
        print("Erro ao selecionar 'Condição das Equipes':", e)

    # Aguarde e selecione a caixa "Competência"
    try:
        competencia_select = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#competencia'))
        )
        # Obter todas as opções
        options = competencia_select.find_elements(By.TAG_NAME, 'option')

        if options:
            # Encontrar a opção com o maior valor
            max_value_option = max(options, key=lambda opt: int(opt.get_attribute('value')) if opt.get_attribute('value').isdigit() else -1)
            max_value = max_value_option.get_attribute('value')
            max_value_text = max_value_option.text

            # Selecionar a opção encontrada usando JavaScript
            driver.execute_script("arguments[0].selected = true;", max_value_option)
            driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", max_value_option)
            print(f"Selecionado valor: {max_value}")

            # Encontrar e clicar no botão correspondente ao valor selecionado
            try:
                # Esperar que o botão correspondente esteja presente e visível
                button = WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.XPATH, f"//button[@title='{max_value_text}']"))
                )
                button.click()
                print(f"Botão selecionado: {max_value_text}")
            except Exception as e:
                print("Erro ao selecionar o botão correspondente:", e)
        else:
            print("Nenhuma opção encontrada no seletor 'Competência'")
    except Exception as e:
        print("Erro ao selecionar 'Competência':", e)

    # Clique no botão de download
    try:
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#componente-download'))
        ).click()
    except Exception as e:
        print("Erro ao clicar no botão de download:", e)

    # Selecione a opção CSV no menu suspenso
    try:
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[title="CSV"]'))  # Ajuste conforme necessário
        ).click()
    except Exception as e:
        print("Erro ao selecionar o formato CSV:", e)

    # Aguarde o download do CSV (ajuste o tempo de espera conforme necessário)
    time.sleep(300)  # Ajuste o tempo de espera conforme necessário

    # Nome do arquivo CSV (ajuste conforme necessário)
    nome_arquivo_csv = 'relatorio.csv'  # Atualize se necessário
    caminho_csv = os.path.join(pasta_download, nome_arquivo_csv)

    # Verifique se o arquivo foi baixado
    if os.path.exists(caminho_csv):
        print(f"Arquivo CSV baixado com sucesso: {caminho_csv}")
    else:
        raise FileNotFoundError(f"O arquivo CSV não foi encontrado em: {caminho_csv}")

finally:
    # Fechar o driver
    driver.quit()
