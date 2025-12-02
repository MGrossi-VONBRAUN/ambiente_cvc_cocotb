'''
# +FHDR------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Copyright (c) 2025 von Braun Design Center, Inc. Todos os direitos reservados
# -----------------------------------------------------------------------------
# Confidencial - Propriedade do CPA Wernher von Braun
# -----------------------------------------------------------------------------
# Item da verificação:
# NOME DO ARQUIVO: test_ack.v
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
# Arquivo test: 
#----------------------------------------------------------------------------------------------------------------------------
#Instâncias de bibliotecas:

import cocotb
import pyuvm
from pyuvm import *

from components.env import Env
from components.bfm import Bfm
from components.seq import ACKCoverageSeq
from components.utils import mem_ctrl


@pyuvm.test()
class ACK_test(uvm_test):
    """
    Este é o bloco responsável por realizar as rotinas de testes.
    """
    def build_phase(self):
        ConfigDB().set(None, "*", "DISABLE_COVERAGE_ERRORS", False)
        self.env = Env.create("env", self)

    def end_of_elaboration_phase(self):
        self.test_seq = ACKCoverageSeq.create("test_seq")

    async def run_phase(self):
        self.raise_objection()
        
        bfm = Bfm()

        corners = [
            {"period": 25000}, #40KHz
            {"period": 1562},  #640KHz
            {"period": 3126}   #320KHz
        ]

        for i, corner in enumerate(corners):
            cocotb.log.info(f"Starting Corner Case {i+1}/{len(corners)}: {corner}")
            clock_task = cocotb.start_soon(bfm.clock_ack(corner["period"])) #modificar a geração de clock depois
            mem_ctrl_task = cocotb.start_soon(mem_ctrl(bfm))
            
            ConfigDB().set(None, "*", "CLK_PERIOD", corner["period"])
            seqr = ConfigDB().get(self, "", "SEQR")
            await self.test_seq.start(seqr)

            await cocotb.triggers.Timer(100000, units="ns")

            clock_task.kill()
            mem_ctrl_task.kill()

        self.drop_objection()