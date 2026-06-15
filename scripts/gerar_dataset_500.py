"""
Gera o dataset sintético de 500 alunos para EDA
e salva como CSV para uso no Power BI / Python / HTML
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

# Gerar dados
rows = []
for i in range(1, N+1):
    sexo = random.choices(['M','F'], [0.48, 0.52])[0]
    raca = random.choices(['Branca','Parda','Preta','Amarela','Indígena'], [0.25,0.45,0.22,0.05,0.03])[0]

    # idade ponderada
    r = random.random()
    if r < 0.35: idade = random.randint(18, 24)
    elif r < 0.65: idade = random.randint(25, 34)
    elif r < 0.85: idade = random.randint(35, 44)
    else: idade = random.randint(45, 64)

    # renda
    r = random.random()
    if r < 0.40: renda = random.randint(600, 1000)
    elif r < 0.70: renda = random.randint(1001, 1800)
    elif r < 0.90: renda = random.randint(1801, 2500)
    else: renda = random.randint(2501, 4000)
    renda = (renda // 10) * 10

    trabalha = random.choices([1, 0], [0.82, 0.18])[0]
    filhos = random.choices([1, 0], [0.55, 0.45])[0]

    curso = random.choices(['Cozinha','Alimentação','Panificação','Hospedagem'], [0.30,0.35,0.20,0.15])[0]

    ano = random.randint(2020, 2025)
    sem = random.choice([1, 2])
    ingresso = f"{ano}.{sem}"

    # nome
    no = random.choice(nomes_m if sexo == 'M' else nomes_f)
    so = f"{random.choice(sobrenomes)} {random.choice(sobrenomes)}"
    nome = f"{no} {so}"

    # risco (0 a 1)
    risco = 0.0
    if trabalha: risco += 0.15
    if filhos: risco += 0.12
    if renda < 1200: risco += 0.10
    if idade < 25: risco += 0.08
    if idade > 50: risco += 0.05
    if raca in ['Preta','Parda']: risco += 0.05
    if curso in ['Cozinha']: risco += 0.03
    risco = min(risco, 0.70)
    if ano >= 2024:
        risco *= 0.6

    r_ev = random.random()
    if r_ev < risco:
        status = 'Evadido'
        meses = max(1, int(random.expovariate(1/8)))
        if meses > 36: meses = 36
        mr = random.random()
        if mr < 0.40: motivo = 'Trabalho'
        elif mr < 0.55: motivo = 'Horário Incompatível'
        elif mr < 0.67: motivo = 'Currículo/Metodologia'
        elif mr < 0.76: motivo = 'Problemas de Saúde'
        elif mr < 0.84: motivo = 'Questões Familiares'
        elif mr < 0.91: motivo = 'Falta de Interesse'
        else: motivo = 'Transferência'
    elif r_ev < risco + 0.15:
        status = 'Formado'
        meses = random.randint(36, 48)
        motivo = ''
    else:
        status = 'Ativo'
        meses = random.randint(3, 36)
        motivo = ''

    # semestre evasao
    if status == 'Evadido':
        total_sem = max(1, meses // 6)
        total_m = total_sem * 6
        if sem == 1:
            ae = ano + total_m // 12
            se = 2 if total_m % 12 >= 6 else 1
        else:
            ae = ano + total_m // 12
            se = 1 if total_m % 12 < 6 else 2
        if se > 2: se = 2
        sev = f"{ae}.{se}"
    else:
        sev = ''

    bairro = random.choice(["Setor Central","Setor Sul","Setor Oeste","Setor Bueno","Vila Nova","Campinas",
                            "Setor Universitário","Setor Pedro Ludovico","Cidade Jardim","Parque Atheneu"])

    rows.append({
        'id_aluno': i, 'nome': nome, 'idade': idade, 'sexo': sexo, 'raca': raca,
        'renda_familiar': renda, 'trabalha': 'Sim' if trabalha else 'Não',
        'bairro': bairro, 'possui_filhos': 'Sim' if filhos else 'Não',
        'curso': curso, 'semestre_ingresso': ingresso, 'semestre_evasao': sev,
        'status': status, 'meses_cursados': meses, 'motivo_evasao': motivo
    })

# Salvar CSV
with open('dados_evasao_proeja_500.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)

stats = {
    'total': N,
    'evadidos': sum(1 for r in rows if r['status'] == 'Evadido'),
    'ativos': sum(1 for r in rows if r['status'] == 'Ativo'),
    'formados': sum(1 for r in rows if r['status'] == 'Formado'),
    'taxa_evasao': sum(1 for r in rows if r['status'] == 'Evadido') / N * 100,
}
print(f"Total: {stats['total']}")
print(f"Ativos: {stats['ativos']} ({stats['ativos']/N*100:.1f}%)")
print(f"Evadidos: {stats['evadidos']} ({stats['evadidos']/N*100:.1f}%)")
print(f"Formados: {stats['formados']} ({stats['formados']/N*100:.1f}%)")
print(f"Taxa de evasão: {stats['taxa_evasao']:.1f}%")
print("Dataset salvo: dados_evasao_proeja_500.csv")
