class Transaction:
    """
    Representa uma transação bancária individual.
    """
    def __init__(self, transaction_id: str, valor: float, timestamp: str):
        self.id = transaction_id
        self.valor = valor
        self.timestamp = timestamp  # Formato simplificado YYYY-MM-DD

    def __repr__(self) -> str:
        sinal = "+" if self.valor >= 0 else ""
        return f"[ID: {self.id} | Valor: R$ {sinal}{self.valor:.2f} | Data: {self.timestamp}]"
