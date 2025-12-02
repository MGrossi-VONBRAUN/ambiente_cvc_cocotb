'''
# +FHDR------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Copyright (c) 2025 von Braun Design Center, Inc. Todos os direitos reservados
# -----------------------------------------------------------------------------
# Confidencial - Propriedade do CPA Wernher von Braun
# -----------------------------------------------------------------------------
# Item da verificação:
# NOME DO ARQUIVO: monitor.py
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
# Arquivo Monitor: 
#----------------------------------------------------------------------------------------------------------------------------

#Instâncias de bibliotecas:
from pyuvm import *                                                   
from .bfm import Bfm

class Monitor(uvm_component):                                                           # type: ignore
    #Função responsável por monitorar os dados na transmissão.

    def __init__(self, name, parent):
        #Inicializa o componente UVM com nome e hierarquia do testbench.
        super().__init__(name, parent)

    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)                                         # type: ignore
        self.bfm = Bfm()

    async def run_phase(self):
        #Inicializa a função de monitoramento no BFM.

        self.bfm.logger = self.logger 
        #Esse comando reaproveita o logger do monitor no BFM.

        await self.bfm.monitor_outputs(self.ap) 
        #Com isso o BFM irá começar a observar as saídas do DUT e enviar ao ap
        #Esse comando roda em loop, aguardando por variações nos estados.

