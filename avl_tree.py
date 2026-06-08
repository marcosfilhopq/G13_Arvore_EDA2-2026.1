from typing import List, Optional
from transaction import Transaction

class AVLNode:
    """
    Representa um nó na Árvore AVL.
    A chave é o timestamp (data no formato YYYY-MM-DD).
    O valor é uma lista de transações ocorridas naquela data.
    """
    def __init__(self, key: str, transaction: Transaction):
        self.key: str = key
        self.transactions: List[Transaction] = [transaction]
        self.left: Optional[AVLNode] = None
        self.right: Optional[AVLNode] = None
        self.height: int = 1  # Novo nó é inicialmente adicionado com altura 1


class AVLTree:
    """
    Árvore AVL auto-balanceável para armazenamento de transações bancárias por data.
    """
    def _get_height(self, node: Optional[AVLNode]) -> int:
        if not node:
            return 0
        return node.height

    def _get_balance(self, node: Optional[AVLNode]) -> int:
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _right_rotate(self, y: AVLNode) -> AVLNode:
        """
        Rotaciona a subárvore enraizada em y para a direita.
        """
        x = y.left
        T2 = x.right

        # Realiza a rotação
        x.right = y
        y.left = T2

        # Atualiza as alturas
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))

        # Retorna a nova raiz
        return x

    def _left_rotate(self, x: AVLNode) -> AVLNode:
        """
        Rotaciona a subárvore enraizada em x para a esquerda.
        """
        y = x.right
        T2 = y.left

        # Realiza a rotação
        y.left = x
        x.right = T2

        # Atualiza as alturas
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        # Retorna a nova raiz
        return y

    def insert(self, root: Optional[AVLNode], transaction: Transaction) -> AVLNode:
        """
        Insere uma transação na árvore AVL, balanceando-a se necessário.
        """
        # 1. Inserção normal de BST
        if not root:
            return AVLNode(transaction.timestamp, transaction)

        if transaction.timestamp == root.key:
            # Se a data já existir, adicionamos à lista de transações deste dia
            # e a estrutura da árvore não muda
            root.transactions.append(transaction)
            return root
        elif transaction.timestamp < root.key:
            root.left = self.insert(root.left, transaction)
        else:
            root.right = self.insert(root.right, transaction)

        # 2. Atualiza a altura deste nó pai
        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))

        # 3. Obtém o fator de balanceamento para verificar se desbalanceou
        balance = self._get_balance(root)

        # Casos de Desbalanceamento:

        # Caso 1: Esquerda Esquerda (Left Left)
        if balance > 1 and transaction.timestamp < root.left.key:
            return self._right_rotate(root)

        # Caso 2: Direita Direita (Right Right)
        if balance < -1 and transaction.timestamp > root.right.key:
            return self._left_rotate(root)

        # Caso 3: Esquerda Direita (Left Right)
        if balance > 1 and transaction.timestamp > root.left.key:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)

        # Caso 4: Direita Esquerda (Right Left)
        if balance < -1 and transaction.timestamp < root.right.key:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)

        # Retorna o nó (inalterado ou rotacionado)
        return root

    def search(self, root: Optional[AVLNode], timestamp: str) -> List[Transaction]:
        """
        Busca transações correspondentes a um timestamp específico.
        """
        if not root:
            return []
        
        if timestamp == root.key:
            return root.transactions
        elif timestamp < root.key:
            return self.search(root.left, timestamp)
        else:
            return self.search(root.right, timestamp)

    def inorder_traversal(self, root: Optional[AVLNode], result: List[Transaction]) -> List[Transaction]:
        """
        Preenche a lista result com transações em ordem cronológica.
        """
        if root:
            self.inorder_traversal(root.left, result)
            result.extend(root.transactions)
            self.inorder_traversal(root.right, result)
        return result

    def get_tree_structure_lines(self, node: Optional[AVLNode], prefix: str = "", is_tail: bool = True, label: str = "Raiz") -> List[str]:
        """
        Gera uma lista de strings contendo uma representação visual ASCII da árvore AVL.
        """
        if not node:
            return []

        lines = []
        connector = "└── " if is_tail else "├── "
        bal = self._get_balance(node)
        lines.append(f"{prefix}{connector}{label}: {node.key} [Alt: {node.height} | Bal: {bal:+.0f}] ({len(node.transactions)} txs)")

        new_prefix = prefix + ("    " if is_tail else "│   ")

        # Exibe os filhos somente se ao menos um existir
        if node.left or node.right:
            if node.left:
                lines.extend(self.get_tree_structure_lines(node.left, new_prefix, is_tail=False, label="Esq"))
            else:
                lines.append(f"{new_prefix}├── Esq: None")

            if node.right:
                lines.extend(self.get_tree_structure_lines(node.right, new_prefix, is_tail=True, label="Dir"))
            else:
                lines.append(f"{new_prefix}└── Dir: None")

        return lines
