# Ambiente de Verificação Digital (Cocotb + CVC + Sky130)

Este repositório contém a estrutura para configurar um ambiente de verificação funcional e pós-síntese (GLS - Gate Level Simulation) utilizando **Cocotb**, **PyUVM** e o simulador **CVC**.

O fluxo foi projetado para facilitar a integração com netlists gerados para a tecnologia **SkyWater 130nm**, automatizando a criação de *wrappers* de simulação e a configuração do Makefile.

--- 
## 📋 Sumário
1. [Estrutura de Diretórios Necessária](#-estrutura-de-diretórios-necessária)
2. [Scripts de Automação](#-scripts-de-automação)
3. [Fluxo de Trabalho](#-fluxo-de-trabalho-sugerido)
4. [Limpeza](#-limpeza-do-projeto)
---

## 📂 Estrutura de Diretórios Necessária

Para que os scripts funcionem corretamente e a simulação ocorra sem erros, as seguintes pastas devem estar presentes na raiz do projeto:

### `files_synthesis/`
Esta pasta deve conter os arquivos resultantes do processo de síntese lógica (gerados por ferramentas como OpenLane/Librelane).
* **Netlist (.v)**: O arquivo Verilog estrutural pós-síntese do seu design. O script `build_wrapper.sh` buscará automaticamente o primeiro arquivo `.v` encontrado aqui.
* **Delay File (.sdf)**: (Obrigatório para simulação com timing) Um arquivo *Standard Delay Format* que deve ter o **mesmo nome base** do arquivo `.v` (ex: `design.v` e `design.sdf`). O wrapper gerado incluirá a anotação `$sdf_annotate` apontando para este arquivo.

### `pdk-lib/`
Esta pasta abriga as células da biblioteca SkyWater 130nm corrigidas por Mohammed Shalan e incluídas neste repositório para simplificar a integração. O Makefile gerado inclui este diretório via flag `+incdir+pdk-lib`.
* **Conteúdo**: Arquivos Verilog que descrevem o comportamento das primitivas (ex: `sky130_fd_sc_hd.v`, `primitives_hd.v`).
* **Importância**: Sem esta pasta, o simulador CVC falhará ao tentar instanciar as portas lógicas presentes no netlist.

---

## 🛠 Scripts de Automação

### 1. `gen_cocotb_env.sh`
**Propósito:** Bootstrap do ambiente de simulação e geração do Makefile.

* **Pré-requisitos do Sistema:** Verifica e instala `python3.10`, `venv` e `virtualenv` (pode solicitar senha `sudo` se necessário).
* **Ambiente Virtual:** Cria a pasta `cocotb_env/` e instala:
    * `cocotb` (v1.9.2)
    * `pytest` (para relatórios detalhados)
    * `pyuvm` (Metodologia UVM em Python)
* **Geração de Makefile:** Cria o arquivo `Makefile.cvc_cocotb` configurado para:
    * Usar o simulador **CVC**.
    * Abriga dois modos de compilação, respectivamente com/sem células Sky130, comente com "#" o que não deseja utilizar.
    * E com isso é possível compilar fontes com flags específicas para Sky130 (supressão de warnings, power pins, timing checks).
    * Gerenciar logs e ondas (`.fst`).

**Uso:**
```bash
chmod +x gen_cocotb_env.sh
./gen_cocotb_env.sh