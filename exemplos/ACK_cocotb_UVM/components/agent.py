'''
# +FHDR------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Copyright (c) 2025 von Braun Design Center, Inc. Todos os direitos reservados
# -----------------------------------------------------------------------------
# Confidencial - Propriedade do CPA Wernher von Braun
# -----------------------------------------------------------------------------
# Item da verificação:
# NOME DO ARQUIVO: agent.py
# REFERENCIA:      BlockGuide_ACK_PAv2.docx
# DEPARTAMENTO:    Microeletronica
# AUTOR:           Matheus Grossi
# EMAIL:           matheus.grossi@vonbraunlabs.com.br
# CO-AUTOR:        Marcelo Rodrigues Soares
# EMAIL:           marcelo.soares@vonbraunlabs.com.br
# -----------------------------------------------------------------------------
# Bloco em estudo:
# NOME DO ARQUIVO: ack_pav2.v
# REFERENCIA:      Transponder – vB – Documento de projeto do bloco ACK
# DEPARTAMENTO:    Inovacao
# AUTOR:           Guilherme Pereira
# EMAIL DO AUTOR:  guilherme.pereira@vonbraunlabs.com.br
# -----------------------------------------------------------------------------
# HISTORICO DAS VERSOES
# VERSAO      DATA        AUTOR             DESCRICAO
# 1.0         15/10/2025  Matheus Grossi    Elaboração da rotina de testes
# -----------------------------------------------------------------------------
# PALAVRAS-CHAVE: ISO18000-6C Ack
# -----------------------------------------------------------------------------
# PROPOSITO: Ler as informacoes necessarias do banco UII e responder conforme
# especificado para o projeto.
'''

#----------------------------------------------------------------------------------------------------------------------------
# Arquivo Agent: 
#----------------------------------------------------------------------------------------------------------------------------

#Instâncias de bibliotecas:
from pyuvm import *                                                   
from .driver import Driver
from .monitor import Monitor

class Agent(uvm_agent):                                                 # type: ignore
    """
    O Agent encapsula: driver, monitor e o sequenciador de interface.
    ele também atua como uma cola que faz todos funcionarem de forma conjunta e permitindo a mecânica de reuso.
    """

    def build_phase(self):    
        
    #A função "build_phase", é responsável por agrupar os 3 membros fundamentais:
        
    # O sequenciador (seqr): Emite a ordem correta de dados a serem executador pelo o driver.
        self.seqr = uvm_sequencer.create("seqr", self)                  # type: ignore
        
    # O Driver: Converte os dados vindos do sequenciador para estímulos de sinais do dut, quando o BFM está em modo ativo.
    # A instrução abaixo irá consumir os itens vindos de sequencer e dirigirá os sinais do DUT
        self.driver = Driver.create("driver", self)
        
    # O Monitor: Observa o barramento e publoca as transações obersvadas, quando o BFM está em modo passivo. 
    # Os dados observados por ele serão enviados ao analysis_port.
        self.monitor = Monitor.create("monitor", self)

    def connect_phase(self):
    # Este é o "barramento de conexões", e será o responsável por interligar
    # TLM, Ports/Exports ao sequenciador e ao driver.

    # Habilita o envio de dados do sequenciador para o driver.
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)
        
    # Esta etapa ajusta o envio para o receptor:
        self.driver_ap = self.driver.ap
        self.monitor_ap = self.monitor.ap

