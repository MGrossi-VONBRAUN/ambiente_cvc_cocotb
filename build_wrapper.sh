#!/bin/bash

# Configurações
SEARCH_DIR="files_synthesis"
OUTPUT_FILE="wrapper.v"

# Verifica se a pasta existe
if [ ! -d "$SEARCH_DIR" ]; then
    echo "Erro: A pasta '$SEARCH_DIR' não foi encontrada no diretório atual."
    exit 1
fi

# Busca automática pelo arquivo .v dentro da pasta
files=("$SEARCH_DIR"/*.v)

# Verifica se encontrou algum arquivo (testa se o primeiro item existe)
if [ ! -e "${files[0]}" ]; then
    echo "Erro: Nenhum arquivo .v encontrado dentro de '$SEARCH_DIR'."
    exit 1
fi

# Seleciona automaticamente o primeiro arquivo encontrado
INPUT_FILE="${files[0]}"

# Aviso se houver múltiplos arquivos
count=$(ls -1 "$SEARCH_DIR"/*.v 2>/dev/null | wc -l)
if [ "$count" -gt 1 ]; then
    echo "Aviso: Múltiplos arquivos .v encontrados. Utilizando: $INPUT_FILE"
else
    echo "Arquivo Verilog detectado: $INPUT_FILE"
fi

echo "Gerando $OUTPUT_FILE..."

# Inicia o Python passando o caminho do arquivo encontrado
# Usamos 'EOF' para o Python para evitar expansão de variáveis do Bash
python3 - "$INPUT_FILE" "$OUTPUT_FILE" <<'EOF'
import sys
import re
import datetime
import os

# Argumentos recebidos do Bash
input_file_path = sys.argv[1]
output_file_name = sys.argv[2]

def parse_verilog(filename):
    try:
        with open(filename, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"Erro ao ler o arquivo {filename}: {e}")
        sys.exit(1)

    # Limpeza de comentários
    content = re.sub(r'//.*', '', content)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    
    # Extrair nome do módulo
    module_match = re.search(r'module\s+(\w+)', content)
    if not module_match:
        print(f'Erro: Nenhum módulo encontrado em {filename}')
        sys.exit(1)
    
    module_name = module_match.group(1)

    # Regex para capturar portas
    port_regex = re.compile(
        r'^\s*(input|output|inout)\s+(?:(\[[^\]]+\])\s+)?([^;]+);', 
        re.MULTILINE | re.DOTALL
    )
    
    ports = []
    
    for match in port_regex.finditer(content):
        p_type = match.group(1)
        p_width = match.group(2) if match.group(2) else ''
        p_names_raw = match.group(3)
        p_names = [n.strip() for n in p_names_raw.split(',')]
        
        for name in p_names:
            if name:
                ports.append({
                    'type': p_type,
                    'width': p_width,
                    'name': name
                })

    return module_name, ports

def generate_wrapper(mod_name, ports, out_file):
    current_date = datetime.date.today().strftime('%Y-%m-%d')
    
    # Cabeçalho atualizado
    header = f"""// +FHDR------------------------------------------------------------------------
// Copyright (c) 2025 von Braun Design Center, Inc. Todos os direitos reservados
// Propriedade Confidencial do Centro de Pesquisas Avancadas Wernher von Braun
// -----------------------------------------------------------------------------
// NOME DO ARQUIVO : wrapper.v (Gerado automaticamente)
// REFERENCIA :
// DEPARTAMENTO : Microeletronica
// DATA GERACAO : {current_date}
// AUTOR : Matheus Grossi
// EMAIL DO AUTOR : matheus.grossi@vonbraunlabs.com.br
// -----------------------------------------------------------------------------
// HISTORICO DAS VERSOES
// VERSAO  DATA         AUTOR              DESCRICAO
// 1.0     {current_date}   grossi              Versao inicial
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
"""
    
    body = ""
    valid_ports = [p for p in ports if p['name'] not in ['VPWR', 'VGND']]
    
    # Declaração dos wires
    for p in valid_ports:
        width_str = p['width'] + " " if p['width'] else ""
        body += f"    wire {width_str}{p['name']};\n"

    body += "\n    //Conexão dos pinos de alimentação:\n"
    body += "    wire VPWR = 1;\n"
    body += "    wire VGND = 0;\n\n"

    # Instância do DUT
    body += f"    {mod_name} dut\n"
    body += "    (\n"
    body += "        //Power pins:\n"
    body += "        .VPWR               (VPWR),\n"
    body += "        .VGND               (VGND),\n\n"
    body += "        //Pin-list:\n"

    for i, p in enumerate(valid_ports):
        comma = "," if i < len(valid_ports) - 1 else ""
        body += f"        .{p['name']:<19} ({p['name']}){comma}\n"
    
    body += "    );\n"

    footer = f"""
    initial begin : Sdf_annotate
        $sdf_annotate("files_synthesis/{mod_name}.sdf", dut);
    end

    initial begin : Dump
        $dumpfile("dump.fst");
        $dumpvars(0, wrapper);
    end

endmodule
"""

    with open(out_file, 'w') as f:
        f.write(header + body + footer)

if __name__ == "__main__":
    mod_name, ports = parse_verilog(input_file_path)
    generate_wrapper(mod_name, ports, output_file_name)
    print(f"Sucesso! Wrapper gerado em '{output_file_name}'")

EOF

# Verificação de status do Python
if [ $? -eq 0 ]; then
    # Sucesso
    clear
    cat <<'ART_EOF'
 ______________________________________
/                                      \
| >>> Wrapper criado com sucesso!      |
\_________       ______________________/
          \     /
           \   /
               .--.
              |o_o |
              |:_/ |
             //   \ \
            (|     | )
           /'\_   _/`\
           \___)=(___/

ART_EOF
    # Confirmação do local
    echo "Localização: $(pwd)/$OUTPUT_FILE"
else
    # Falha (Python retornou erro)
    clear
    cat <<'ART_EOF'
 ________________________________________
/                                        \
| >>> Falha na geração do wrapper!       |
\_________       ________________________/
          \     /
           \   /
               .--.
              |o_o |
              |:_/ |
             //   \ \
            (|     | )
           /'\_   _/`\
           \___)=(___/

ART_EOF
    exit 1
fi