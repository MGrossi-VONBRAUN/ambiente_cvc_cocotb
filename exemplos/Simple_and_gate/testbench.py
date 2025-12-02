import cocotb
from cocotb.triggers import Timer
from cocotb.utils import get_sim_time

# Função auxiliar para imitar o $monitor do Verilog de forma SEGURA
# Usa polling (verificação periódica) ao invés de Edge Triggers para evitar Segfault no CVC
async def monitor_signals_safe(dut):
    print("|====================================|")
    print("|========And-Gate-Truth-Table========|")
    print("|====================================|")
    print("|           |  INPUT(s) ||  OUTPUT(s) |")
    print("|      time |  A  |  B  ||     out    |")
    print("|           +-----+-----||------------|")
    
    # Armazena valores anteriores para detectar mudanças
    last_values = (-1, -1, -1)
    
    while True:
        # Verifica a cada 100ps (alta resolução, mas seguro)
        await Timer(100, units='ps')
        
        try:
            # Leitura segura convertendo para int
            # Se for 'x' ou 'z', o int() falha e vai pro except
            a = int(dut.A.value)
            b = int(dut.B.value)
            out = int(dut.out.value)
            
            current_values = (a, b, out)
            
            # Se houve mudança, imprime
            if current_values != last_values:
                time_ns = get_sim_time(units='ns')
                print(f"{time_ns:>10} |  {a}  |  {b}  ||      {out}     |")
                last_values = current_values
                
        except ValueError:
            # Ignora estados indeterminados (X/Z) durante a inicialização
            pass

@cocotb.test()
async def test_sequence(dut):
    """
    Testbench seguro para CVC + Sky130
    """
       
    # Inicializa entradas para evitar X
    dut.A.value = 0
    dut.B.value = 0
    
    # Inicia o monitor seguro em paralelo
    # Não vamos usar kill(), deixaremos ele rodar até o fim do teste
    cocotb.start_soon(monitor_signals_safe(dut))

    # Sequência de teste (baseada em Timer, super estável)
    # A=0, B=0
    dut.A.value = 0
    dut.B.value = 0
    await Timer(50, units='ns')

    # A=0, B=1
    dut.A.value = 0
    dut.B.value = 1
    await Timer(50, units='ns')

    # A=1, B=0
    dut.A.value = 1
    dut.B.value = 0
    await Timer(50, units='ns')

    # A=1, B=1
    dut.A.value = 1
    dut.B.value = 1
    await Timer(50, units='ns')

    dut._log.info("Fim da simulação")
    # O teste termina aqui automaticamente, o Cocotb encerra as coroutines filhas.
    # Sem o kill() explícito em triggers de borda, o CVC não deve crashar.