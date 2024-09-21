# 🏥 **Crawler SISAB** - Download de Cadastros de Equipes de Saúde

Automatize o processo de download dos cadastros das equipes de Saúde da Família (eSF) e Atenção Primária (eAP) diretamente do [SISAB](https://sisab.saude.gov.br/), facilitando o acesso aos dados essenciais para o modelo de **Capitação Ponderada** do Ministério da Saúde.


---

## 🏗️ **Contexto**

A **Capitação Ponderada** é um modelo de financiamento no qual os repasses do Ministério da Saúde são baseados no número de pessoas cadastradas nas equipes de Saúde da Família (eSF) e Atenção Primária (eAP). Este projeto visa:

✅ Automatizar a obtenção de relatórios de equipes **homologadas** ou **todas as equipes**.

✅ Facilitar o **cálculo dos repasses financeiros** para municípios e o Distrito Federal.

---

## ✨ **Funcionalidades**

- 📥 **Download Automatizado**: Extrai relatórios das equipes de saúde diretamente do portal SISAB.
- ⚙️ **Seleção de Equipes**: Escolha entre equipes **homologadas** ou **todas as equipes**.
- 📊 **Renomeação Inteligente**: Organiza os arquivos CSV baixados por competência.
- 💸 **Integração com Modelos de Repasse**: Auxilia no cálculo de repasses financeiros com base nos dados capturados.

---

## ⚙️ **Instalação**

### 🛠️ Pré-requisitos

- [Python 3.x](https://www.python.org/downloads/)
  
- [Selenium WebDriver](https://www.selenium.dev/)
  
- [Google Chrome](https://www.google.com/chrome/) ou outro navegador compatível
  
- Dependências Python:
  ```bash
  pip install selenium

### 🔧 Configuração do WebDriver

Baixe o [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) e adicione-o ao seu `PATH`:

- **Windows**: Adicione o caminho do ChromeDriver nas configurações de variáveis de ambiente do sistema.
- **Linux/Mac**: Mova o executável para `/usr/local/bin` ou outro diretório incluído no seu `PATH`.

---

### 🚀 Uso

1. Clone o repositório:

   ```bash
   git clone https://github.com/WizardCodeForge/crawler-sisab.git
   cd crawler-sisab

2. Configure o caminho da pasta de download para salvar os arquivos CSV.

3. Execute o arquivo main.py para baixar os CSVs das equipes homologadas e de todas as equipes:

     ```python
     python main.py
     ```
     
🎉 O arquivo CSV será baixado, renomeado e salvo na pasta configurada.

---

### 🤝 Contribuição

Sinta-se à vontade para enviar **pull requests** ou abrir **issues**. Melhorias são sempre bem-vindas! 🙌

---

### 📜 Licença

Este projeto é licenciado sob a [MIT License](LICENSE). 📝

