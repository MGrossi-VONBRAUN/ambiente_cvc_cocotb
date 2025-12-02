'''
# +FHDR------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Copyright (c) 2025 von Braun Design Center, Inc. Todos os direitos reservados
# -----------------------------------------------------------------------------
# Confidencial - Propriedade do CPA Wernher von Braun
# -----------------------------------------------------------------------------
# Item da verificação:
# NOME DO ARQUIVO: env.py
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
# Arquivo Env: 
#----------------------------------------------------------------------------------------------------------------------------
#Instâncias de bibliotecas:
from pyuvm import *
from .agent import Agent
from .Scoreboard import Scoreboard
from .coverage import Coverage

class Env(uvm_env): # type: ignore
# Classe de ambiente de mais alto nível (top-level) do testbench UVM.
    
    def build_phase(self):
    # build_phase(): criar (instanciar) os subcomponentes do ambiente.

        self.agent = Agent.create("agent", self)
        # Instancia o Agent que irá conter seqr, driver e o monitor.

        self.coverage = Coverage.create("coverage", self)
        # Instancia o coletor da cobertura funcional (Coverage)

        self.scoreboard = Scoreboard.create("scoreboard", self)
        # Instancia o Scoreboard.

    def connect_phase(self):
    # Fase de conexão.

        ConfigDB().set(None, "*", "SEQR", self.agent.seqr) # type: ignore
        # Definimos o SEQR como sequenciador do Agent.

        self.agent.driver_ap.connect(self.scoreboard.cmd_export)
        # Interliga o driver ao Scoreboard (Comandos).

        self.agent.driver_ap.connect(self.coverage.analysis_export)
        # Interliga o driver ao Coverage (Comandos).

        self.agent.monitor_ap.connect(self.scoreboard.result_export)
        # Interliga o monitor ao scoreboard (Resultados).
