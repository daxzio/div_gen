This is a proof of concept to create a BFM equivalent divider like that which is created in the vivado IP generation.

## Install myhdl

    pip install myhdl
    
## To run myhdl simulation

    python tb_divider.py
    
This test also generates a divider example in both vhdl and verilog
    
## View results in GTKWave

    gtkwave tb_divider.vcd
    
## VHDL testbenchs

There is a basic testbench written for vhdl, which can be used in vivado/modelsim simulators etc:

    tb_divider.vhd

The two tests are self checking, but the 2 results that come out, with the valid asserted, should be:

    0x010203
    0x010100
