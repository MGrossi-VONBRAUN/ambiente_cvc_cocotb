'''
# +FHDR------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Copyright (c) 2025 von Braun Design Center, Inc. Todos os direitos reservados
# -----------------------------------------------------------------------------
# Confidencial - Propriedade do CPA Wernher von Braun
# -----------------------------------------------------------------------------
# Item da verificação:
# NOME DO ARQUIVO: utils.py
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
# Arquivo Utils: 
#----------------------------------------------------------------------------------------------------------------------------

#Instâncias de bibliotecas:
import cocotb

'''
No Utils é possível alocar gemeos virtuais que irão emular comportamentos de blocos auxiliares,
na verificação do ACK este foi utilizado para virtualizar a memória NVM.
'''
NVM = {
    # RESERVERD
    0x000 :  0,#(AK >> 112) & 0xFFFF, 
    0x001 :  1,#(AK >> 96) & 0xFFFF,
    0x002 :  2,#(AK >> 80) & 0xFFFF,
    0x003 :  3,#(AK >> 64) & 0xFFFF,
    0x004 :  4,#(AK >> 48) & 0xFFFF,
    0x005 :  5,#(AK >> 32) & 0xFFFF,
    0x006 :  6,#(AK >> 16) & 0xFFFF, 
    0x007 :  7,#AK & 0xFFFF,
    #UII
    0x080 :  80,#CRC-16 Activated & 0xFFFF, 
    0x081 :  81,#CRC-16 Disabled & 0xFFFF, Mapped to flip-flops
    0x082 :  82,#PV, BF, TF and (OV >> 8) & 0xFFFF,
    0x083 :  83,#OV, (GID >> 16) & 0xFFFF,
    0x084 :  84,#GID & 0xFFFF,
    #TID
    0x100 :  57985,#CLASSID, (MDID >> 4) & 0xFFFF, 
    0x101 :  36864,#MDID, TMN & 0xFFFF,
    0x102 :  16384,#XTIDHEADER & 0xFFFF,
    0x103 :  103,#(SERIALNUMBER >> 48) & 0xFFFF,
    0x104 :  104,#(SERIALNUMBER >> 32) & 0xFFFF,
    0x105 :  105,#(SERIALNUMBER >> 16) & 0xFFFF,
    0x106 :  106,#SERIALNUMBER & 0xFFFF,
    #N/A
    0x107 :  107,#FLAGSFABRICANTE & 0xFFFF, 
    0x10D :  108,#(AUXEP >> 32) & 0xFFFF,
    0x10E :  109,#(AUXEP >> 16) & 0xFFFF,
    0x10F :  110,#AUXEP & 0xFFFF,
    # USER
    0x180 : 180,#(RFU24 >> 8) & 0xFFFF,     # seleciona os 16 MSB
    0x181 : 181,#((RFU24 & 0xFF)|((OBU_ID40 >> 32))) & 0xFFFF, # seleciona os 8 LSB  de RFU e os 8 MSB de OBU_ID
    0x182 : 182,#(OBU_ID40 >> 16) & 0xFFFF,        # seleciona os 16 bits intermediarios 
    0x183 : 183,#OBU_ID40 & 0xFFFF,        # seleciona os 16 LSB
    0x184 : 184,#(DATA64 >> 48) & 0xFFFF,  # seleciona os 16 MSB
    0x185 : 185,#(DATA64 >> 32) & 0xFFFF,  # seleciona 47:32
    0x186 : 186,#(DATA64 >> 16) & 0xFFFF,  # seleciona 31:16
    0x187 : 187 #DATA64 & 0xFFFF   # seleciona os 16 LSB
}

async def mem_ctrl(self):
    while True:
        await cocotb.triggers.Timer(1, units="ns")
        await cocotb.triggers.RisingEdge(self.dut.nvm_ack_rd_stb_o)
        await cocotb.triggers.Timer(10, units="ns")

        rst_mem_ctrl = 1 #modificar para os sinais que seu bloco usar
        nvm_wr_en_mem_ctrl = 0
        nvm_rd_en_mem_ctrl = self.dut.nvm_ack_rd_stb_o.value
        nvm_addr_mem_ctrl = self.dut.nvm_ack_addr_o.value
        nvm_wr_dt_mem_ctrl = 0

        if rst_mem_ctrl:
            if (nvm_rd_en_mem_ctrl and not nvm_wr_en_mem_ctrl):  # leitura
                self.nvm_busy_mem_ctrl = 1
                #self.dut.nvm_busy_i.value = self.nvm_busy_mem_ctrl
                self.nvm_rd_dt_mem_ctrl = NVM[int(nvm_addr_mem_ctrl)]
                self.dut.nvm_rd_dt_i.value = self.nvm_rd_dt_mem_ctrl  
                await cocotb.triggers.Timer(2000, units="ns")
                self.nvm_busy_mem_ctrl = 0
                #self.dut.nvm_busy_i.value = self.nvm_busy_mem_ctrl
            elif (not nvm_rd_en_mem_ctrl and nvm_wr_en_mem_ctrl):  # escrita
                self.nvm_busy_mem_ctrl = 1
                #self.dut.nvm_busy_i.value = self.nvm_busy_mem_ctrl
                NVM[int(nvm_addr_mem_ctrl)] = int(nvm_wr_dt_mem_ctrl)
                await cocotb.triggers.Timer(4000, units="ns")
                self.nvm_busy_mem_ctrl = 0
                #self.dut.nvm_busy_i.value = self.nvm_busy_mem_ctrl
            else:   # nenhuma operação ou operações concorrentes
                self.nvm_busy_mem_ctrl = 0
                #self.dut.nvm_busy_i.value = self.nvm_busy_mem_ctrl
                self.nvm_rd_dt_mem_ctrl = 0
        else:
            self.nvm_busy_mem_ctrl = 0
            #self.dut.nvm_busy_i.value = self.nvm_busy_mem_ctrl
            self.nvm_rd_dt_mem_ctrl = 0

