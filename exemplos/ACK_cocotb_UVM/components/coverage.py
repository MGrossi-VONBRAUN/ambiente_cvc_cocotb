'''
# +FHDR------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Copyright (c) 2025 von Braun Design Center, Inc. Todos os direitos reservados
# -----------------------------------------------------------------------------
# Confidencial - Propriedade do CPA Wernher von Braun
# -----------------------------------------------------------------------------
# Item da verificação:
# NOME DO ARQUIVO: coverage.py
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
# Arquivo Coverage: 
#----------------------------------------------------------------------------------------------------------------------------
#Instâncias de bibliotecas:

from pyuvm import *
from .seq_item import SeqItem
from .defs import g_ack, dt_proc_ctrl, f_saia

CoverageBins = [
    (g_ack.VALIDO, dt_proc_ctrl.VALIDO, f_saia.VALIDO       ), 
    #!rack_mode_test
#-------------------------------------------------------------------------------
    (g_ack.INVALIDO, dt_proc_ctrl.VALIDO, f_saia.VALIDO     ), 
    #!off_mode_test
#-------------------------------------------------------------------------------
    (g_ack.VALIDO, dt_proc_ctrl.INVALIDO, f_saia.INVALIDO   ), 
    #!idle_mode_test
#-------------------------------------------------------------------------------
    (g_ack.VALIDO, dt_proc_ctrl.INVALIDO, f_saia.VALIDO     ), 
    #!rdtx_mode_test
#-------------------------------------------------------------------------------
    (g_ack.VALIDO, dt_proc_ctrl.VALIDO, f_saia.INVALIDO     )  
    #!return_to_idle
]

class Coverage(uvm_subscriber):
    """
    O bloco Covarage é onde fazemos a varredura dos sinais que estamos aplicando 
    afim de obter resultados x ou y em nosso sistema.
    """
    def end_of_elaboration_phase(self):
        self.cvg = set()

    def write(self, item):
        if isinstance(item, SeqItem):
            coverage_bin = (
                item.g_ack,
                item.dt_proc_ctrl,
                item.f_saia
            )
            self.cvg.add(coverage_bin)

    def report_phase(self):
        try:
            disable_errors = ConfigDB().get(self, "", "DISABLE_COVERAGE_ERRORS")
        except UVMConfigItemNotFound:
            disable_errors = False

        if not disable_errors:
            coverage_bins_set = set(CoverageBins)
            missed_bins = coverage_bins_set - self.cvg
            if len(missed_bins) > 0:
                self.logger.error("Functional coverage error!")
                self.logger.error(f"  -> Bins not covered: {missed_bins}")

                assert False
            else:
                self.logger.info("✅ Functional coverage reached all bins.")
                assert True

