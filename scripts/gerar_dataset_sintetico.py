"""
Gerador de Dataset Sintético para EDA - Evasão PROEJA IFG Goiânia
=================================================================
Gera 500 registros de alunos com características realistas baseadas na literatura.

Para executar: python gerar_dataset_sintetico.py
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

N = 500

# ========== PERFIS BASEADOS NA LITERATURA ==========
# Distribuições baseadas em: Anuário 2025, Pereira (2011), Castro & Vitorette (2016)

nomes_m = ["João","Carlos","Paulo","Rafael","Fernando","Lucas","Diego","Rodrigo","Eduardo","Gustavo",
           "Thiago","Leonardo","Fábio","Marcos","Gabriel","Daniel","Hugo","Vinicius","Francisco",
           "Felipe","William","Jorge","Alexandre","Mateus","Igor", "Bruno", "Ricardo", "Pedro"]
nomes_f = ["Maria","Ana","Lúcia","Juliana","Patrícia","Amanda","Larissa","Michele","Camila","Vanessa",
           "Andréia","Tatiane","Renata","Priscila","Simone","Aline","Cristiane","Adriana","Fernanda",
           "Eliane","Viviane","Débora","Luciana","Rosângela","Juliana", "Sandra", "Carla"]
sobrenomes = ["Silva","Santos","Oliveira","Souza","Lima","Costa","Pereira","Rocha","Alves","Martins",
              "Gomes","Ribeiro","Carvalho","Almeida","Rodrigues","Nascimento","Araújo","Barbosa"]

sexos = np.random.choice(['M', 'F'], N, p=[0.48, 0.52])
racas = np.random.choice(['Branca', 'Parda', 'Preta', 'Amarela', 'Indígena'], N, p=[0.25, 0.45, 0.22, 0.05, 0.03])

# Faixa etária realista para EJA: maioria 18-40 anos
idades = np.concatenate([
    np.random.randint(18, 25, int(N*0.35)),
    np.random.randint(25, 35, int(N*0.30)),
    np.random.randint(35, 45, int(N*0.20)),
    np.random.randint(45, 65, int(N*0.15)),
])
np.random.shuffle(idades)

# Renda familiar - baixa renda predominante (Salário mínimo ~ R$ 1.200)
rendas = np.concatenate([
    np.random.uniform(600, 1000, int(N*0.40)),   # Até 1 SM
    np.random.uniform(1000, 1800, int(N*0.30)),  # 1-1.5 SM
    np.random.uniform(1800, 2500, int(N*0.20)),  # 1.5-2 SM
    np.random.uniform(2500, 4000, int(N*0.10)),  # >2 SM
])
np.random.shuffle(rendas)
rendas = np.round(rendas, -1).astype(int)

# Trabalho: maioria trabalha (80%, consistente com literatura EJA)
trabalha = np.random.choice([1, 0], N, p=[0.82, 0.18])

# Filhos: alta proporção (alunos EJA costumam ter filhos)
possui_filhos = np.random.choice([1, 0], N, p=[0.55, 0.45])

# Cursos
cursos = np.random.choice(['Cozinha', 'Alimentação', 'Panificação', 'Hospedagem'], N, p=[0.30, 0.35, 0.20, 0.15])

# Semestre de ingresso (2020.1 a 2025.1)
semestres = []
for _ in range(N):
    ano = np.random.randint(2020, 2026)
    sem = np.random.choice([1, 2])
    semestres.append(f"{ano}.{sem}")

# Status e evasão - baseado nas taxas reais (30-40% de evasão)
# Modelagem: probabilidade de evasão depende de fatores de risco
def calcular_risco(idade, renda, trabalha, filhos, raca, curso):
    score = 0
    if trabalha == 1: score += 0.15
    if filhos == 1: score += 0.12
    if renda < 1200: score += 0.10
    if idade < 25: score += 0.08
    if idade > 50: score += 0.05
    if raca in ['Preta', 'Parda']: score += 0.05  # desigualdade racial
    if curso == 'Cozinha': score += 0.03
    return min(score, 0.70)

status_list = []
meses_list = []
motivos_list = []
semestre_evasao_list = []
for i in range(N):
    risco = calcular_risco(idades[i], rendas[i], trabalha[i], possui_filhos[i], racas[i], cursos[i])
    # Alunos mais recentes têm menos tempo para evadir
    ing = semestres[i]
    ano_ing = int(ing.split('.')[0])
    if ano_ing >= 2024:
        risco *= 0.6  # menos tempo para evadir

    r = np.random.random()
    if r < risco:
        status_list.append('Evadido')
        # Meses até evasão: maioria nos primeiros 12 meses
        meses = int(np.random.exponential(scale=8))
        meses = max(1, min(meses, 36))

        # Motivo de evasão - baseado em distribuições reais
        motivo_r = np.random.random()
        if motivo_r < 0.45:
            motivo = 'Trabalho'
        elif motivo_r < 0.62:
            motivo = 'Horário Incompatível'
        elif motivo_r < 0.75:
            motivo = 'Currículo/Metodologia'
        elif motivo_r < 0.84:
            motivo = 'Problemas de Saúde'
        elif motivo_r < 0.91:
            motivo = 'Questões Familiares'
        elif motivo_r < 0.96:
            motivo = 'Falta de Interesse'
        else:
            motivo = 'Transferência'
        motivos_list.append(motivo)
        meses_list.append(meses)

        # Calcular semestre de evasão
        ing_parts = ing.split('.')
        ano_ing = int(ing_parts[0])
        sem_ing = int(ing_parts[1])
        total_sem = max(1, meses // 6)
        total_meses = total_sem * 6
        if sem_ing == 1:
            ano_ev = ano_ing + (total_meses // 12)
            sem_ev = 2 if total_meses % 12 >= 6 else 1
        else:
            ano_ev = ano_ing + (total_meses // 12)
            sem_ev = 1 if total_meses % 12 < 6 else 2
        if sem_ev > 2: sem_ev = 2
        semestre_evasao_list.append(f"{ano_ev}.{sem_ev}")
    elif r < risco + 0.15:
        status_list.append('Formado')
        meses_list.append(np.random.randint(36, 48))
        motivos_list.append('')
        semestre_evasao_list.append('')
    else:
        status_list.append('Ativo')
        meses_list.append(np.random.randint(3, 36))
        motivos_list.append('')
        semestre_evasao_list.append('')

# Garantir proporções realistas
n_evadidos = status_list.count('Evadido')
n_ativos = status_list.count('Ativo')
n_formados = status_list.count('Formado')
print(f"Proporções - Ativos: {n_ativos/N:.1%}, Evadidos: {n_evadidos/N:.1%}, Formados: {n_formados/N:.1%}")

# Gerar nomes
nomes = []
for i in range(N):
    if sexos[i] == 'M':
        nome = np.random.choice(nomes_m) + ' ' + np.random.choice(sobrenomes) + ' ' + np.random.choice(sobrenomes)
    else:
        nome = np.random.choice(nomes_f) + ' ' + np.random.choice(sobrenomes) + ' ' + np.random.choice(sobrenomes)
    nomes.append(nome)

# Bairros de Goiânia
bairros = ["Setor Central", "Setor Sul", "Setor Oeste", "Setor Bueno", "Setor Marista",
           "Setor Universitário", "Setor Leste Universitário", "Setor Aeroporto",
           "Setor Pedro Ludovico", "Setor Jardim América", "Vila Nova", "Fama",
           "Campinas", "Setor dos Funcionários", "Setor Norte Ferroviário",
           "Cidade Jardim", "Setor Coimbra", "Setor Bela Vista",
           "Residencial Itaipu", "Jardim Curitiba", "Parque Atheneu",
           "Setor Jaó", "Setor Nova Esperança", "Jardim Balneário Meia Ponte"]

# Criar DataFrame
df = pd.DataFrame({
    'id_aluno': range(1, N+1),
    'nome': nomes,
    'idade': idades,
    'faixa_etaria': pd.cut(idades, bins=[0, 25, 35, 45, 100], labels=['18-24', '25-34', '35-44', '45+']),
    'sexo': sexos,
    'raca': racas,
    'renda_familiar': rendas,
    'trabalha': trabalha,
    'possui_filhos': possui_filhos,
    'bairro': np.random.choice(bairros, N),
    'curso': cursos,
    'semestre_ingresso': semestres,
    'semestre_evasao': semestre_evasao_list,
    'status': status_list,
    'meses_cursados': meses_list,
    'motivo_evasao': motivos_list,
})

# Adicionar colunas derivadas
df['renda_per_capita'] = df['renda_familiar'] / (df['possui_filhos'] + 2)  # simplificação
df['idade_categoria'] = pd.cut(df['idade'], bins=[0, 25, 35, 45, 100],
                                labels=['Jovem (18-24)', 'Adulto Jovem (25-34)', 'Adulto (35-44)', 'Adulto+ (45+)'])
df['ano_ingresso'] = df['semestre_ingresso'].str.split('.').str[0].astype(int)

# Salvar
df.to_csv('../data/dados_evasao_proeja_ifg.csv', index=False)
print(f"\nDataset gerado: {N} alunos")
print(f"Colunas: {list(df.columns)}")
print(f"Taxa de evasão: {n_evadidos/N:.1%}")
print(f"Média de meses até evasão: {df[df.status=='Evadido']['meses_cursados'].mean():.1f}")
print(f"Arquivo salvo: ../data/dados_evasao_proeja_ifg.csv")
