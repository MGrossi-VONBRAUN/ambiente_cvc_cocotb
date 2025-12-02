'''
# +FHDR------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Copyright (c) 2025 von Braun Design Center, Inc. Todos os direitos reservados
# -----------------------------------------------------------------------------
# Confidencial - Propriedade do CPA Wernher von Braun
# -----------------------------------------------------------------------------
# Item da verificação:
# NOME DO ARQUIVO: seq.py
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
# Arquivo Seq: 
#----------------------------------------------------------------------------------------------------------------------------

#Instâncias de bibliotecas:
from pyuvm import *
from pyuvm import uvm_sequence
from .seq_item import SeqItem
from .coverage import CoverageBins

class ACKCoverageSeq(uvm_sequence):
    """
    Este é responsável por gerenciar e enviar os dados sequenciados.
    """
    async def body(self):
        for g_ack, dt_proc_ctrl, f_saia in CoverageBins:
            clk = ConfigDB().get(None, "", "CLK_PERIOD")
            item = SeqItem(
                name="ack_cov",
                clk=clk, 
                g_ack=g_ack, 
                dt_proc_ctrl=dt_proc_ctrl, 
                f_saia=f_saia
            )
            
            await self.start_item(item)
            await self.finish_item(item)



