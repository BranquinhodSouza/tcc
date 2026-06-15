"""
Gera dataset sintético de alunos PROEJA IFG Goiânia com distribuições
calibradas pelos dados reais do Anuário Brasileiro da Educação Básica 2025
(Todos pela Educação) e pela literatura sobre EJA/PROEJA.
"""
import csv, random, math
random.seed(42)

N = 500

nomes_m = ["João","Carlos","Paulo","Rafael","Fernando","Lucas","Diego","Rodrigo","Eduardo","Gustavo",
           "Thiago","Leonardo","Fábio","Marcos","Gabriel","Daniel","Hugo","Vinicius","Francisco","Felipe"]
nomes_f = ["Maria","Ana","Lúcia","Juliana","Patrícia","Amanda","Larissa","Michele","Camila","Vanessa",
           "Andréia","Tatiane","Renata","Priscila","Simone","Aline","Cristiane","Adriana","Fernanda","Eliane"]
sobrenomes = ["Silva","Santos","Oliveira","Souza","Lima","Costa","Pereira","Rocha","Alves","Martins",
              "Gomes","Ribeiro","Carvalho","Almeida","Rodrigues","Nascimento","Araújo","Barbosa"]

bairros_perif = ["Vila Nova","Campinas","Jardim América","Finsocial","Jardim Curitiba","Novo Horizonte",
                 "Residencial Itamaracá","Conjunto Vera Cruz","Parque Atheneu","Setor Pedro Ludovico"]
bairros_centro = ["Setor Central","Setor Sul","Setor Oeste","Setor Bueno","Setor Marista",
                  "Setor Universitário","Cidade Jardim","Jardim Goiás"]

