'''
# +FHDR------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Copyright (c) 2025 von Braun Design Center, Inc. Todos os direitos reservados
# -----------------------------------------------------------------------------
# Confidencial - Propriedade do CPA Wernher von Braun
# -----------------------------------------------------------------------------
# Item da verificação:
# NOME DO ARQUIVO: driver.py
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
# Arquivo Driver: 
#----------------------------------------------------------------------------------------------------------------------------

#Instâncias de bibliotecas:
from pyuvm import *                                                   
from .bfm import Bfm

class Driver(uvm_driver):                                              
    """
    O Driver irá definir a ordem de conexão do DUT ao BFM
    """
    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self) # type: ignore
        # Fase de construção (UVM): criar portas/exports/objetos necessários antes da simulação iniciar.
        # cria uma analysis port, chamada "ap", que será usada para enviar os dados para outros componentes do scoreboard.

    def start_of_simulation_phase(self):
        self.bfm = Bfm()
    # Inicia a fase de simulação e aloca o bfm ao monitor.

    async def run_phase(self):
    #Ciclo de operação principal do driver
    #Habitualmente é usado em loop, agardando os itens vindos do sequenciador que serão enviados ao dut via BFM

        while True:
            # Aguarda de forma assíncrona o próximo item da lista do sequenciador,
            # Além disso, o sequenciador irá controlar a ordem dos itens.
            item = await self.seq_item_port.get_next_item()
        
            await self.bfm.send_seq(item)
            # Ele irá enviar o item para o BFM que irá converter os dados em sinais de estimulos no dut.

            self.ap.write(item)
            # Os dados serão escrito no scoreboard para que seja possível observa-lo.

            self.seq_item_port.item_done()
            #Notifica o sequenciador que o processamento do item foi concluído.



            