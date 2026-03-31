import paramiko
import socket
import time
import logging
from .base import BaseModule

# Suprime todos os logs do paramiko (incluindo erros)
logging.getLogger("paramiko").setLevel(logging.CRITICAL)

class SSHModule(BaseModule):
    """
    Módulo SSH com retry automático em caso de erros de rede.
    """
    def __init__(self, target, username, port=22, timeout=10, delay=1.0, max_retries=2):
        """
        :param target: IP ou hostname
        :param username: usuário alvo
        :param port: porta SSH (padrão 22)
        :param timeout: tempo máximo de espera por conexão (segundos)
        :param delay: pausa entre tentativas (segundos)
        :param max_retries: número máximo de retentativas em caso de erro de rede
        """
        super().__init__(target, username)
        self.port = port
        self.timeout = timeout
        self.delay = delay
        self.max_retries = max_retries

    def connect(self, password):
        """
        Tenta autenticar com a senha fornecida.
        Em caso de erro de rede, faz até `max_retries` tentativas antes de retornar False.
        """
        # Atraso inicial para não sobrecarregar
        time.sleep(self.delay)

        retry_count = 0
        while retry_count <= self.max_retries:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            try:
                client.connect(
                    hostname=self.target,
                    port=self.port,
                    username=self.username,
                    password=password,
                    timeout=self.timeout,
                    look_for_keys=False,
                    allow_agent=False
                )
                client.close()
                return True  # sucesso

            except paramiko.AuthenticationException:
                # Credenciais inválidas – falha definitiva
                return False

            except (paramiko.SSHException, socket.error, TimeoutError,
                    ConnectionResetError, EOFError, OSError) as e:
                # Erros de rede/protocolo – pode ser temporário
                retry_count += 1
                if retry_count <= self.max_retries:
                    # Aguarda um pouco antes de tentar novamente
                    time.sleep(1.0 * retry_count)  # espera crescente
                    continue
                else:
                    # Esgotou as tentativas, considera falha
                    return False

            except Exception as e:
                # Qualquer outro erro inesperado
                return False

        return False