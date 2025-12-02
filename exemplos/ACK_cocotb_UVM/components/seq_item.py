'''
# +FHDR------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Copyright (c) 2025 von Braun Design Center, Inc. Todos os direitos reservados
# -----------------------------------------------------------------------------
# Confidencial - Propriedade do CPA Wernher von Braun
# -----------------------------------------------------------------------------
# Item da verificação:
# NOME DO ARQUIVO: seq_item.py
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
# Arquivo Seq_item: 
#----------------------------------------------------------------------------------------------------------------------------
#Instâncias de bibliotecas:

from pyuvm import uvm_sequence_item

class SeqItem(uvm_sequence_item):
    """
    Este quem encapsula o envio de dados de modo unitário para o DUT.
    """
    def __init__(self, name, clk, g_ack, dt_proc_ctrl, f_saia):
        super().__init__(name)
        self.clk = clk
        self.g_ack = g_ack
        self.dt_proc_ctrl = dt_proc_ctrl
        self.f_saia = f_saia

    def __str__(self):
        s = (f"clk:          {self.clk:<6} | "
             f"g_ack:        {self.g_ack:<6} | "
             f"dt_proc_ctrl: {self.dt_proc_ctrl:<6} | "
             f"f_saia:       {self.f_saia:<6} | ")
        return s
    

