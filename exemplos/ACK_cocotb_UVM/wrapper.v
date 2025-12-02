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
