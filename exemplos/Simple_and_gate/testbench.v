
`timescale 1ns/1ps
`include "primitives_hd.v"
`include "sky130_fd_sc_hd.v"
`include "sky130_ef_sc_hd__decap_12.v"

module testbench;

  // Width param:
  localparam WIDTH   = 8;                
  localparam T_WIDTH = WIDTH - 1;

  // Inputs
  reg A_tb;
  reg B_tb;

  // Output
  wire out_tb;

  //Power Pins:
  wire VPWR=1;
  wire VGND=0;

  // Conect the DUT
  Simple_and_gate DUT (
    .A    (A_tb),
    .B    (B_tb),
    .out  (out_tb),

    //Power Pins:
    .VPWR (VPWR),
    .VGND (VGND)
  );
  
  /*
  // Dump setup — must be at time 0
  initial begin
    $sdf_annotate("Simple_and_gate.sdf", DUT);
  end
  */

  // Simulation sequence
  initial begin
    A_tb = 0; B_tb = 0; #50;
    A_tb = 0; B_tb = 1; #50;
    A_tb = 1; B_tb = 0; #50;
    A_tb = 1; B_tb = 1; #50;
    $finish;
  end

  initial begin
    $display("|====================================|");
    $display("|========And-Gate-Truth-Table========|");
    $display("|====================================|");
    $display("|          |  INPUT(s) ||  OUTPUT(s) |");
    $display("|     time |  A  |  B  ||     out    |");
    $display("|          +-----+-----||------------|");
    $monitor("%10t |  %1d  |  %1d  ||      %1d     |",
               $realtime,  A_tb, B_tb,    out_tb);
  end

  // Dump setup — must be at time 0
  initial begin
    $dumpfile("dump.fst");
    $dumpvars(0, DUT);
  end

endmodule

