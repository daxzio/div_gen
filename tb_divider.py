from myhdl import *
from divider import divider

@block
def tb_divider():
    
    clock       = Signal(bool(0))

    i_valid     = Signal(bool(0))
    i_divisor   = Signal(modbv(0)[8:])
    i_dividend  = Signal(modbv(0)[16:])
    i_validout  = Signal(bool(0))
    i_dataout   = Signal(modbv(0)[24:])
    
    count       = Signal(modbv(0)[8:])

        
    module = divider(clock, i_valid, i_divisor, i_valid, i_dividend, i_validout, i_dataout)

    module.convert(hdl='VHDL')
    module.convert(hdl='Verilog')

    @always(delay(10))
    def clkgen():
        clock.next = not clock

    @always(clock.posedge)
    def stimulus():
        if not count  == 15:
            count.next = count+1
        
        if count == 10:
            i_valid.next    = 1
            i_divisor.next  = 0xfe
            i_dividend.next = 0xffff
        elif count == 11:
            i_valid.next    = 1
            i_divisor.next  = 0xa5
            i_dividend.next = 0xa5a5
        else:
            i_valid.next    = 0
            i_divisor.next  = 0x0
            i_dividend.next = 0x0
   
    return module, clkgen, stimulus


def simulate(timesteps):

    tb = tb_divider()
    tb.config_sim(trace=True)
    tb.run_sim(timesteps)


simulate(2000)
