'''
# +FHDR------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Copyright (c) 2025 von Braun Design Center, Inc. Todos os direitos reservados
# -----------------------------------------------------------------------------
# Confidencial - Propriedade do CPA Wernher von Braun
# -----------------------------------------------------------------------------
# Item da verificação:
# NOME DO ARQUIVO: defs.py
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
# Arquivo Defs: 
#----------------------------------------------------------------------------------------------------------------------------
#Instâncias de bibliotecas:

from enum import IntEnum

# Aqui é possível trazer as rotinas.

class g_ack(IntEnum):
    """Estados de operação"""
    VALIDO   = 1           
    INVALIDO = 0                  

class dt_proc_ctrl(IntEnum):
    """Estados de operação"""
    VALIDO   = 1           
    INVALIDO = 0            

class f_saia(IntEnum):
    """Estados de operação"""
    VALIDO   = 1           
    INVALIDO = 0    

