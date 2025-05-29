import requests
import os
import warnings
import shutil
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

    password = cfg["PASSWORD"]

    data = {
        "username": cfg["USERNAME"],
        "password": password
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
    log_url = f"{cfg['GRC_API_URL']}/bwise/api/log"

    headers = {
        "bwise-session": session_id
    }

    response = requests.get(log_url, headers=headers, verify=False)

    if response.status_code == 200:
        return response.text.strip()
    else:
        return ""

def upload_xml_records_to_sai360(cfg, input_dir, processed_dir, error_dir, class_name):
    xml_files = [f for f in os.listdir(input_dir) if f.endswith('.xml')]

    for xml_file in xml_files:
        file_path = os.path.join(input_dir, xml_file)

        print(f"🚀 Processando arquivo: {xml_file}")

        try:
            session_id = sai360_login(cfg)

            with open(file_path, 'r', encoding='utf-8') as f:
                xml_data = f.read()

            endpoint = f"{cfg['GRC_API_URL']}/bwise/api/instances?class={class_name}"

            headers = {
                "bwise-session": session_id,
                "Content-Type": "application/xml"
            }

            response = requests.post(endpoint, headers=headers, data=xml_data, verify=False)

            if response.status_code == 200:
                print(f"✅ Upload bem-sucedido para {xml_file}.")
                append_to_log(cfg, f"[{xml_file}]: {response.status_code} {response.reason}")
                shutil.move(file_path, os.path.join(processed_dir, xml_file))
            else:
                print(f"❌ Erro no upload de {xml_file} (status {response.status_code}):")
                print(response.text)
                error_detail = response.text.strip()
                append_to_log(cfg, f"[{xml_file}]: {response.status_code} {response.reason} - {error_detail[:500]}")

                # Grava o corpo completo da resposta em um arquivo separado
                error_log_dir = cfg.get("LOG_PATH", ".")
                os.makedirs(error_log_dir, exist_ok=True)
                error_log_path = os.path.join(error_log_dir, f"{xml_file}_error_response.xml")
                with open(error_log_path, "w", encoding="utf-8") as f:
                    f.write(error_detail)

                shutil.move(file_path, os.path.join(error_dir, xml_file))

            session_log = get_sai360_session_log(cfg, session_id)
            if session_log:
                append_to_log(cfg, f"[{xml_file} LOG]: {session_log[:200]}...")

        except Exception as e:
            print(f"❌ Falha ao processar {xml_file}: {e}")
            shutil.move(file_path, os.path.join(error_dir, xml_file))

        finally:
            if 'session_id' in locals():
                sai360_logout(cfg, session_id)

def sai360_logout(cfg, session_id):
    """
    Encerra a sessão autenticada no SAI360.
    """
    logout_url = f"{cfg['GRC_API_URL']}/bwise/api/logout"

    headers = {
        "bwise-session": session_id,
        "Content-Type": "application/json"
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

def append_to_log(cfg, message):
    from datetime import datetime
    log_dir = cfg.get("LOG_PATH", ".")
    os.makedirs(log_dir, exist_ok=True)
    log_filename = datetime.now().strftime("%d-%m-%Y_sai360_uploader.log")
    log_path = os.path.join(log_dir, log_filename)

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(message + "\n")

def main():
    input_dir = cfg.get("INPUT_XML_DIR", "./input")
    processed_dir = cfg.get("PROCESSED_XML_DIR", "./processed")
    error_dir = cfg.get("ERROR_XML_DIR", "./error")

    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(error_dir, exist_ok=True)

    class_name = cfg["CLASS_NAME"]

    upload_xml_records_to_sai360(
        cfg=cfg,
        input_dir=input_dir,
        processed_dir=processed_dir,
        error_dir=error_dir,
        class_name=class_name
    )

if __name__ == "__main__":
    main()
