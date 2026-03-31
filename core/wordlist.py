def get_passwords(file_path, start_at=0):
    """Lê a wordlist linha por linha sem carregar tudo na RAM."""
    with open(file_path, 'r', encoding='latin-1', errors='ignore') as f:
        for _ in range(start_at):
            next(f, None)
        
        for current_idx, line in enumerate(f, start=start_at):
            yield line.strip(), current_idx