import sys
from datetime import datetime
from transaction import Transaction
from avl_tree import AVLTree, AVLNode

# Cores e Estilos para o Terminal
RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"

def clear_screen():
    # Limpa a tela de forma amigável no terminal Linux
    print("\033[H\033[J", end="")

def show_hud_header():
    print(f"{CYAN}{BOLD}" + "=" * 62)
    print(f"  🏦  SISTEMA DE LOG DE TRANSAÇÕES BANCÁRIAS (ÁRVORE AVL)  🏦  ")
    print("=" * 62 + f"{RESET}")

def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def show_menu():
    print(f"\n{BOLD}Escolha uma das opções abaixo:{RESET}")
    print(f"[{GREEN}1{RESET}] ➕ Registrar Nova Transação")
    print(f"[{GREEN}2{RESET}] 🔍 Buscar Transações por Data")
    print(f"[{GREEN}3{RESET}] 📋 Listar Todas as Transações (Ordem Cronológica)")
    print(f"[{GREEN}4{RESET}] 🌲 Visualizar Estrutura da Árvore AVL")
    print(f"[{RED}0{RESET}] ❌ Sair")
    print(f"{CYAN}" + "-" * 62 + f"{RESET}")

def get_tree_stats(node: AVLNode) -> tuple:
    if not node:
        return 0, 0
    
    # Faz uma contagem recursiva simples
    left_count, left_nodes = get_tree_stats(node.left)
    right_count, right_nodes = get_tree_stats(node.right)
    
    total_txs = len(node.transactions) + left_count + right_count
    total_nodes = 1 + left_nodes + right_nodes
    return total_txs, total_nodes

