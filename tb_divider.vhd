library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.numeric_std.all;
library work;

entity tb_div is
end;

architecture tb of tb_div is

    signal clk       : std_logic                                   := '0';  -- main fpga clk
    signal i_valid0   : std_logic                                   := '0';  -- main fpga clk
    signal i_valid1   : std_logic                                   := '0';  -- main fpga clk
    signal i_divisor  : unsigned(7 downto 0);
    signal i_dividend : unsigned(15 downto 0);
    signal i_quotient : unsigned(23 downto 0);
    signal i_qv       : std_logic;
    
    signal i_index       : integer := 0;

begin

    clk       <= not clk       after 1 ns;
    
    p_gen_inputs : process
    begin
        i_divisor <= x"00";
        i_dividend <= x"0000";
        i_valid0   <= '0';
        i_valid1   <= '0';
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        i_divisor <= x"fe";
        i_dividend <= x"ffff";
        i_valid0   <= '1';
        i_valid1   <= '1';
        wait until rising_edge(clk);
        i_divisor <= x"a5";
        i_dividend <= x"a5a5";
        i_valid0   <= '1';
        i_valid1   <= '1';
        wait until rising_edge(clk);
        i_divisor <= x"00";
        i_dividend <= x"0000";
        i_valid0   <= '0';
        i_valid1   <= '0';
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        wait until rising_edge(clk);
        wait;

    end process;
    
    p_check_read : process
    begin
        if '1' = i_qv then
            if 0 = i_index and x"010203" /= i_quotient then
                report "DOUT MISMATCH!!" severity error;
            elsif 1 = i_index and x"010100" /= i_quotient then
                report "DOUT MISMATCH!!" severity error;
            end if;
            i_index <=  i_index + 1;
        end if;
        wait until rising_edge(clk);
    end process;

    div_gen_chan : entity work.divider
        port map(
            aclk                   => clk,
            s_axis_dividend_tvalid => i_valid0,
            s_axis_dividend_tdata  => i_dividend,
            s_axis_divisor_tvalid  => i_valid1,
            s_axis_divisor_tdata   => i_divisor,
            m_axis_dout_tvalid     => i_qv,
            m_axis_dout_tdata      => i_quotient
            );
end;
