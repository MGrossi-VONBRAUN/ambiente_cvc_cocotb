
`timescale 1ns/1ps
`include "primitives_hd.v"
`include "sky130_fd_sc_hd.v"
`include "sky130_ef_sc_hd__decap_12.v"

module Simple_and_gate_wrapper (
    input A,
    input B,
    output out
);

    //Conexão dos pinos de alimentação:
    wire VPWR = 1;
    wire VGND = 0;

    Simple_and_gate Wrapper (
        .A      (A),
        .B      (B),
        .out    (out),
        .VPWR   (VPWR),
        .VGND   (VGND)
    );

    // Dump setup — must be at time 0
    initial begin
        $sdf_annotate("Simple_and_gate.sdf", Wrapper);
    end
    

    // Setup de dump para ondas
    initial begin
        $dumpfile("dump.fst");
        $dumpvars(0, Simple_and_gate_wrapper);
    end

endmodule