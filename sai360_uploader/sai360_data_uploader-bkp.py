import requests
import os
import warnings
from config import cfg

warnings.filterwarnings("ignore")


def sai360_login(cfg):
    """
    Autentica na API SAI360 via POST x-www-form-urlencoded e retorna o sessionid.
    """
    login_url = f"{cfg['GRC_API_URL']}/bwise/api/login"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }

    data = {
        "username": cfg["USERNAME"],
        "password": cfg["PASSWORD"]
    }

    print(f"▶️ Realizando login no SAI360 como '{cfg['USERNAME']}'...")
    response = requests.post(login_url, headers=headers, data=data, verify=False)

    if response.status_code == 200:
        session_id = response.json().get("sessionid")
        if session_id:
            print("✅ Login realizado com sucesso.")
            return session_id
        else:
            raise Exception("❌ Login falhou: sessionid não retornado.")
    else:
        print(f"❌ Erro no login: {response.status_code}")
        print(response.text)
        raise Exception("Erro ao autenticar na API SAI360.")


def get_sai360_session_log(cfg, session_id):
    """
    Recupera o log da sessão atual da API SAI360.
    """
    log_url = f"{cfg['GRC_API_URL']}/bwise/api/log"

    headers = {
        "bwise-session": session_id
    }

    print("🧾 Recuperando log da sessão atual...")
    response = requests.get(log_url, headers=headers, verify=False)

    if response.status_code == 200:
        log_path = os.path.join(cfg.get("LOG_PATH", "."), "sai360_session.log")
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"📄 Log salvo em: {log_path}")
    elif response.status_code == 400:
        print("⚠️ Nenhum log disponível para a sessão atual.")
    elif response.status_code == 403:
        print("❌ Sessão inválida ou expirada.")
    else:
        print(f"❌ Erro ao recuperar log (status {response.status_code})")
        print(response.text)


def upload_staging_data_to_sai360(cfg, session_id, staging_table, class_name, id_column):
    """
    Envia dados da tabela staging para a classe correspondente no SAI360.
    """
    endpoint = f"{cfg['GRC_API_URL']}/bwise/api/class/{class_name}"

    headers = {
        "bwise-session": session_id,
        "Content-Type": "application/json"
    }

    body = {
        "table": staging_table,
        "idColumn": id_column
    }

    print(f"🚀 Enviando dados da tabela '{staging_table}' para a classe '{class_name}'...")
    response = requests.post(endpoint, headers=headers, json=body, verify=False)

    if response.status_code == 200:
        print("✅ Dados enviados com sucesso.")
        print(response.json())
    else:
        print(f"❌ Erro ao enviar dados (status {response.status_code}):")
        print(response.text)
        get_sai360_session_log(cfg, session_id)


def sai360_logout(cfg, session_id):
    """
    Encerra a sessão autenticada no SAI360.
    """
    logout_url = f"{cfg['GRC_API_URL']}/bwise/api/logout"

    headers = {
        "bwise-session": session_id
    }

    print("🚪 Encerrando sessão...")
    response = requests.post(logout_url, headers=headers, verify=False)

    if response.status_code == 200:
        print("✅ Logout realizado com sucesso.")
    elif response.status_code == 403:
        print("⚠️ Sessão já estava inválida.")
    else:
        print(f"❌ Erro no logout (status {response.status_code})")
        print(response.text)


if __name__ == "__main__":
    try:
        session_id = sai360_login(cfg)

        upload_staging_data_to_sai360(
            cfg=cfg,
            session_id=session_id,
            staging_table="dis_users_temp",
            class_name="UserElement",
            id_column="userId"
        )

    finally:
        if 'session_id' in locals():
            sai360_logout(cfg, session_id)
