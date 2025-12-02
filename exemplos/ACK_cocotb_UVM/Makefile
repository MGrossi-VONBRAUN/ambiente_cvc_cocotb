# Makefile
PYTHON := $(abspath cocotb_env/bin/python)
export PATH := $(dir $(PYTHON)):$(PATH)

# --- Capturar toda saída quando o usuário rodar "make" sem argumentos ---
.DEFAULT_GOAL := run_and_log

.PHONY: run_and_log
run_and_log:
	@echo "Running default target and saving full log to cocotb_status.log"
	@$(MAKE) --no-print-directory results.xml 2>&1 | tee cocotb_status.log
# -----------------------------------------------------------------------

# Makefile
PYTHON := $(abspath cocotb_env/bin/python)
export PATH := $(dir $(PYTHON)):$(PATH)

# =======================================================================
# 1. Configuração da Simulação (Definir ANTES do include)
# =======================================================================

# Defina o simulador
SIM = cvc

# Defina a linguagem
TOPLEVEL_LANG = verilog

# Aponte para seu arquivo de teste Python (sem o .py)
# NOTA: O arquivo gerado anteriormente foi test_and_gate.py.
# Se o seu arquivo se chama testbench.py, altere para: MODULE = testbench
MODULE = tests.test_ack
FS = files_synthesis

# O Wrapper é o topo da hierarquia
NETLIST_FILE = ack_pav2
TOPLEVEL = wrapper

# Conexões:
VERILOG_SOURCES = 	\
					$(TOPLEVEL).v \
					$(PWD)/$(FS)/$(NETLIST_FILE).v

# Argumentos de compilação para uso sem células:
#COMPILE_ARGS += \
				-sv \
				+acc+4 \
				+interp \
				+verbose \
				+large \
				+parallel2=on \
				-l cvc_compile.log

# Argumentos de compilação para uso com células sky130 com/sem sdf:
COMPILE_ARGS += \
				+acc+4 +incdir+pdk-lib \
				+define+FUNCTIONAL \
				+define+UNIT_DELAY \
				+define+USE_POWER_PINS \
				+informs +verbose \
				+typdelays \
				-l cvc_compile.log \
				+suppress_warns+679 \
				+suppress_warns+531 \
				+suppress_warns+597 \
				+suppress_warns+653 \
				+suppress_warns+555 \
				+suppress_warns+678 \
				+suppress_warns+3106 \
				+suppress_warns+3153 \
				+suppress_warns+3154 \
				+suppress_warns+3155
				+parallel2=on \
				+large 

# Habilita geração de ondas
export WAVES = 1

# =======================================================================
# 2. Inclusão das Regras do Cocotb
# =======================================================================
include $(shell cocotb-config --makefiles)/Makefile.sim

# =======================================================================
# 3. Alvos Customizados e Pós-Processamento (Definir DEPOIS do include)
# =======================================================================

# Define run_and_log como o alvo padrão explicitamente no final
.DEFAULT_GOAL := run_and_log

.PHONY: run_and_log
run_and_log:
	@echo ">>> 1/3 Iniciando Simulação (logs salvos em cocotb_status.log)..."
	# O pipe para 'tee' só retorna quando o make terminar.
	# O prefixo '-' ignora erros de saída para permitir que o pós-processamento rode.
	-@$(MAKE) --no-print-directory results.xml 2>&1 | tee cocotb_status.log
	
	@echo ">>> 2/3 Simulação finalizada. Iniciando pós-processamento..."
	
	@# Move os logs para a pasta sim_build (se existirem)
	@mv -f cocotb_status.log sim_build/ 2>/dev/null || true
	@mv -f cvc_compile.log sim_build/ 2>/dev/null || true
	@mv -f results.xml sim_build/ 2>/dev/null || true
	@# Move o arquivo de onda para a pasta sim_build
	@mv -f dump.fst sim_build/ 2>/dev/null || true
	
	@echo ">>> 3/3 Organizando diretórios..."
	@# Remove a pasta final_results antiga se existir
	@rm -rf final_results
	
	@# Renomeia sim_build para final_results apenas se sim_build existir
	@[ -d sim_build ] && mv sim_build final_results && echo "Pasta 'sim_build' movida para 'final_results'" \
	|| echo "Aviso: Pasta sim_build não encontrada (simulação falhou antes de criá-la?)"

.PHONY: wave
wave:
	@if [ ! -f final_results/dump.fst ]; then \
		echo "Arquivo final_results/dump.fst não encontrado! Rode 'make' antes."; \
		exit 1; \
	fi
	@echo "Abrindo GTKWave com final_results/dump.fst..."
	surfer final_results/dump.fst &>/dev/null &

clean::
	@# Limpa a tela inicial
	clear
	@# Remove arquivos de simulação e logs
	rm -f *.fst *.vcd
	rm -f netlist.json simv.vvp
	rm -f diagram.dot diagram.svg diagram.png
	rm -f cvcsim comp.log sdf.log cvcsim.log verilog.log results.xml cocotb_status.log cvc_compile.log
	rm -rf final_results sim_build
	
	@# Limpa a tela novamente
	clear
	@echo "   __________________________________ "
	@echo "  /                                  \\"
	@echo " |  >>> Make clean is done            |"
	@echo "  \__________________________________/"
	@echo "            \\ "
	@echo "             \\ "
	@echo "                  .--. "
	@echo "                 |o_o | "
	@echo "                 |:_/ | "
	@echo "                //   \\ \\ "
	@echo "               (|     | ) "
	@echo "              /'\\_   _/\`\\ "
	@echo "              \\___)=(___/ "
	@sleep 0.8
	clear