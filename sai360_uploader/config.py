cfg = {
    # URL base da API do SAI360 (sem barra no final)
    "GRC_API_URL": "https://ambipar.bwise.net",

    # Credenciais do usuário com permissão de API
    "USERNAME": "Admin",
    "PASSWORD": "P@rB1amBaMd1n24brGrC",

    # Caminho onde os logs de sessão serão salvos (para análise de falhas)
    "LOG_PATH": "./logs",  # Pode ser um caminho absoluto ou relativo

    # Diretórios de arquivos XML
    "INPUT_XML_DIR": "./input",
    "PROCESSED_XML_DIR": "./processed",
    "ERROR_XML_DIR": "./error",

    # Classe padrão (pode ser alterada dinamicamente)
    "CLASS_NAME": "lawsuit"
}
