from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import os
import time
import glob

def executar_equipes_homologadas(driver, pasta_download):
    valor_desejado = None

    # Abra o site
    driver.get('https://sisab.saude.gov.br/paginas/acessoRestrito/relatorio/federal/indicadores/indicadorCadastro.xhtml')

    # Imprimir o HTML da página para depuração (opcional)
    # print(driver.page_source)

    # Aguarde e selecione a caixa "Nível de visualização"
    nivel_visualizacao = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#selectLinha'))
    )
    Select(nivel_visualizacao).select_by_value('ibge')  # Seleciona a opção com o valor 'ibge'

    # Aguarde e selecione a caixa "Condição das Equipes"
    condicao_equipes = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#opacao-capitacao'))
    )
    Select(condicao_equipes).select_by_value('|HM|')  # Seleciona a opção com o valor '|HM|'

    # Selecionar a competência mais recente
    driver.find_element(By.CSS_SELECTOR, '.multiselect.dropdown-toggle').click()
    options = WebDriverWait(driver, 100).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.multiselect-container .checkbox input[type="checkbox"]'))
    )

    if options:
        max_value_checkbox = max(options, key=lambda opt: int(opt.get_attribute('value')) if opt.get_attribute('value').isdigit() else -1)
        valor_desejado = max_value_checkbox.get_attribute('value')

        if not max_value_checkbox.is_selected():
            max_value_checkbox.click()

        print(f"Checkbox selecionado com valor: {valor_desejado}")
        driver.find_element(By.CSS_SELECTOR, '.multiselect.dropdown-toggle').click()
    else:
        print("Nenhuma checkbox encontrada no menu 'Competência'")

    # Clique no botão de download e selecione CSV
    download_button = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-group .btn'))
    )
    download_button.click()

    # Executa script para acionar o download do CSV
    js_script = """
    var element = document.querySelector('a[onclick*="j_idt85"]');
    if (element) {
        element.click();
    } else {
        console.error("Elemento de download CSV não encontrado.");
    }
    """
    driver.execute_script(js_script)
    print("Opção CSV selecionada com sucesso.")

    # Aguarda o download
    print("Aguardando o download do arquivo...")
    time.sleep(30)  # Ajuste conforme necessário

    # Verifique o nome do arquivo baixado e renomeie
    arquivos_csv = glob.glob(os.path.join(pasta_download, '*.csv'))
    arquivo_cadastro_individual = os.path.join(pasta_download, 'cadastro-individual.csv')
    arquivos_para_renomear = [f for f in arquivos_csv if not f.startswith(os.path.join(pasta_download, 'sisab_todas_equipes'))]

    if arquivos_para_renomear:
        arquivo_original = arquivos_para_renomear[0]
        nome_arquivo_csv = f'sisab_equipes_homologadas_{valor_desejado}.csv'
        caminho_csv = os.path.join(pasta_download, nome_arquivo_csv)

        if not os.path.exists(caminho_csv):
            os.rename(arquivo_original, caminho_csv)
            print(f"Arquivo CSV renomeado com sucesso para: {caminho_csv}")
        else:
            print(f"O arquivo {nome_arquivo_csv} já existe e não será alterado.")
    else:
        print("Nenhum arquivo CSV válido encontrado para renomear.")

    # Exclusão do arquivo cadastro-individual.csv se existir
    if os.path.exists(arquivo_cadastro_individual):
        os.remove(arquivo_cadastro_individual)
        print(f"Arquivo {arquivo_cadastro_individual} excluído.")

    print("SCRIPT FINALIZADO")
