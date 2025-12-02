'''
# +FHDR------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Copyright (c) 2025 von Braun Design Center, Inc. Todos os direitos reservados
# -----------------------------------------------------------------------------
# Confidencial - Propriedade do CPA Wernher von Braun
# -----------------------------------------------------------------------------
# Item da verificação:
# NOME DO ARQUIVO: bfm.py
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
# Arquivo Bfm: 
#----------------------------------------------------------------------------------------------------------------------------

#Instâncias de bibliotecas:
import cocotb                                                               # type: ignore
import random                                                               # type: ignore
from cocotb.triggers import Timer, RisingEdge                               # type: ignore
from cocotb.clock import Clock                                              # type: ignore
from pyuvm import *                                                         # type: ignore
from enum import Enum                                                       # type: ignore
from .utils import NVM

class Bfm:
    """
    Modelo Funcional de Barramento (BFM) para o ambiente de verificacao.
    Esta classe lida com todas as interacoes diretas com os sinais do DUT.
    Ela e' implementada para garantir um unico ponto de contato com o DUT.
    """
    _instance = None                                                        # type: ignore

#----------------------------------------------------------------------------
# Ativa o modo Singleton
#----------------------------------------------------------------------------
    def __new__(cls):                                                       # type: ignore
        if cls._instance is None:                                           # type: ignore
            cls._instance = super().__new__(cls)                            # type: ignore
        return cls._instance                                                # type: ignore

#----------------------------------------------------------------------------
#Parametros de inicializacao:
#----------------------------------------------------------------------------
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.dut = cocotb.top
            self.dut.g_ack_i.value = 0                                      # type: ignore
            self.dut.dt_proc_ctrl_i.value = 0                               # type: ignore         
            self.dut.f_saia_i.value = 0                                     # type: ignore
            self.dut.dft_tm_i.value = 0                                     # type: ignore
            self.dut.nvm_rd_dt_i.value = 0                                  # type: ignore

#----------------------------------------------------------------------------
#Campo de inicio das funcoes (tasks):
#---------------------------------------------------------------------------- 

    #----------------------------------------------------------------------------
    #Geracao do clock:
    #----------------------------------------------------------------------------

    async def clock_ack(self, period):
        """Generates the main clock signal for the DUT."""
        self.clk = 1
        while True:
            await cocotb.triggers.Timer(period / 2, units="ns")
            self.clk = not self.clk
            self.dut.clk_i.value = self.clk

    #----------------------------------------------------------------------------
    #Geracao da aleatoriedade dos valores de entrada vindos da memória:
    #----------------------------------------------------------------------------

    #Todos os sinais após a transação devem ir para 0 (nível baixo) [g_ack, dt_proc, f_saia]
    async def send_seq(self, item):
        """Executes a complete transaction sequence."""

        NVM[130] = random.randint(0, 65535) & 0xFFF7
        NVM[131] = random.randint(0, 65535)
        NVM[132] = random.randint(0, 65535)

        await cocotb.triggers.RisingEdge(self.dut.clk_i)
        await cocotb.triggers.RisingEdge(self.dut.clk_i)

        self.dut.g_ack_i.value = item.g_ack            

        await cocotb.triggers.Timer(10, units="ns")
        for _ in range (15): #Repete 15x o aguarde pela borda de clock
            await cocotb.triggers.RisingEdge(self.dut.clk_i)

        self.dut.dt_proc_ctrl_i.value = item.dt_proc_ctrl             

        await cocotb.triggers.Timer(10, units="ns")
        for _ in range (5): #Repete 5x o aguarde pela borda de clock
            await cocotb.triggers.RisingEdge(self.dut.clk_i)

        self.dut.f_saia_i.value = item.f_saia            

        await cocotb.triggers.Timer(10, units="ns")

        for _ in range (30): #Repete 30x o aguarde pela borda de clock
            await cocotb.triggers.RisingEdge(self.dut.clk_i)

        self.dut.dt_proc_ctrl_i.value = 0     

        for _ in range (100): #Repete 100x o aguarde pela borda de clock
            await cocotb.triggers.RisingEdge(self.dut.clk_i)
        self.dut.g_ack_i.value = 0    
        self.dut.f_saia_i.value = 0    
        self.dut.dt_proc_ctrl_i.value = 0     
        await cocotb.triggers.Timer(10, units="ns")
        for _ in range (10): #Repete 10x o aguarde pela borda de clock
            await cocotb.triggers.RisingEdge(self.dut.clk_i)

    #Monitoramento:
    async def monitor_outputs(self, ap): #Monitor quase certo, falta apenas acertar o valor dividido por
        """Collects the decoded data that will be used by Scoreboard."""
        self.checker_data = 0
        self.output_valid = 0

        while True:
            await cocotb.triggers.Edge(self.dut.clk_i) #Aguarda alguma mudança no clock
            await cocotb.triggers.First(cocotb.triggers.RisingEdge(self.dut.g_ack_i), cocotb.triggers.RisingEdge(self.dut.dt_proc_ctrl_i), cocotb.triggers.RisingEdge(self.dut.f_saia_i))

            for _ in range (75):  # executa 75 ciclos ou acha o endereço 083
                if self.dut.nvm_ack_addr_o.value == 131:
                    self.output_valid = 1
                    break
                await cocotb.triggers.RisingEdge(self.dut.clk_i)

            if self.output_valid:
                while self.dut.dt_ack_done_o.value == 0:
                    dt_bit = int(self.dut.dt_ack_o.value)
                    self.checker_data = ((self.checker_data << 1) | dt_bit) & ((1 << 127) - 1)
                    await cocotb.triggers.RisingEdge(self.dut.clk_i)
           
            dt_bit = int(self.dut.dt_ack_o.value)
            self.checker_data = ((self.checker_data << 1) | dt_bit) & ((1 << 127) - 1)

            ap.write(self.checker_data)
            self.checker_data = 0
            self.output_valid = 0










"""
#O ACK não possui reset.
    #-----------------------------------------------------------
    #Funcao de reset:
    #-----------------------------------------------------------    
    
    async def reset(self):
        if self.dut:
            #Personaliza a sequencia de reset
            self.dut.reset_n.value = 0
            await cocotb.triggers.Timer(100, units="ns")
            self.dut.reset_n.value = 1
            await cocotb.triggers.Timer(100, units="ns")
"""