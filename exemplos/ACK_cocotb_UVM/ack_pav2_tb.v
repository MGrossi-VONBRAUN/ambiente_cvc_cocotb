// +FHDR------------------------------------------------------------------------
// Copyright (c) 2025 von Braun Design Center, Inc. Todos os direitos reservados
// Propriedade Confidencial do Centro de Pesquisas Avancadas Wernher von Braun
// -----------------------------------------------------------------------------
// NOME DO ARQUIVO : ack_pav2_tb_wrapper.v
// REFERENCIA :
// DEPARTAMENTO : Microeletronica
// AUTOR : Matheus Grossi
// EMAIL DO AUTOR : matheus.grossi@vonbraunlabs.com.br
// -----------------------------------------------------------------------------
// HISTORICO DAS VERSOES
// VERSAO  DATA         AUTOR              DESCRICAO
// 1.0     2025-05-08   grossi              Versao inicial
// -----------------------------------------------------------------------------
// PALAVRAS-CHAVE :
// -----------------------------------------------------------------------------
// PROPOSITO : Atuar como interface de acoplamento do cocotb ao dut
// -FHDR------------------------------------------------------------------------

`timescale 1ns / 1ps
`include "primitives_hd.v"
`include "sky130_fd_sc_hd.v"
`include "sky130_ef_sc_hd__decap_12.v"

module ack_pav2_tb;

        //Inputs
        reg clk_i;
        reg dft_tm_i;
        reg dt_proc_ctrl_i;
        reg f_saia_i;
        reg g_ack_i;
        reg [15:0] nvm_rd_dt_i;

        //Outputs:
        wire nvm_ack_rd_stb_o;
        wire r_ack_o;
        wire dt_ack_done_o;
        wire dt_ack_o;
        wire [8:0] nvm_ack_addr_o;

    parameter [15:0] NVM_FIXED = 16'h7B3D;

    localparam integer PERIOD_40K  = 25000;
    localparam integer PERIOD_640K = 1564;
    localparam real PERIOD_320K = 0.5;

/*
    BLF Clock functions:
    Frequencies:
    period: 25000 for 40KHz
    period: 1562  for 640KHz
    period: 3126  for 320KHz
*/

 // ========= BLF Clock functions =========
  // Cada task abaixo dirige clk_i por "cycles" ciclos completos
  // no período especificado.

  task BLF_clk_40k;
    input integer cycles; // número de ciclos
    integer i;
    begin
      for (i = 0; i < cycles; i = i + 1) begin
        clk_i = 1'b0; #(PERIOD_40K/2);
        clk_i = 1'b1; #(PERIOD_40K/2);
      end
    end
  endtask

  task BLF_clk_640k;
    input integer cycles;
    integer i;
    begin
      for (i = 0; i < cycles; i = i + 1) begin
        clk_i = 1'b0; #(PERIOD_640K/2);
        clk_i = 1'b1; #(PERIOD_640K/2);
      end
    end
  endtask

  task BLF_clk_320k;
    input integer cycles;
    integer i;
    begin
      for (i = 0; i < cycles; i = i + 1) begin
        clk_i = 1'b0; #(PERIOD_320K/2);
        clk_i = 1'b1; #(PERIOD_320K/2);
      end
    end
  endtask

  // ========= Utilitário de impressão =========
  task print_header;
    begin
      $display(" time | dft_tm dt_proc f_saia g_ack || nvm_ack_rd_stb r_ack dt_ack_done dt_ack | nvm_ack_addr");
      $display("------+--------------------------------+-----------------------------------------+--------------");
    end
  endtask

  task print_line;
    begin
      // pequena folga para sinais derivados estabilizarem após a borda
      #10;
      $display("%5t |    %0d       %0d       %0d      %0d ||       %0d            %0d         %0d        %0d |    0x%03h",
               $time, dft_tm_i, dt_proc_ctrl_i, f_saia_i, g_ack_i,
               nvm_ack_rd_stb_o, r_ack_o, dt_ack_done_o, dt_ack_o, nvm_ack_addr_o);
    end
  endtask

  // ========= Varredura das combinações =========
  task run_truth_table_once;
    input integer which_clk; // 0=40k, 1=640k, 2=320k
    integer i;
    begin
      case (which_clk)
        0: begin
             $display("\n=== Rodada 1: Clock 40 kHz (PERIOD=%0d) ===", PERIOD_40K);
             print_header();
             for (i = 0; i < 16; i = i + 1) begin
               dft_tm_i       = (i >> 3) & 1;
               dt_proc_ctrl_i = (i >> 2) & 1;
               f_saia_i       = (i >> 1) & 1;
               g_ack_i        = (i >> 0) & 1;
               // Gera 1 ciclo completo e registra após a borda de subida
               clk_i = 1'b0; #(PERIOD_40K/2); clk_i = 1'b1;
               print_line();
               #(PERIOD_40K/2);
             end
           end
        1: begin
             $display("\n=== Rodada 2: Clock 640 kHz (PERIOD=%0d) ===", PERIOD_640K);
             print_header();
             for (i = 0; i < 16; i = i + 1) begin
               dft_tm_i       = (i >> 3) & 1;
               dt_proc_ctrl_i = (i >> 2) & 1;
               f_saia_i       = (i >> 1) & 1;
               g_ack_i        = (i >> 0) & 1;
               clk_i = 1'b0; #(PERIOD_640K/2); clk_i = 1'b1;
               print_line();
               #(PERIOD_640K/2);
             end
           end
        2: begin
             $display("\n=== Rodada 3: Clock 320 kHz (PERIOD=%0d) ===", PERIOD_320K);
             print_header();
             for (i = 0; i < 16; i = i + 1) begin
               dft_tm_i       = (i >> 3) & 1;
               dt_proc_ctrl_i = (i >> 2) & 1;
               f_saia_i       = (i >> 1) & 1;
               g_ack_i        = (i >> 0) & 1;
               clk_i = 1'b0; #(PERIOD_320K/2); clk_i = 1'b1;
               print_line();
               #(PERIOD_320K/2);
             end
           end
      endcase
      // Alguns ciclos extras no final dessa rodada
      clk_i = 1'b0;
    end
  endtask

  // ========= Estímulos =========
    initial begin
    // Defaults
    clk_i          = 1'b0;
    dft_tm_i       = 1'b0;
    dt_proc_ctrl_i = 1'b0;
    f_saia_i       = 1'b0;
    g_ack_i        = 1'b0;
    nvm_rd_dt_i    = NVM_FIXED;

    // 3 repetições: uma por clock
    run_truth_table_once(0); // 40 kHz
    run_truth_table_once(1); // 640 kHz
    run_truth_table_once(2); // 320 kHz

    // Finaliza
    repeat (5) @(posedge clk_i);

    #10;
    $finish;

    end

    initial begin
        $dumpfile("dump.fst");
        $dumpvars(0, dut);
    end

    // Anotação SDF (habilitada por define)
    initial begin
        // Ajuste o caminho se precisar
        $sdf_annotate("ack_pav2.sdf", dut);
    end

endmodule