#!/usr/bin/env bash
# cocotb_env.sh
# Bootstrap mínimo (SEM WRAPPER, SEM editar Makefile existente)
# Garante python3.10 no sistema, cria cocotb_env usando python3.10, instala cocotb==1.9.2, pytest e pyuvm.
# Também cria automaticamente o arquivo Makefile.cvc_cocotb no diretório de trabalho.
#
# Uso:
#   chmod +x cocotb_env.sh
#   ./cocotb_env.sh
#
set -euo pipefail

PROJECT_DIR="$(pwd)"
VENV_DIR="${PROJECT_DIR}/cocotb_env"
MAKEFILE_OUT="${PROJECT_DIR}/Makefile.cvc_cocotb"

echo
echo "=== cocotb_env.sh iniciado em: ${PROJECT_DIR} ==="
echo

# 1) Garantir pacotes necessários: python3.10 e virtualenv
echo "Passo 1: verificando python3.10 e virtualenv (pode exigir sudo)"
MISSING_PKGS=()

if ! command -v python3.10 >/dev/null 2>&1; then
  echo "python3.10 não encontrado. Será instalado via apt."
  MISSING_PKGS+=("python3.10" "python3.10-venv" "python3.10-dev")
else
  echo "python3.10 encontrado: $(command -v python3.10)"
fi

if ! command -v virtualenv >/dev/null 2>&1; then
  echo "virtualenv não encontrado. Será instalado python3-virtualenv."
  MISSING_PKGS+=("python3-virtualenv")
else
  echo "virtualenv encontrado: $(command -v virtualenv)"
fi

if [ "${#MISSING_PKGS[@]}" -ne 0 ]; then
  echo "Atualizando apt e instalando: ${MISSING_PKGS[*]}"
  sudo apt update
  sudo apt install -y "${MISSING_PKGS[@]}"
fi

if ! command -v python3.10 >/dev/null 2>&1; then
  echo "ERRO: python3.10 ainda indisponível após tentativa de instalação."
  echo "Instale manualmente: sudo apt install python3.10 python3.10-venv"
  exit 1
fi

# 2) Criar ambiente virtual
echo
echo "Passo 2: criando ambiente virtual em '${VENV_DIR}' usando python3.10"
if [ -d "${VENV_DIR}" ]; then
  echo "Aviso: ${VENV_DIR} já existe. Será movido para ${VENV_DIR}.old.$$"
  mv "${VENV_DIR}" "${VENV_DIR}.old.$$"
fi

virtualenv -p python3.10 "${VENV_DIR}"
echo "Ambiente virtual criado: ${VENV_DIR}"

# 3) Instalar cocotb 1.9.2 no ambiente
echo
echo "Passo 3: instalando cocotb==1.9.2"
"${VENV_DIR}/bin/pip" install --upgrade pip setuptools wheel
"${VENV_DIR}/bin/pip" install --no-cache-dir "cocotb==1.9.2"

# 4) Instalar pytest
echo
echo "Passo 4: instalando pytest (recomendado — melhora relatórios de erro do cocotb)"
"${VENV_DIR}/bin/pip" install --no-cache-dir pytest

# 5) Instalar pyuvm (NOVO)
echo
echo "Passo 5: instalando pyuvm (UVM for Python)"
"${VENV_DIR}/bin/pip" install --no-cache-dir pyuvm

# 6) Verificação rápida
echo
echo "Passo 6: verificação rápida"
echo "Python dentro do ambiente virtual:"
"${VENV_DIR}/bin/python" -c 'import sys; print(sys.executable)'
"${VENV_DIR}/bin/python" --version || true

echo "Local do cocotb:"
"${VENV_DIR}/bin/python" -c 'import cocotb, os; print(os.path.dirname(cocotb.__file__))' || true

echo "Versão do pytest:"
"${VENV_DIR}/bin/pytest" --version || true

echo "Versão do pyuvm:"
"${VENV_DIR}/bin/python" -c 'import pyuvm; print(f"pyuvm instalado: {pyuvm.__file__}")' || echo "ERRO: pyuvm não encontrado"

# 7) Criar arquivo Makefile.cvc_cocotb automático
echo
echo "Passo 7: criando Makefile.cvc_cocotb em ${MAKEFILE_OUT}"

cat > "${MAKEFILE_OUT}" << 'EOF'
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

echo
echo "=== CONCLUÍDO ==="
echo "Ambiente virtual criado em: ${VENV_DIR}"
echo
cat <<EOF
Próximos passos:
 1) Ative o ambiente:
      source "${VENV_DIR}/bin/activate"

 2) Rode sua simulação com:
      make -f Makefile.cvc_cocotb

Observações:
 - Este script NÃO edita makefiles existentes.
 - pytest e pyuvm agora estão instalados no venv.
EOF

clear

	cat <<'EOF'
  _______________________________________________________________________
 /                                                                       \
 | >>> Ambiente virtual Cocotb + PyUVM + cvc64 criado com sucesso!       |
 | >>> Para ativar use: source cocotb_env/bin/activate                   |
 |                                                                       |
 | >>> Em sua pasta de projeto foi criado o Makefile.cvc_cocotb          |
 | >>> Já existe as definições para uso com sky130 e sdf caso queira     |
 | >>> Não se esqueça de ajustar os nomes conforme seu projeto           | 
 \_______________________________________________________________________/
          \
           \
                .--.
               |o_o |
               |:_/ |
              //   \ \
             (|     | )
            /'\_   _/`\
            \___)=(___/

EOF
exit 0