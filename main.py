import argparse
import sys
from core.wordlist import get_passwords
from core.state import load_progress
from core.engine import BruteforceEngine
from modules.ssh_module import SSHModule

# Códigos de cores ANSI para o terminal
CYAN = '\033[96m'
RED = '\033[91m'
BOLD = '\033[1m'
ENDC = '\033[0m' # Reseta para a cor padrão

def print_banner():
    """Exibe o banner ASCII colorido do ErebusVD."""
    # ASCII Art
    banner_ascii = f"""
{CYAN} {BOLD}
████▀░░░░░░░░░░░░░░░░░▀████
███│░░░░░░ErebusVD░░░░░│███
██▌│░░░░░░░░░░░░░░░░░░░│▐██
██░└┐░░░░░░░░░░░░░░░░░┌┘░██
██░░└┐░░░░░░░░░░░░░░░┌┘░░██
██░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██
██▌░│██████▌░░░▐██████│░▐██
███░│▐███▀▀░░▄░░▀▀███▌│░███
██▀─┘░░░░░░░▐█▌░░░░░░░└─▀██
██▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄██
████▄─┘██▌░░░░░░░▐██└─▄████
█████░░▐█─┬┬┬┬┬┬┬─█▌░░█████
████▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐████
█████▄░░░└┴┴┴┴┴┴┴┘░░░▄█████
███████▄░░░░░░░░░░░▄██████ {ENDC}
    """
    
    # Subtítulo com destaque
    sub_title = f"{BOLD} {RED}  [>]{ENDC} {BOLD}Erebus Verification Daemon{ENDC} - {CYAN}Academic BruteForce Tool v1.0{ENDC}"
    status_line = f"{CYAN} [=]{ENDC} Modular Engine | Threading Pool | State Persistence"
    divisor = f"{CYAN}{BOLD}" + "="*68 + f"{ENDC}"

    print(banner_ascii)
    print(sub_title)
    print(status_line)
    print(divisor)
    print("")

def main():
    # Verifica se o terminal suporta cores
    global CYAN, RED, BOLD, ENDC
    if not sys.stdout.isatty():
        # Desativa cores se não for um terminal interativo ou se a saída for redirecionada
        CYAN = RED = BOLD = ENDC = ''

    # Exibe o banner Dark Hacker
    print_banner()

    parser = argparse.ArgumentParser(description="Ferramenta de Bruteforce Acadêmica")
    parser.add_argument("-t", "--target", required=True, help="IP do alvo")
    parser.add_argument("-u", "--user", required=True, help="Usuário alvo")
    parser.add_argument("-w", "--wordlist", required=True, help="Caminho da wordlist")
    parser.add_argument("-th", "--threads", type=int, default=2, help="Threads (padrão 2)")
    parser.add_argument("-d", "--delay", type=float, default=1.0, help="Atraso entre tentativas (segundos)")
    parser.add_argument("-r", "--retries", type=int, default=2, help="Número de retentativas em caso de erro")
    
    args = parser.parse_args()

    # 1. Carrega progresso anterior
    last_index = load_progress()
    
    if last_index > 0:
        print(f"[*] Retomando o ataque a partir da linha {last_index} da wordlist...\n")
    
    # 2. Instancia o módulo desejado
    module = SSHModule(args.target, args.user, delay=args.delay, max_retries=args.retries)
    
    # 3. Configura o gerador e o motor
    passwords = get_passwords(args.wordlist, start_at=last_index)
    engine = BruteforceEngine(module, max_threads=args.threads)
    
    # 4. Inicia
    try:
        engine.run(passwords)
    except KeyboardInterrupt:
        # Usa a cor vermelha para destacar a interrupção
        print(f"\n{RED}[!] Ataque interrompido pelo usuário. Progresso salvo com sucesso.{ENDC}")

if __name__ == "__main__":
    main()