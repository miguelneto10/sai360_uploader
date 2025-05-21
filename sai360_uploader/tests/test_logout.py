import time
from sai360_data_uploader import sai360_login, sai360_logout, get_sai360_session_log
from config import cfg

if __name__ == "__main__":
    try:
        # Etapa 1: Login
        session_id = sai360_login(cfg)
        print(f"🔐 Session ID: {session_id}")

        # Etapa 2: Validar sessão com log
        get_sai360_session_log(cfg, session_id)

        # Espera de 5 segundos antes de logout
        print("⏳ Aguardando 5 segundos antes de encerrar a sessão...")
        time.sleep(5)

    finally:
        # Etapa 3: Logout
        if 'session_id' in locals():
            sai360_logout(cfg, session_id)
