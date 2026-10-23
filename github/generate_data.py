import os
import random
from datetime import datetime, timedelta
import pandas as pd
from faker import Faker

# Configurando a reprodutibilidade

fake = Faker('pt_BR')
Faker.seed(42)
random.seed(42)

# Criando a pasta para salvar os dados caso não existam

OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok = True)

# Gerando clientes

NUM_CLIENTES = 150
segmentos = ['Varejo', 'Atacado', 'Serviços', 'Tecnologia', 'Industria']

clientes = []
for i in range(1,NUM_CLIENTES + 1):
    clientes.append({
        'cliente_id': f"CLI-{i:04d}",
        'nome_empresa': fake.company(),
        'segmento': random.choice(segmentos),
        'limite_credito': round(random.uniform(10000, 200000), 2),
        'data_cadastro': fake.date_between(start_date = '-2y', end_date = '-1y')
    })

df_clientes = pd.DataFrame(clientes)
df_clientes.to_csv(f"{OUTPUT_DIR}/clientes.csv", index=False)
print(f"✓ {NUM_CLIENTES} clientes gerados com sucesso.")


# 2. GERAR FATURAS / TÍTULOS DE COBRANÇA


NUM_FATURAS = 1200
faturas = []
DATA_INICIAL = datetime(2025, 1, 1)
DATA_ATUAL = datetime(2026, 10, 1)

for i in range(1, NUM_FATURAS + 1):
    cliente = df_clientes.sample(1).iloc[0]
    
    # Data de emissão aleatória entre início de 2025 e hoje
    data_emissao = fake.date_between(start_date=DATA_INICIAL, end_date=DATA_ATUAL)
    prazos_vencimento = [15, 30, 45, 60, 90]
    prazo = random.choice(prazos_vencimento)
    data_vencimento = data_emissao + timedelta(days=prazo)
    
    valor_fatura = round(random.uniform(500, min(cliente['limite_credito'] * 0.3, 25000)), 2)
    
    faturas.append({
        'fatura_id': f"FAT-{i:05d}",
        'cliente_id': cliente['cliente_id'],
        'data_emissao': data_emissao,
        'data_vencimento': data_vencimento,
        'valor_fatura': valor_fatura
    })

df_faturas = pd.DataFrame(faturas)
df_faturas.to_csv(f"{OUTPUT_DIR}/faturas.csv", index=False)
print(f"✓ {NUM_FATURAS} faturas geradas com sucesso.")


# 3. GERAR PAGAMENTOS (Com comportamentos realistas)


pagamentos = []
pagamento_id_counter = 1

for _, fatura in df_faturas.iterrows():
    vencimento = datetime.combine(fatura['data_vencimento'], datetime.min.time())
    emissao = datetime.combine(fatura['data_emissao'], datetime.min.time())
    
    # Se a fatura ainda não venceu em relação à data do sistema
    if vencimento > DATA_ATUAL:
        # 80% de chance de ainda estar em aberto, 20% de antecipação
        if random.random() < 0.8:
            continue
        else:
            dias_pago = random.randint(0, (vencimento - emissao).days)
            data_pagamento = emissao + timedelta(days=dias_pago)
            status_comportamento = 'antecipado'
    else:
        # Faturas já vencidas no tempo
        sorteio = random.random()
        if sorteio < 0.70:
            # 70% pago em dia ou com pequeno atraso (até 5 dias)
            dias_atraso = random.randint(-5, 5)
            data_pagamento = vencimento + timedelta(days=dias_atraso)
            status_comportamento = 'em_dia'
        elif sorteio < 0.88:
            # 18% pago com atraso moderado (6 a 60 dias)
            dias_atraso = random.randint(6, 60)
            data_pagamento = vencimento + timedelta(days=dias_atraso)
            status_comportamento = 'atrasado'
        else:
            # 12% Inadimplente / Não pago (não gera registro de pagamento)
            continue
    
    # Se a data de pagamento simulada for no futuro em relação a hoje, ignoramos (continua em aberto)
    if data_pagamento > DATA_ATUAL:
        continue

    # Juros se pagou com atraso significativo
    dias_efetivos_atraso = (data_pagamento - vencimento).days
    juros_multa = 0.0
    if dias_efetivos_atraso > 0:
        juros_multa = round(fatura['valor_fatura'] * (0.02 + 0.001 * dias_efetivos_atraso), 2)

    pagamentos.append({
        'pagamento_id': f"PAG-{pagamento_id_counter:05d}",
        'fatura_id': fatura['fatura_id'],
        'data_pagamento': data_pagamento.date(),
        'valor_pago': fatura['valor_fatura'],
        'juros_multa': juros_multa
    })
    pagamento_id_counter += 1

df_pagamentos = pd.DataFrame(pagamentos)
df_pagamentos.to_csv(f"{OUTPUT_DIR}/pagamentos.csv", index=False)
print(f"✓ {len(df_pagamentos)} registros de pagamentos gerados com sucesso.")
print(f"\nArquivos salvos no diretório '{OUTPUT_DIR}/': clientes.csv, faturas.csv, pagamentos.csv")