Estudo feito por Matheus Grossi, quaisquer dúvidas, correções/sugestões, estarei aqui para o que necessário!

# Ambiente de Verificação Digital (Cocotb + CVC + Sky130 + SDF)

Este repositório contém a estrutura para configurar um ambiente de verificação funcional e pós-síntese (GLS - Gate Level Simulation) utilizando **Cocotb**, **PyUVM** e o simulador **CVC**.

O fluxo foi projetado para facilitar a integração com netlists gerados para a tecnologia **SkyWater 130nm**, automatizando a criação de *wrappers* de simulação e a configuração do Makefile.

--- 
## 📋 Sumário
1. [Estrutura de Diretórios Necessária](#-estrutura-de-diretórios-necessária)
2. [Scripts de Automação](#-scripts-de-automação)
3. [Exemplo de diretório pós-script](#exemplo-de-diretório-pós-script)
4. [Exemplo do wrapper do ACK_pav2 gerado pelo script](#exemplo-do-wrapper-do-ack_pav2-gerado-pelo-script)
5. [Instalação do Compilador CVC](#instalação-do-compilador-cvc)
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
```
---
Após sua execução, será gerado o wrapper na pasta raiz do projeto em uma estrutura como a do exemplo abaixo:

## Exemplo de diretório pós-script:
```bash
├── build_wrapper.sh 
├── files_synthesis
│   ├── design.sdf
│   └── design.v
├── gen_cocotb_env.sh
├── Makefile.cvc_cocotb
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
├── README.md
└── wrapper.v
```

## Exemplo do wrapper do ACK_pav2 gerado pelo script:
---
Sua estrutura interna será composta por algo como:
```bash
// +FHDR------------------------------------------------------------------------
// Copyright (c) 2025 von Braun Design Center, Inc. Todos os direitos reservados
// Propriedade Confidencial do Centro de Pesquisas Avancadas Wernher von Braun
// -----------------------------------------------------------------------------
// NOME DO ARQUIVO : wrapper.v (Gerado automaticamente)
// REFERENCIA :
// DEPARTAMENTO : Microeletronica
// DATA GERACAO : 2025-12-02
// AUTOR : Matheus Grossi
// EMAIL DO AUTOR : matheus.grossi@vonbraunlabs.com.br
// -----------------------------------------------------------------------------
// HISTORICO DAS VERSOES
// VERSAO  DATA         AUTOR              DESCRICAO
// 1.0     2025-12-02   grossi              Versao inicial
// -----------------------------------------------------------------------------
// PROPOSITO : Atuar como interface de acoplamento do cocotb + cvc ao dut
// -FHDR------------------------------------------------------------------------

`timescale 1ns / 1ps
`include "primitives_hd.v"
`include "primitives_hvl.v"
`include "sky130_fd_io.v"
`include "sky130_fd_sc_hd.v"
`include "sky130_fd_sc_hvl.v"
`include "sky130_ef_sc_hd__decap_12.v"

module wrapper;
    wire clk_i;
    wire dft_tm_i;
    wire dt_ack_done_o;
    wire dt_ack_o;
    wire dt_proc_ctrl_i;
    wire f_saia_i;
    wire g_ack_i;
    wire nvm_ack_rd_stb_o;
    wire r_ack_o;
    wire [8:0] nvm_ack_addr_o;
    wire [15:0] nvm_rd_dt_i;

    //Conexão dos pinos de alimentação:
    wire VPWR = 1;
    wire VGND = 0;

    ack_pav2 dut
    (
        //Power pins:
        .VPWR               (VPWR),
        .VGND               (VGND),

        //Pin-list:
        .clk_i               (clk_i),
        .dft_tm_i            (dft_tm_i),
        .dt_ack_done_o       (dt_ack_done_o),
        .dt_ack_o            (dt_ack_o),
        .dt_proc_ctrl_i      (dt_proc_ctrl_i),
        .f_saia_i            (f_saia_i),
        .g_ack_i             (g_ack_i),
        .nvm_ack_rd_stb_o    (nvm_ack_rd_stb_o),
        .r_ack_o             (r_ack_o),
        .nvm_ack_addr_o      (nvm_ack_addr_o),
        .nvm_rd_dt_i         (nvm_rd_dt_i)
    );

    initial begin : Sdf_annotate
        $sdf_annotate("files_synthesis/ack_pav2.sdf", dut);
    end

    initial begin : Dump
        $dumpfile("dump.fst");
        $dumpvars(0, wrapper);
    end

endmodule
```
Neste exemplo foi utilizado o bloco ACK, mas a mesma regra se aplica aos demais, a pin-list sendo declarada inicialmente como wires, os power-pins com seus valores respectivos, a instanciação ao dut e por fim a anotação sdf, seguida do dump.

---
## Instalação do Compilador CVC:

Com o objetivo de evitar dificuldades do usuário, também optei por linkar o compilador cvc neste repositório, não apenas isso, como este possui uma instalação relativamente chata de se fazer, criei um instalador .deb que instala de forma autônoma o compilador no sistema:

Para isso execute o cvc.deb com o comando:

```bash
sudo dpkg -i ./cvc.deb
```
Caso peça algum pacote complementar, rode:

```bash
sudo apt-get install -f
```

 Esta é a forma mais simples para usuários de sistemas baseado em debian/ubuntu, caso utilize uma distro não compatível com o ecossistema o mais adequado é fazer a instalação manual que pode ser obtida pelo link abaixo:

https://github.com/programmable-logic-tools/tachyon-cvc/tree/master

Para a instalação iremos seguir o fluxo de instalação sugerido pelo fórum [Zhuanlan](https://www.google.com/url?q=https://zhuanlan.zhihu.com/p/440026629&sa=D&source=docs&ust=1764698040432303&usg=AOvVaw0Whiu513giaGrC2ItiSXPk):

1º Passo: Entre no diretório da pasta:
```bash
cd open-src-cvc
```
2º Passo: Entre no diretório da pasta chkcvc.src.dir e execute o checkcvc64:
```bash
cd open-src-cvc/chkcvc.src.dir
```
3º Passo: Execute o checkcvc64:
```bash
./checkcvc64
```
Observação importante: O executável checkcvc64 é para sistemas operacionais de 64 bits. Se for um sistema operacional de 32 bits, você precisará gerar um arquivo binário para a verificação antes de executá-la, através dos passos abaixo:
```bash
make -f makefile.lnx
```
4º Passo: E após isso, acionar o executável:
```bash
./checkcvc
```
O programa verificará o ambiente de compilação do sistema e se algumas bibliotecas estão completas. Quando estiver concluído, ele imprimirá:
```bash
System configuration is fine for CVC compilation.
```
Isso indica que o ambiente de compilação está funcionando, caso contrário, você deve verificar se o gcc está totalmente instalado e se alguns arquivos de biblioteca estão instalados.

5º Passo: Precisamos compilar o arquivo make presente na pasta src, para isso, precisamos adentra-la, através do comando:
```bash
cd open-src-cvc/src
```
ou caso esteja fazendo de forma sequencial, o comando abaixo já será suficiente:
```
cd src
```
6º Passo: Efetue a compilação do arquivo make de 64 bits, através do comando abaixo:
```bash
make -f makefile.cvc64
```
Após uma breve espera, o arquivo executável cvc64 será gerado no diretório atual, indicando que a compilação e a instalação foram bem-sucedidas.

7º Passo: Aproveitando que estamos dentro da pasta src, copie o arquivo cvc64 para a pasta bin do sistema, através do comando:
```bash
cp ./cvc64 ../bin/
```
Após isso, iremos adicionar o executável ao path do sistema, através de uma edição simples do arquivo bash.

**Observação importante:** O arquivo bash define os critérios de operação do terminal, e como sabemos o terminal pode ter dois modos de acesso, sendo por usuário comum ou por super usuário (sudo), então esse processo precisa ser feito duas vezes, uma vez em usuário comum e outra em sudo, caso não proceda desse modo, o cvc somente funcionará no perfil de terminal definido, ou seja, caso faça as alterações no bash em usuário comum, posteriormente tentes acessar o cvc em um terminal que esteja em sudo, o terminal irá retornar um erro.

8º Passo: Para isso, é recomendado que crie uma nova janela de terminal e execute o comando à seguir para ir para o diretório base do sistema:
```bash
cd ~/
```
9º Passo: Após isso, abra o arquivo do bash, com o comando à seguir:
```bash
nano ~/.bashrc
```
10º Passo: Após isso, desça até o final do arquivo e adicione o seguinte trecho ao bash:
```bash
export PATH=/home/open-src-cvc/bin:$PATH
```
Observação importante: Caso seu programa esteja em outra pasta, ajuste para o caminho correto. 

11º Passo: Salve o bashrc e feche o terminal. 

Após concluir os passos acima, você poderá executar o cvc diretamente da linha de comando. 

12º Passo: Sendo assim, abra um novo terminal e digite:
```bash
cvc64
```
Se tiver feito tudo corretamente, o terminal lhe retornará esta saída, indicando que a instalação do ambiente foi concluída:
```bash
OSS_CVC_7.00b-x86_64-rhel6x of 07/07/14 (Linux-elf).
Copyright (c) 1991-2014 Tachyon Design Automation Corp.
  All Rights reserved.  Licensed software subject to prohibitions and
  restrictions.  See OSS CVC artistic license included with release.
Today is Wed Dec  1 03:22:49 2021.
**FATAL ERROR** [301] no Verilog input files specified
```
É normal que ocorra  um fatal error, pois nenhum arquivo verilog foi escolhido junto ao comando.

