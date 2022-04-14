from myhdl import *

@block
def divider(
    aclk, 
    s_axis_divisor_tvalid, 
    s_axis_divisor_tdata,
    s_axis_dividend_tvalid,      
    s_axis_dividend_tdata,
    m_axis_dout_tvalid,      
    m_axis_dout_tdata,
):
   
    C_FULL_LENGTH = len(m_axis_dout_tdata)
    d             = []
    n             = []
    q             = []
    v             = []
    for i in range(C_FULL_LENGTH):
        d.append(Signal(modbv(0)[len(s_axis_divisor_tdata):]))
        n.append(Signal(modbv(0)[C_FULL_LENGTH:]))
        q.append(Signal(modbv(0)[C_FULL_LENGTH:]))
        v.append(Signal(bool(0)))
    
    @always(aclk.posedge)
    def regDivisor():
        if 1 == s_axis_divisor_tvalid:
            d[0].next = s_axis_divisor_tdata
        else:
            d[0].next = 0
        q[0].next = 0
        v[0].next = s_axis_divisor_tvalid or s_axis_dividend_tvalid
        
        if (s_axis_dividend_tdata >> len(s_axis_dividend_tdata)-1) >= s_axis_divisor_tdata and not 0 == s_axis_divisor_tdata:
            n[0].next = (s_axis_dividend_tdata - (s_axis_divisor_tdata << 15)) << len(s_axis_divisor_tdata)
            q[0].next = 1
        else:
            n[0].next = s_axis_dividend_tdata << len(s_axis_divisor_tdata)
        
        for i in range(len(d)-1):
            d[i+1].next = d[i]
            n[i+1].next = n[i]
            q[i+1].next = q[i] << 1
            v[i+1].next = v[i]
            
            if (n[i] >> (C_FULL_LENGTH-2-i)) >= d[i]:
                n[i+1].next = (n[i] - (d[i] << (C_FULL_LENGTH-2-i)))
                q[i+1].next = (q[i] << 1) | 1 
    
    @always_comb
    def assign_output():
        m_axis_dout_tvalid.next = v[len(v)-1]
        m_axis_dout_tdata.next = q[len(q)-1]

    return regDivisor, assign_output
