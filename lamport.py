# Atividade Prática: Simulação de Relógios Lógicos de Lamport
# Aluno: Cauan Alves Pinho
# Disciplina: Sistemas Distribuídos

class Processo:
    def __init__(self, id_nome):
        """
        Inicializa um processo com um identificador e relógio lógico zerado.
        """
        self.id = id_nome
        self.relogio = 0 

    def evento_interno(self):
        """
        Simula um evento interno no processo.
        Regra 1 de Lamport: Incrementa o relógio local.
        """
        self.relogio += 1
        print(f"[{self.id}] Evento Interno. Relógio: {self.relogio}")

    def enviar_mensagem(self, destinatario_id):
        """
        Simula o envio de uma mensagem para outro processo.
        Regra 1: Incrementa o relógio antes de enviar.
        Regra 2 (Envio): Anexa o timestamp à mensagem.
        """
        self.relogio += 1
        timestamp_envio = self.relogio
        print(f"[{self.id}] Envia msg para {destinatario_id}. Timestamp da msg: {timestamp_envio} (Relógio local: {self.relogio})")
        return {"conteudo": "msg", "timestamp": timestamp_envio}

    def receber_mensagem(self, remetente_id, mensagem):
        """
        Simula o recebimento de uma mensagem.
        Regra 2 (Recebimento): Ajusta o relógio para max(local, msg) + 1.
        """
        timestamp_msg = mensagem['timestamp']
        
        # O relógio deve ser maior que o atual e maior que o da mensagem recebida
        self.relogio = max(self.relogio, timestamp_msg) + 1
        
        print(f"[{self.id}] Recebe msg de {remetente_id} (Ts: {timestamp_msg}). Novo Relógio: {self.relogio}")

# --- Execução Principal da Simulação ---

if __name__ == "__main__":
    print("--- Iniciando Simulação de Lamport ---\n")

    # Instanciação dos processos
    p1 = Processo("P1")
    p2 = Processo("P2")
    p3 = Processo("P3")

    # Sequência de eventos definida no enunciado:
    
    # 1. P1: Evento interno.
    p1.evento_interno()

    # 2. P2: Envia mensagem para P3.
    msg_p2_para_p3 = p2.enviar_mensagem("P3")

    # 3. P3: Recebe mensagem de P2.
    p3.receber_mensagem("P2", msg_p2_para_p3)

    # 4. P1: Envia mensagem para P2.
    msg_p1_para_p2 = p1.enviar_mensagem("P2")

    # 5. P3: Evento interno.
    p3.evento_interno()

    # 6. P2: Recebe mensagem de P1.
    p2.receber_mensagem("P1", msg_p1_para_p2)

    # 7. P2: Envia mensagem para P1.
    msg_p2_para_p1 = p2.enviar_mensagem("P1")

    # 8. P1: Recebe mensagem de P2.
    p1.receber_mensagem("P2", msg_p2_para_p1)

    print("\n--- Estado Final dos Relógios ---")
    print(f"P1: {p1.relogio}")
    print(f"P2: {p2.relogio}")
    print(f"P3: {p3.relogio}")