def main():
    tree = AVLTree()
    root = None

    # Transações pré-carregadas para demonstração
    preload_data = [
        ("T101", 1500.00, "2026-06-08"),
        ("T102", -200.00, "2026-06-07"),
        ("T103", 450.50, "2026-06-09"),
        ("T104", -75.00, "2026-06-06"),
        ("T105", 2000.00, "2026-06-11"),
        ("T106", -150.00, "2026-06-10"),
    ]

    for tx_id, valor, timestamp in preload_data:
        tx = Transaction(tx_id, valor, timestamp)
        root = tree.insert(root, tx)

    clear_screen()
    show_hud_header()
    print(f"{GREEN}Sistema iniciado com sucesso! 6 transações pré-carregadas para demonstração.{RESET}")

    while True:
        show_menu()
        try:
            opcao = input(f"{BOLD}Digite a opção desejada: {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{RED}Operação cancelada. Saindo...{RESET}")
            sys.exit(0)

        if opcao == "1":
            clear_screen()
            show_hud_header()
            print(f"{BLUE}{BOLD}📝 REGISTRO DE NOVA TRANSAÇÃO{RESET}\n")

            # ID da transação
            tx_id = input(f"{BOLD}ID da Transação (ex: T201) [Enter para auto-gerar]: {RESET}").strip()
            if not tx_id:
                tx_id = f"T{int(datetime.now().timestamp()) % 10000:04d}"
                print(f"ID auto-gerado: {YELLOW}{tx_id}{RESET}")

            # Valor
            while True:
                try:
                    valor_str = input(f"{BOLD}Valor (ex: 150.50 ou -50.00): {RESET}").strip()
                    valor = float(valor_str)
                    break
                except ValueError:
                    print(f"{RED}❌ Valor inválido. Digite um número decimal (use ponto para centavos).{RESET}")

            # Timestamp (Data)
            while True:
                data_hoje = datetime.now().strftime("%Y-%m-%d")
                timestamp = input(f"{BOLD}Data (Formato YYYY-MM-DD) [Enter para hoje: {data_hoje}]: {RESET}").strip()
                if not timestamp:
                    timestamp = data_hoje
                    break
                if validate_date(timestamp):
                    break
                print(f"{RED}❌ Data inválida ou no formato incorreto. Use YYYY-MM-DD.{RESET}")

            # Inserir
            tx = Transaction(tx_id, valor, timestamp)
            root = tree.insert(root, tx)
            print(f"\n{GREEN}✔️ Transação registrada com sucesso e adicionada à Árvore AVL!{RESET}")

        elif opcao == "2":
            clear_screen()
            show_hud_header()
            print(f"{BLUE}{BOLD}🔍 BUSCA DE TRANSAÇÕES POR DATA{RESET}\n")
            
            data_hoje = datetime.now().strftime("%Y-%m-%d")
            timestamp = input(f"{BOLD}Digite a data para busca (YYYY-MM-DD) [Enter para hoje: {data_hoje}]: {RESET}").strip()
            if not timestamp:
                timestamp = data_hoje

            if not validate_date(timestamp):
                print(f"{RED}❌ Data inválida ou formato incorreto (use YYYY-MM-DD).{RESET}")
            else:
                resultados = tree.search(root, timestamp)
                if resultados:
                    print(f"\n{GREEN}Encontrada(s) {len(resultados)} transação(ões) para a data {timestamp}:{RESET}")
                    total_dia = 0.0
                    for r in resultados:
                        print(f"  • {r}")
                        total_dia += r.valor
                    sinal = "+" if total_dia >= 0 else ""
                    cor_sinal = GREEN if total_dia >= 0 else RED
                    print(f"\nSaldo total do dia: {cor_sinal}{sinal}R$ {total_dia:.2f}{RESET}")
                else:
                    print(f"\n{YELLOW}Nenhuma transação encontrada para a data {timestamp}.{RESET}")

        elif opcao == "3":
            clear_screen()
            show_hud_header()
            print(f"{BLUE}{BOLD}📋 LISTA COMPLETA DE TRANSAÇÕES (ORDEM CRONOLÓGICA){RESET}\n")

            transacoes = []
            tree.inorder_traversal(root, transacoes)

            if not transacoes:
                print(f"{YELLOW}Nenhuma transação registrada no sistema.{RESET}")
            else:
                print(f"{UNDERLINE}{'Data':<12} | {'ID':<8} | {'Valor':>15}{RESET}")
                saldo_total = 0.0
                for tx in transacoes:
                    cor_valor = GREEN if tx.valor >= 0 else RED
                    sinal = "+" if tx.valor >= 0 else ""
                    print(f"{tx.timestamp:<12} | {tx.id:<8} | {cor_valor}{sinal}R$ {tx.valor:11.2f}{RESET}")
                    saldo_total += tx.valor
                
                print("-" * 45)
                cor_saldo = GREEN if saldo_total >= 0 else RED
                sinal_saldo = "+" if saldo_total >= 0 else ""
                print(f"{BOLD}{'SALDO ACUMULADO GERAL:':<23} {cor_saldo}{sinal_saldo}R$ {saldo_total:.2f}{RESET}")

        elif opcao == "4":
            clear_screen()
            show_hud_header()
            print(f"{BLUE}{BOLD}🌲 ESTRUTURA VISUAL DA ÁRVORE AVL{RESET}\n")

            if not root:
                print(f"{YELLOW}A árvore está vazia.{RESET}")
            else:
                total_txs, total_nodes = get_tree_stats(root)
                print(f"{BOLD}Estatísticas da Árvore:{RESET}")
                print(f"  • Nós criados (Datas únicas): {YELLOW}{total_nodes}{RESET}")
                print(f"  • Altura da Árvore: {YELLOW}{root.height}{RESET}")
                print(f"  • Total de Transações: {YELLOW}{total_txs}{RESET}")
                print("\n" + "-" * 62 + "\n")

                lines = tree.get_tree_structure_lines(root)
                for line in lines:
                    # Colorir conexões para destacar
                    colored_line = line.replace("├──", f"{CYAN}├──{RESET}").replace("└──", f"{CYAN}└──{RESET}").replace("│", f"{CYAN}│{RESET}")
                    colored_line = colored_line.replace("Esq:", f"{MAGENTA}Esq:{RESET}").replace("Dir:", f"{MAGENTA}Dir:{RESET}").replace("Raiz:", f"{YELLOW}Raiz:{RESET}")
                    print(colored_line)
                
                print(f"\n{YELLOW}Nota: B representa o Fator de Balanceamento (Altura Esq - Altura Dir).{RESET}")

        elif opcao == "0":
            print(f"\n{GREEN}Obrigado por utilizar o log de transações AVL! Saindo...{RESET}\n")
            break
        else:
            print(f"\n{RED}❌ Opção inválida! Digite um número de 0 a 4.{RESET}")

if __name__ == "__main__":
    main()
