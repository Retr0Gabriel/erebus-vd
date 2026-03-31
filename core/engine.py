from concurrent.futures import ThreadPoolExecutor
import threading
from .state import save_progress

class BruteforceEngine:
    def __init__(self, module, max_threads=10):
        self.module = module
        self.max_threads = max_threads
        self.lock = threading.Lock()
        self.found = False

    def _worker(self, data):
        password, index = data
        if self.found:
            return

        try:
            result = self.module.connect(password)
            if result is True:
                print(f"\n[!] SUCESSO! Senha encontrada: {password}")
                self.found = True
        except Exception as e:
            print(f"[!] Erro inesperado ao testar senha '{password}': {e}")

        # Salva progresso (se encontrou, ainda salva o índice, mas não importa)
        with self.lock:
            save_progress(index)

    def run(self, generator):
        print(f"[*] Iniciando motor com {self.max_threads} threads...")
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            executor.map(self._worker, generator)