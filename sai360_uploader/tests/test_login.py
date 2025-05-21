from sai360_data_uploader import sai360_login
from config import cfg

if __name__ == "__main__":
    try:
        session_id = sai360_login(cfg)
        print(f"🔐 Session ID obtido: {session_id}")
    except Exception as e:
        print(f"Erro no login: {e}")
