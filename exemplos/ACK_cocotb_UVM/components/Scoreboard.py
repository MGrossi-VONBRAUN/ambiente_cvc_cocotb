'''
# +FHDR------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Copyright (c) 2025 von Braun Design Center, Inc. Todos os direitos reservados
# -----------------------------------------------------------------------------
# Confidencial - Propriedade do CPA Wernher von Braun
# -----------------------------------------------------------------------------
# Item da verificação:
# NOME DO ARQUIVO: Sc.py
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
# Arquivo Scoreboard: 
#----------------------------------------------------------------------------------------------------------------------------

#Instâncias de bibliotecas:
import cocotb
from .utils import NVM
from pyuvm import *

class Scoreboard(uvm_component):
    """
    Este é o responsável por efetuar a varredura de nossos casos de testes
    e os resultados obtidos e assim confirmar se nosso DUT condiz com o 
    que se tinha como planejamento.
    """
    def build_phase(self):
        self.cmd_fifo = uvm_tlm_analysis_fifo("cmd_fifo", self)
        self.result_fifo = uvm_tlm_analysis_fifo("result_fifo", self)
        self.cmd_get_port = uvm_get_port("cmd_get_port", self)
        self.result_get_port = uvm_get_port("result_get_port", self)
        self.cmd_export = self.cmd_fifo.analysis_export
        self.result_export = self.result_fifo.analysis_export
        self.fail_count = 0

    def connect_phase(self):
        self.cmd_get_port.connect(self.cmd_fifo.get_export)
        self.result_get_port.connect(self.result_fifo.get_export)

    async def run_phase(self):
        while True:
            item = await self.cmd_get_port.get()
            actual_data_ack = await self.result_get_port.get()

            # Converte cada valor em hexadecimal (sem o prefixo '0x', sempre com 4 dígitos)
            hex_130 = format(NVM[130], '04X')
            hex_131 = format(NVM[131], '04X')
            hex_132 = format(NVM[132], '04X')

            # Concatena os hexadecimais
            concat_hex = hex_130 + hex_131 + hex_132
            valor_inteiro = int(concat_hex, 16)

            if (item.g_ack == 0 or item.f_saia == 0):
                valor_inteiro = 0


            if (actual_data_ack == valor_inteiro):
                self.logger.info(f"✅ PASSED: {item}")
            else:
                self.logger.error(f"❌ FAILED: {item}")
                self.logger.error(
                    f"    └─ Expected: {valor_inteiro}\n"
                    f"                                      Got:      {actual_data_ack}"
                )
                self.fail_count += 1
                
                
    def report_phase(self):
        """Prints a final summary of the test results."""
        cocotb.log.info(f"\n+--------------------+")
        cocotb.log.info(f"| Final Fail Count: {self.fail_count:d} |")
        cocotb.log.info(f"+--------------------+")
        if self.fail_count > 0:
            assert False, f"{self.fail_count} failures detected in scoreboard"






















            '''
#Processo de alocação da biblioteca do cocotb.
import cocotb

#Processo de alocação da biblioteca do pyuvm.
from pyuvm import *

class Scoreboard(uvm_component):# type: ignore
# Define a classe 'Scoreboard' que herda de 'uvm_component'.
# Um uvm_component é um bloco de construção estático e reutilizável na hierarquia de verificação.
# A função do scoreboard é comparar os dados esperados com os dados reais obtidos do DUT.

    def build_phase(self):
    # Esta é a 'build_phase' (fase de construção), uma das fases padrão da UVM.
    # Ela é executada no início da simulação para criar os subcomponentes internos.

    # Inicializa o armazenamento do tipo fifo dos dados esperados enviados pelo monitor:
        self.cmd_fifo = uvm_tlm_analysis_fifo("cmd_fifo", self) # type: ignore

    # Inicializa o armazenamento do tipo fifo dos dados reais, vindos do DUT (através do monitor):
        self.result_fifo = uvm_tlm_analysis_fifo("result_fifo", self) # type: ignore
    
    # Este comando irá puxar o próximo item da fila de comandos:
        self.cmd_get_port = uvm_get_port("cmd_get_port", self) # type: ignore

    # Este comando irá puxar o próximo item da fila de resultados:
        self.result_get_port = uvm_get_port("result_get_port", self) # type: ignore
    
    # Através deste comando se forma a estrutura, onde os demais componentes,
    # como o monitor irão enviar os dados esperados:
        self.cmd_export = self.cmd_fifo.analysis_export

    # Através deste comando serão depositados os resultados reais vindos do DUT(através do monitor).
        self.result_export = self.result_fifo.analysis_export

    #Inicializa o Contador de falhas:
        self.fail_count = 0

    def connect_phase(self):
        self.cmd_get_port.connect(self.cmd_fifo.get_export)
        self.result_get_port.connect(self.result_fifo.get_export)

    def check_phase(self):
        while self.result_get_port.can_get():
            _, actual_result = self.result_get_port.try_get()
            cmd_success, cmd = self.cmd_get_port.try_get()
            if not cmd_success:
                self.logger.critical(f"result {actual_result} had no command")
            else:
                (A, B, op_numb) = cmd
                op = Ops(op_numb)# type: ignore
                predicted_result = alu_prediction(A, B, op)# type: ignore
                if predicted_result == actual_result:
                    self.logger.info(f"PASSED: 0x{A:02x} {op.name} 0x{B:02x} ="
                                     f" 0x{actual_result:04x}")
                else:
                    self.logger.error(f"FAILED: 0x{A:02x} {op.name} 0x{B:02x} "
                                      f"= 0x{actual_result:04x} "
                                      f"expected 0x{predicted_result:04x}")

'''
