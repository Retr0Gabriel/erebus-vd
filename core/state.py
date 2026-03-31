import os

STATUS_FILE = "config.status"

def save_progress(index):
    """Salva a linha atual no disco."""
    with open(STATUS_FILE, 'w') as f:
        f.write(str(index))

def load_progress():
    """Lê a última linha processada salva no arquivo de status."""
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0