from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

def executar_equipes_homologadas(driver, pasta_download):
    valor_desejado = None

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
            from selenium.webdriver.support.ui import Select
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
        except Exception as e:
            print("Erro ao selecionar 'Competência':", e)

        # Clique no botão de download e selecione CSV
        try:
            download_button = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-group .btn'))
            )
            download_button.click()
            js_script = """
            function simulateCsvDownload() {
                var element = document.querySelector('a[onclick*="j_idt85"]');
                if (element) {
                    element.click();
                } else {
                    console.error("Elemento de download CSV não encontrado.");
                }
            }
            simulateCsvDownload();
            """
            driver.execute_script(js_script)
            print("Opção CSV selecionada com sucesso.")
        except Exception as e:
            print("Erro ao clicar no botão de download ou selecionar a opção CSV:", e)
            driver.save_screenshot("screenshot.png")

        # Ajustar o tempo conforme necessário
        time.sleep(30)
        
        # Nome do arquivo CSV com o valor da checkbox
        nome_arquivo_csv = f'sisab_equipes_homologadas_{valor_desejado}.csv'
        caminho_csv = os.path.join(pasta_download, nome_arquivo_csv)

        if os.path.exists(caminho_csv):
            print(f"Arquivo CSV baixado com sucesso: {caminho_csv}")
        else:
            raise FileNotFoundError(f"O arquivo CSV não foi encontrado em: {caminho_csv}")

    finally:
        print("Fechando o driver...")