
# SAI360 Data Uploader

Módulo Python para automatizar o envio de arquivos XML para a API do SAI360.

## 📦 Instalação

```bash
pip install -e .
```

ou apenas clone e execute localmente.

## 🚀 Uso

**Via terminal:**

```bash
sai360-upload
```

**Ou via código:**

```python
from sai360_uploader import sai360_login, upload_xml_records_to_sai360
```

## ⚙️ Configuração

Edite o arquivo `config.py` com as credenciais e diretórios desejados:

```python
cfg = {
    "GRC_API_URL": "https://hostname.bwise.net",
    "USERNAME": "Admin",
    "PASSWORD": "password@123",

    "INPUT_XML_DIR": "./input",
    "PROCESSED_XML_DIR": "./processed",
    "ERROR_XML_DIR": "./error",

    "CLASS_NAME": "lawsuit",

    "LOG_PATH": "./logs"
}
```

**Nota:**  
Se deseja proteger a senha, recomendamos armazená-la em um arquivo separado (`.secrets.json`) ou via variável de ambiente.

## ✅ Estrutura de diretórios recomendada

```
sai360_uploader/
├── sai360_uploader/
│   ├── __init__.py
│   ├── uploader.py
├── config.py
├── setup.py
├── README.md
├── requirements.txt
├── input/
│   ├── file1.xml
│   ├── file2.xml
├── logs/
├── error/
├── processed/
```

## 📝 Sistema de Logs

A partir da versão atual, o script armazena **todos os logs de processamento** no diretório definido em `LOG_PATH`.

### ✅ Características:

- Cada execução escreve no arquivo de log correspondente ao **dia de execução**.
- O arquivo tem o formato:  
  `dd-mm-aaaa_sai360_uploader.log`

- Para cada arquivo XML processado, será adicionada uma linha no log com o formato:  
  `[nome-arquivo.xml]: [status_code] [status_reason]`

- Além disso, um trecho do log da sessão SAI360 também será adicionado:  
  `[nome-arquivo.xml LOG]: [conteúdo parcial do log da sessão...]`

### ✅ Como configurar:

No `config.py`:

```python
cfg = {
    ...
    "LOG_PATH": "./logs"
}
```

Se o diretório não existir, será criado automaticamente.

## ✅ Exemplo de fluxo:

1. Coloque arquivos `.xml` na pasta `./input`.
2. Execute: `python -m sai360_uploader.uploader` ou simplesmente `sai360-upload`
3. Arquivos serão movidos automaticamente para:
   - `./processed` → caso sucesso.
   - `./error` → caso falha.
4. Logs de cada execução estarão em `./logs/dd-mm-aaaa_sai360_uploader.log`.

## ✅ Dependências

- `requests`

Instale via:

```bash
pip install -r requirements.txt
```