rows = []
for i in range(1, N+1):
    # --- SEXO: EJA tem maioria feminina (Pnad 2023) ---
    sexo = random.choices(['M','F'], [0.44, 0.56])[0]

    # --- RAÇA: Anuário 2025 aponta 76,8% pretos/pardos na EJA ---
    raca = random.choices(['Branca','Parda','Preta','Amarela','Indígena'], [0.20,0.50,0.27,0.02,0.01])[0]

    # --- IDADE: perfil PROEJA IFG (Pereira, 2011): 18-40 anos, maioria ---
    r = random.random()
    if r < 0.32: idade = random.randint(18, 22)
    elif r < 0.58: idade = random.randint(23, 30)
    elif r < 0.80: idade = random.randint(31, 40)
    elif r < 0.94: idade = random.randint(41, 50)
    else: idade = random.randint(51, 65)

    # --- RENDA: 76,8% com renda até 1,5 SM (Anuário 2025) ---
    r = random.random()
    if r < 0.35: renda = random.randint(600, 1000)
    elif r < 0.65: renda = random.randint(1001, 1600)
    elif r < 0.85: renda = random.randint(1601, 2200)
    elif r < 0.95: renda = random.randint(2201, 3000)
    else: renda = random.randint(3001, 4500)
    renda = (renda // 10) * 10

    # --- TRABALHO: ~80% dos alunos EJA trabalham (Pnad/EJA) ---
    trabalha = random.choices([1, 0], [0.80, 0.20])[0]

    # --- FILHOS: maioria tem responsabilidades familiares (Arroyo, 2017) ---
    tem_filhos = random.choices([1, 0], [0.58, 0.42])[0]

    # --- CURSO: baseado nos cursos PROEJA do IFG Goiânia ---
    curso = random.choices(['Cozinha','Alimentação','Panificação','Hospedagem'], [0.28,0.37,0.20,0.15])[0]

    # --- INGRESSO: janela 2019-2025 ---
    ano = random.randint(2019, 2025)
    sem = random.choice([1, 2])
    ingresso = f"{ano}.{sem}"

    # --- NOME ---
    no = random.choice(nomes_m if sexo == 'M' else nomes_f)
    so = f"{random.choice(sobrenomes)} {random.choice(sobrenomes)}"
    nome = f"{no} {so}"

    # --- BAIRRO: alunos PROEJA majoritariamente de bairros periféricos (Pereira, 2011) ---
    if random.random() < 0.75:
        bairro = random.choice(bairros_perif)
    else:
        bairro = random.choice(bairros_centro)

    # --- ESCORE DE RISCO (baseado na literatura) ---
    risco = 0.0
    if trabalha: risco += 0.18
    if tem_filhos: risco += 0.12
    if renda < 1200: risco += 0.10
    if idade < 25: risco += 0.10
    if idade > 50: risco += 0.06
    if raca in ['Preta','Parda']: risco += 0.06
    if curso in ['Cozinha']: risco += 0.03
    if bairro in bairros_perif: risco += 0.03
    risco = min(risco, 0.72)
    if ano >= 2024:
        risco *= 0.55

    # --- STATUS (ativo / evadido / formado) ---
    r_ev = random.random()
    if r_ev < risco:
        status = 'Evadido'
        meses = max(1, int(random.expovariate(1/7)))
        if meses > 36: meses = 36
        # --- MOTIVOS: dados da literatura (Oliveira & Carmo, 2021) ---
        mr = random.random()
        if mr < 0.38: motivo = 'Trabalho'
        elif mr < 0.54: motivo = 'Horário Incompatível'
        elif mr < 0.65: motivo = 'Currículo/Metodologia'
        elif mr < 0.74: motivo = 'Problemas de Saúde'
        elif mr < 0.83: motivo = 'Questões Familiares'
        elif mr < 0.90: motivo = 'Falta de Interesse'
        else: motivo = 'Transferência'
    elif r_ev < risco + 0.18:
        status = 'Formado'
        meses = random.randint(36, 48)
        motivo = ''
    else:
        status = 'Ativo'
        meses = random.randint(3, 36)
        motivo = ''

    # --- SEMESTRE DE EVASÃO ---
    if status == 'Evadido':
        total_m = max(6, meses)
        ae = ano + total_m // 12
        se_final = sem + (total_m % 12) // 6
        while se_final > 2:
            se_final -= 2
            ae += 1
        sev = f"{ae}.{se_final}"
    else:
        sev = ''

    rows.append({
        'id_aluno': i, 'nome': nome, 'idade': idade, 'sexo': sexo, 'raca': raca,
        'renda_familiar': renda, 'trabalha': 'Sim' if trabalha else 'Não',
        'bairro': bairro, 'possui_filhos': 'Sim' if tem_filhos else 'Não',
        'curso': curso, 'semestre_ingresso': ingresso, 'semestre_evasao': sev,
        'status': status, 'meses_cursados': meses, 'motivo_evasao': motivo
    })

# Salvar CSV (na pasta data/)
csv_path = 'data/dados_evasao_proeja_ifg.csv'
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)

# Estatísticas
total = N
evadidos = sum(1 for r in rows if r['status'] == 'Evadido')
ativos = sum(1 for r in rows if r['status'] == 'Ativo')
formados = sum(1 for r in rows if r['status'] == 'Formado')
tx_evasao = evadidos / N * 100

print(f"{'='*50}")
print(f"  DATASET SINTÉTICO PROEJA IFG GOIÂNIA")
print(f"{'='*50}")
print(f"  Total de alunos:     {total}")
print(f"  Ativos:              {ativos:>3} ({ativos/N*100:.1f}%)")
print(f"  Evadidos:            {evadidos:>3} ({evadidos/N*100:.1f}%)")
print(f"  Formados:            {formados:>3} ({formados/N*100:.1f}%)")
print(f"  Taxa de evasão:      {tx_evasao:.1f}%")
print(f"{'='*50}")
print(f"  Distribuição racial (alvo Anuário 2025: 76,8% Pretos+Pardos):")
pp = sum(1 for r in rows if r['raca'] in ['Preta','Parda'])
print(f"    Pretos+Pardos: {pp} ({pp/N*100:.1f}%)")
print(f"  Alunos que trabalham:")
tr = sum(1 for r in rows if r['trabalha'] == 'Sim')
print(f"    Trabalham: {tr} ({tr/N*100:.1f}%)")
print(f"{'='*50}")
print(f"  Arquivo salvo: {csv_path}")
