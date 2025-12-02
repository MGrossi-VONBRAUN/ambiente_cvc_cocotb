# Ambiente de Verificação Digital (Cocotb + CVC + Sky130 + SDF)

Este repositório contém a estrutura para configurar um ambiente de verificação funcional e pós-síntese (GLS - Gate Level Simulation) utilizando **Cocotb**, **PyUVM** e o simulador **CVC**.

O fluxo foi projetado para facilitar a integração com netlists gerados para a tecnologia **SkyWater 130nm**, automatizando a criação de *wrappers* de simulação e a configuração do Makefile.

--- 
## 📋 Sumário
1. [Estrutura de Diretórios Necessária](#-estrutura-de-diretórios-necessária)
2. [Scripts de Automação](#-scripts-de-automação)
---

## 📂 Estrutura de Diretórios Necessária

Para que os scripts funcionem corretamente e a simulação ocorra sem erros, as seguintes pastas devem estar presentes na raiz do projeto:

```bash
├── build_wrapper.sh 
├── files_synthesis
│   ├── design.sdf
│   └── design.v
├── gen_cocotb_env.sh
├── pdk-lib
│   ├── primitives_hd.v
│   ├── primitives_hvl.v
│   ├── primitives.v
│   ├── sky130_ef_io__analog_pad.v
│   ├── sky130_ef_io__gpiov2_pad_wrapped.v
│   ├── sky130_ef_io.v
│   ├── sky130_ef_sc_hd__decap_12.v
│   ├── sky130_fd_io.v
│   ├── sky130_fd_sc_hd.v
│   ├── sky130_fd_sc_hvl.v
│   └── sky130_sram_2kbyte_1rw1r_32x512_8.v
└── README.md
```

### `files_synthesis/`
Esta pasta deve conter os arquivos resultantes do processo de síntese lógica (gerados por ferramentas como OpenLane/Librelane).

A título de exemplo carreguei o repositório com o arquivo .v e o .sdf para entendimento, substitua para seu caso.
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

---
**Uso do script:**
```bash
chmod +x gen_cocotb_env.sh
./gen_cocotb_env.sh
```

Para ativar o ambiente virtual criado com as configurações acima utilize o comando:

```bash
source cocotb_env/bin/activate
```

---

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

Lembrando que o Makefile criado não possui o nome padrão portanto para executa-lo, uma medida simples de segurança para que, caso o indivíduo já possua outro makefile no mesmo diretório não seja sobreescrito, para utiliza-lo há dois caminhos:
> 1. Renomear o arquivo para o nome Makefile;
> 2. Executar através do comando: 
```bash
make -f Makefile.cvc_cocotb
```

Após o make ser feito será feita a simulação do wrapper instânciando a célula sdf que está na pasta files_synthesis em conjunto com o Cocotb + PyUVM, na pasta final_results serão gravados os logs com os resultados, sendo divididos em cvc_compile.log e cocotb_status.log, caso tudo ocorra bem, também será gerado o dump.fst na mesma pasta.

Caso queira executar uma compilação limpa, apagando assim os logs e fst anteriores há dois possíveis caminhos:

> 1. Se tiver renomeado o Makefile, rode:
```bash
make clean
make
```

> 2. Senão rode: 
```bash
make -f Makefile.cvc_cocotb clean
make -f Makefile.cvc_cocotb
```

### 2. `build_wrapper.sh`
**Propósito:** Script responsável por criar a interface de conexão (wrapper) entre o arquivo estrutural e o simulador cvc, para isso, ele faz a leitura do arquivo .v presente na pasta files_synthesis e cria o wrapper.v à partir das regras descritas internas ao sh.

**Uso:**
```bash
chmod +x build_wrapper.sh
./build_wrapper.sh