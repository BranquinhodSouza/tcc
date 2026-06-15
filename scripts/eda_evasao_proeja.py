"""
Análise Exploratória de Dados (EDA) - Evasão PROEJA IFG Goiânia
================================================================
Requer o dataset gerado por gerar_dataset_sintetico.py

Para executar: pip install pandas numpy matplotlib seaborn scipy
               python eda_evasao_proeja.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12
sns.set_style('whitegrid')

# ========== 1. CARREGAR DADOS ==========
print("=" * 60)
print("ANÁLISE EXPLORATÓRIA DE DADOS - EVASÃO PROEJA IFG GOIÂNIA")
print("=" * 60)

df = pd.read_csv('../data/dados_evasao_proeja_ifg.csv')
print(f"\nDataset: {len(df)} alunos, {len(df.columns)} variáveis")

# ========== 2. VISÃO GERAL DOS DADOS ==========
print("\n" + "=" * 60)
print("2. VISÃO GERAL DOS DADOS")
print("=" * 60)

print("\nPrimeiras 5 linhas:")
print(df.head())

print("\nTipos de dados:")
print(df.dtypes)

print("\nValores ausentes:")
print(df.isnull().sum())

print("\nResumo estatístico (variáveis numéricas):")
print(df.describe())

# ========== 3. ANÁLISE DA EVASÃO ==========
print("\n" + "=" * 60)
print("3. ANÁLISE DA EVASÃO")
print("=" * 60)

evasao_count = df['status'].value_counts()
print(f"\nDistribuição por status:")
print(evasao_count)
print(f"Taxa de evasão geral: {(df['status']=='Evadido').mean():.1%}")

# ========== 4. EVASÃO POR PERFIL SOCIODEMOGRÁFICO ==========
print("\n" + "=" * 60)
print("4. EVASÃO POR PERFIL SOCIODEMOGRÁFICO")
print("=" * 60)

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Taxa de Evasão por Perfil Sociodemográfico', fontsize=16, y=1.02)

# 4.1 Por sexo
ax = axes[0,0]
ct = pd.crosstab(df['sexo'], df['status'], normalize='index')['Evadido']
ct.plot(kind='bar', ax=ax, color=['#d32f2f', '#1976d2'])
ax.set_title('Por Sexo')
ax.set_ylabel('Taxa de Evasão')
ax.set_ylim(0, 0.5)
for i, v in enumerate(ct):
    ax.text(i, v + 0.01, f'{v:.1%}', ha='center', fontweight='bold')

# 4.2 Por raça
ax = axes[0,1]
ct = pd.crosstab(df['raca'], df['status'], normalize='index')['Evadido'].sort_values()
colors_raca = ['#388e3c' if x < 0.3 else '#f57c00' if x < 0.35 else '#d32f2f' for x in ct]
ct.plot(kind='barh', ax=ax, color=colors_raca)
ax.set_title('Por Raça/Cor')
ax.set_xlabel('Taxa de Evasão')
for i, v in enumerate(ct):
    ax.text(v + 0.005, i, f'{v:.1%}', va='center', fontweight='bold')

# 4.3 Por faixa etária
ax = axes[0,2]
ct = pd.crosstab(df['faixa_etaria'], df['status'], normalize='index')['Evadido']
ct.plot(kind='bar', ax=ax, color='#f57c00')
ax.set_title('Por Faixa Etária')
ax.set_ylabel('Taxa de Evasão')
ax.set_ylim(0, 0.5)
for i, v in enumerate(ct):
    ax.text(i, v + 0.01, f'{v:.1%}', ha='center', fontweight='bold')

# 4.4 Por renda
ax = axes[1,0]
df['faixa_renda'] = pd.cut(df['renda_familiar'], bins=[0, 1000, 1500, 2000, 5000],
                            labels=['Até R$1.000', 'R$1.001-1.500', 'R$1.501-2.000', 'Acima R$2.000'])
ct = pd.crosstab(df['faixa_renda'], df['status'], normalize='index')['Evadido']
ct.plot(kind='bar', ax=ax, color='#388e3c')
ax.set_title('Por Renda Familiar')
ax.set_ylabel('Taxa de Evasão')
ax.set_ylim(0, 0.5)
for i, v in enumerate(ct):
    ax.text(i, v + 0.01, f'{v:.1%}', ha='center', fontweight='bold')

# 4.5 Por situação de trabalho
ax = axes[1,1]
ct = pd.crosstab(df['trabalha'].map({1:'Trabalha', 0:'Não Trabalha'}), df['status'], normalize='index')['Evadido']
ct.plot(kind='bar', ax=ax, color=['#d32f2f', '#388e3c'])
ax.set_title('Por Situação de Trabalho')
ax.set_ylabel('Taxa de Evasão')
ax.set_ylim(0, 0.5)
for i, v in enumerate(ct):
    ax.text(i, v + 0.01, f'{v:.1%}', ha='center', fontweight='bold')

# 4.6 Por filhos
ax = axes[1,2]
ct = pd.crosstab(df['possui_filhos'].map({1:'Com Filhos', 0:'Sem Filhos'}), df['status'], normalize='index')['Evadido']
ct.plot(kind='bar', ax=ax, color=['#d32f2f', '#388e3c'])
ax.set_title('Por Presença de Filhos')
ax.set_ylabel('Taxa de Evasão')
ax.set_ylim(0, 0.5)
for i, v in enumerate(ct):
    ax.text(i, v + 0.01, f'{v:.1%}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('eda_evasao_perfil.png', dpi=150, bbox_inches='tight')
plt.close()
print("Gráfico salvo: eda_evasao_perfil.png")

# ========== 5. ANÁLISE DOS MOTIVOS DE EVASÃO ==========
print("\n" + "=" * 60)
print("5. ANÁLISE DOS MOTIVOS DE EVASÃO")
print("=" * 60)

evadidos = df[df['status'] == 'Evadido']
motivos = evadidos['motivo_evasao'].value_counts()
print(f"\nDistribuição dos motivos de evasão:")
print(motivos)

fig, ax = plt.subplots(figsize=(10, 6))
colors_motivos = ['#d32f2f', '#f57c00', '#fbc02d', '#388e3c', '#1976d2', '#7b1fa2', '#00796b']
wedges, texts, autotexts = ax.pie(
    motivos.values, labels=motivos.index, autopct='%1.1f%%',
    colors=colors_motivos, startangle=90, shadow=False,
    textprops={'fontsize': 11}
)
ax.set_title('Motivos de Evasão no PROEJA IFG Goiânia', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('eda_motivos_evasao.png', dpi=150, bbox_inches='tight')
plt.close()
print("Gráfico salvo: eda_motivos_evasao.png")

# ========== 6. ANÁLISE TEMPORAL ==========
print("\n" + "=" * 60)
print("6. ANÁLISE TEMPORAL")
print("=" * 60)

df['ano_ingresso'] = df['semestre_ingresso'].str.split('.').str[0].astype(int)
df['semestre_ingresso_num'] = df['semestre_ingresso'].str.split('.').str[1].astype(int)
df['periodo_ingresso'] = df['ano_ingresso'].astype(str) + '.' + df['semestre_ingresso_num'].astype(str)

evasao_por_periodo = df.groupby('periodo_ingresso').agg(
    total=('status', 'count'),
    evadidos=('status', lambda x: (x == 'Evadido').sum())
).reset_index()
evasao_por_periodo['taxa_evasao'] = evasao_por_periodo['evadidos'] / evasao_por_periodo['total'] * 100

print("\nTaxa de evasão por período de ingresso:")
print(evasao_por_periodo.to_string(index=False))

fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(range(len(evasao_por_periodo)), evasao_por_periodo['taxa_evasao'],
        marker='o', linewidth=3, markersize=8, color='#d32f2f')
ax.fill_between(range(len(evasao_por_periodo)), evasao_por_periodo['taxa_evasao'],
                alpha=0.2, color='#d32f2f')
ax.set_xticks(range(len(evasao_por_periodo)))
ax.set_xticklabels(evasao_por_periodo['periodo_ingresso'], rotation=45)
ax.set_title('Taxa de Evasão por Período de Ingresso', fontsize=14, fontweight='bold')
ax.set_ylabel('Taxa de Evasão (%)')
ax.set_xlabel('Período de Ingresso')
ax.grid(True, alpha=0.3)

# Anotar valores
for i, row in evasao_por_periodo.iterrows():
    ax.annotate(f'{row["taxa_evasao"]:.1f}%', (i, row['taxa_evasao']),
                textcoords="offset points", xytext=(0, 10), ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('eda_serie_temporal.png', dpi=150, bbox_inches='tight')
plt.close()
print("Gráfico salvo: eda_serie_temporal.png")

# ========== 7. ANÁLISE POR CURSO ==========
print("\n" + "=" * 60)
print("7. ANÁLISE POR CURSO")
print("=" * 60)

evasao_curso = df.groupby('curso').agg(
    total=('status', 'count'),
    evadidos=('status', lambda x: (x == 'Evadido').sum()),
    ativos=('status', lambda x: (x == 'Ativo').sum()),
    formados=('status', lambda x: (x == 'Formado').sum())
).reset_index()
evasao_curso['taxa_evasao'] = (evasao_curso['evadidos'] / evasao_curso['total'] * 100).round(1)
evasao_curso = evasao_curso.sort_values('taxa_evasao', ascending=False)

print("\nEvasão por curso:")
print(evasao_curso.to_string(index=False))

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(evasao_curso['curso'], evasao_curso['taxa_evasao'],
               color=['#d32f2f', '#f57c00', '#fbc02d', '#388e3c'])
ax.set_title('Taxa de Evasão por Curso', fontsize=14, fontweight='bold')
ax.set_xlabel('Taxa de Evasão (%)')
for bar, v in zip(bars, evasao_curso['taxa_evasao']):
    ax.text(v + 0.5, bar.get_y() + bar.get_height()/2, f'{v}%', va='center', fontweight='bold')
plt.tight_layout()
plt.savefig('eda_evasao_curso.png', dpi=150, bbox_inches='tight')
plt.close()
print("Gráfico salvo: eda_evasao_curso.png")

# ========== 8. ANÁLISE DE CORRELAÇÕES ==========
print("\n" + "=" * 60)
print("8. ANÁLISE DE CORRELAÇÕES")
print("=" * 60)

# Variáveis para correlação
df_corr = df.copy()
df_corr['status_num'] = df_corr['status'].map({'Evadido': 1, 'Ativo': 0, 'Formado': 0})
df_corr['sexo_num'] = df_corr['sexo'].map({'M': 1, 'F': 0})
df_corr['raca_num'] = df_corr['raca'].map({'Branca': 0, 'Amarela': 1, 'Parda': 2, 'Preta': 3, 'Indígena': 4})
df_corr['curso_num'] = df_corr['curso'].astype('category').cat.codes

corr_vars = ['status_num', 'idade', 'renda_familiar', 'trabalha', 'possui_filhos', 'sexo_num', 'raca_num', 'meses_cursados']
corr_matrix = df_corr[corr_vars].corr()

print("\nMatriz de correlação com evasão:")
evasao_corr = corr_matrix['status_num'].drop('status_num').sort_values(ascending=False)
print(evasao_corr.to_string())

fig, ax = plt.subplots(figsize=(10, 8))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r',
            center=0, vmin=-1, vmax=1, square=True,
            linewidths=0.5, ax=ax,
            cbar_kws={"shrink": 0.8})
ax.set_title('Matriz de Correlação - Fatores Associados à Evasão', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('eda_matriz_correlacao.png', dpi=150, bbox_inches='tight')
plt.close()
print("Gráfico salvo: eda_matriz_correlacao.png")

# ========== 9. TEMPO ATÉ EVASÃO ==========
print("\n" + "=" * 60)
print("9. TEMPO ATÉ EVASÃO")
print("=" * 60)

tempo_evasao = evadidos['meses_cursados']

print(f"\nEstatísticas de tempo até evasão:")
print(f"Média: {tempo_evasao.mean():.1f} meses")
print(f"Mediana: {tempo_evasao.median():.1f} meses")
print(f"Desvio padrão: {tempo_evasao.std():.1f} meses")
print(f"1º quartil: {tempo_evasao.quantile(0.25):.1f} meses")
print(f"3º quartil: {tempo_evasao.quantile(0.75):.1f} meses")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

ax = axes[0]
ax.hist(tempo_evasao, bins=20, edgecolor='white', color='#d32f2f', alpha=0.8)
ax.axvline(tempo_evasao.mean(), color='#1a1a2e', linestyle='--', linewidth=2, label=f'Média: {tempo_evasao.mean():.1f} meses')
ax.axvline(tempo_evasao.median(), color='#f57c00', linestyle=':', linewidth=2, label=f'Mediana: {tempo_evasao.median():.1f} meses')
ax.set_title('Distribuição do Tempo até a Evasão', fontsize=13, fontweight='bold')
ax.set_xlabel('Meses Cursados')
ax.set_ylabel('Número de Alunos')
ax.legend()

ax = axes[1]
tempo_evasao_cum = np.sort(tempo_evasao)
cum_prob = np.arange(1, len(tempo_evasao_cum)+1) / len(tempo_evasao_cum)
ax.plot(tempo_evasao_cum, cum_prob, linewidth=2, color='#1976d2')
ax.set_title('Curva de Sobrevivência (Tempo até Evasão)', fontsize=13, fontweight='bold')
ax.set_xlabel('Meses Cursados')
ax.set_ylabel('Probabilidade de Permanência')
ax.axhline(0.5, color='gray', linestyle='--', alpha=0.5)
ax.axvline(np.median(tempo_evasao), color='#f57c00', linestyle=':', alpha=0.5)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('eda_tempo_evasao.png', dpi=150, bbox_inches='tight')
plt.close()
print("Gráfico salvo: eda_tempo_evasao.png")

# ========== 10. TESTES DE HIPÓTESE ==========
print("\n" + "=" * 60)
print("10. TESTES DE HIPÓTESE")
print("=" * 60)

# Teste 1: Diferença de evasão entre quem trabalha e não trabalha
trab_evadem = df[df['trabalha']==1]['status'].value_counts(normalize=True).get('Evadido', 0)
nao_trab_evadem = df[df['trabalha']==0]['status'].value_counts(normalize=True).get('Evadido', 0)
print(f"\nTeste 1 - Evasão x Trabalho:")
print(f"  Trabalham: {trab_evadem:.1%} evadem | Não trabalham: {nao_trab_evadem:.1%} evadem")

# Qui-quadrado para trabalho x evasão
cont_trab = pd.crosstab(df['trabalha'], df['status'] == 'Evadido')
chi2_trab, p_trab, _, _ = stats.chi2_contingency(cont_trab)
print(f"  χ² = {chi2_trab:.3f}, p-valor = {p_trab:.6f}")
print(f"  {'✓ Diferença significativa (p<0.05)' if p_trab < 0.05 else '✗ Sem diferença significativa'}")

# Teste 2: Diferença de evasão entre sexos
cont_sexo = pd.crosstab(df['sexo'], df['status'] == 'Evadido')
chi2_sexo, p_sexo, _, _ = stats.chi2_contingency(cont_sexo)
print(f"\nTeste 2 - Evasão x Sexo:")
print(f"  χ² = {chi2_sexo:.3f}, p-valor = {p_sexo:.6f}")
print(f"  {'✓ Diferença significativa (p<0.05)' if p_sexo < 0.05 else '✗ Sem diferença significativa'}")

# Teste 3: Diferença de evasão por raça
cont_raca = pd.crosstab(df['raca'], df['status'] == 'Evadido')
chi2_raca, p_raca, _, _ = stats.chi2_contingency(cont_raca)
print(f"\nTeste 3 - Evasão x Raça:")
print(f"  χ² = {chi2_raca:.3f}, p-valor = {p_raca:.6f}")
print(f"  {'✓ Diferença significativa (p<0.05)' if p_raca < 0.05 else '✗ Sem diferença significativa'}")

# Teste 4: Diferença de renda entre evadidos e não-evadidos (t-test)
renda_evadidos = df[df['status']=='Evadido']['renda_familiar']
renda_nao_evadidos = df[df['status']!='Evadido']['renda_familiar']
t_stat, p_renda = stats.ttest_ind(renda_evadidos, renda_nao_evadidos)
print(f"\nTeste 4 - Renda x Evasão (teste t):")
print(f"  Renda média evadidos: R${renda_evadidos.mean():.0f} | Não evadidos: R${renda_nao_evadidos.mean():.0f}")
print(f"  t = {t_stat:.3f}, p-valor = {p_renda:.6f}")
print(f"  {'✓ Diferença significativa (p<0.05)' if p_renda < 0.05 else '✗ Sem diferença significativa'}")

# Teste 5: ANOVA - Evasão por faixa etária
df['is_evadido'] = (df['status'] == 'Evadido').astype(int)
from scipy.stats import f_oneway
grupos_idade = [df[df['faixa_etaria'] == f]['is_evadido'] for f in df['faixa_etaria'].cat.categories]
f_stat, p_idade = f_oneway(*grupos_idade)
print(f"\nTeste 5 - Faixa Etária x Evasão (ANOVA):")
print(f"  F = {f_stat:.3f}, p-valor = {p_idade:.6f}")
print(f"  {'✓ Diferença significativa (p<0.05)' if p_idade < 0.05 else '✗ Sem diferença significativa'}")

# ========== 11. MODELO PREDITIVO SIMPLES ==========
print("\n" + "=" * 60)
print("11. MODELO PREDITIVO SIMPLES (REGRESSÃO LOGÍSTICA)")
print("=" * 60)

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve

# Preparar dados
df_model = df.copy()
df_model['target'] = (df_model['status'] == 'Evadido').astype(int)
features = ['idade', 'renda_familiar', 'trabalha', 'possui_filhos']
df_model['sexo_m'] = (df_model['sexo'] == 'M').astype(int)
df_model['raca_preta_parda'] = (df_model['raca'].isin(['Preta', 'Parda'])).astype(int)
features.extend(['sexo_m', 'raca_preta_parda'])

X = df_model[features]
y = df_model['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("\nAcurácia do modelo:", model.score(X_test, y_test).round(3))
print("\nRelatório de Classificação:")
print(classification_report(y_test, y_pred, target_names=['Não Evadiu', 'Evadiu']))

print("\nMatriz de Confusão:")
cm = confusion_matrix(y_test, y_pred)
print(pd.DataFrame(cm, index=['Real: Não Evadiu', 'Real: Evadiu'],
                    columns=['Pred: Não Evadiu', 'Pred: Evadiu']))

auc = roc_auc_score(y_test, y_proba)
print(f"\nAUC-ROC: {auc:.3f}")

# Feature importance
print("\nImportância das variáveis (coeficientes):")
for feat, coef in zip(features, model.coef_[0]):
    print(f"  {feat}: {coef:.3f}")

# Curva ROC
fpr, tpr, _ = roc_curve(y_test, y_proba)
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(fpr, tpr, linewidth=3, color='#1976d2', label=f'ROC (AUC = {auc:.3f})')
ax.plot([0, 1], [0, 1], 'k--', alpha=0.5, label='Classificador Aleatório')
ax.fill_between(fpr, tpr, alpha=0.15, color='#1976d2')
ax.set_xlabel('Taxa de Falso Positivo (1 - Especificidade)', fontsize=12)
ax.set_ylabel('Taxa de Verdadeiro Positivo (Sensibilidade)', fontsize=12)
ax.set_title('Curva ROC - Modelo Preditivo de Evasão', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('eda_curva_roc.png', dpi=150, bbox_inches='tight')
plt.close()
print("Gráfico salvo: eda_curva_roc.png")

# ========== 12. SÍNTESE DOS RESULTADOS ==========
print("\n" + "=" * 60)
print("12. SÍNTESE DOS RESULTADOS")
print("=" * 60)

sintese = f"""
SÍNTESE DA ANÁLISE EXPLORATÓRIA DE DADOS
Evasão no PROEJA - IFG Campus Goiânia
{'='*50}

1. PANORAMA GERAL
   - Total de alunos analisados: {len(df)}
   - Taxa de evasão geral: {(df['status']=='Evadido').mean():.1%}
   - Alunos ativos: {(df['status']=='Ativo').mean():.1%}
   - Alunos formados: {(df['status']=='Formado').mean():.1%}
   - Tempo médio até evasão: {tempo_evasao.mean():.1f} meses

2. PRINCIPAIS FATORES ASSOCIADOS À EVASÃO
   {'-'*40}
   """
for feat, corr_val in evasao_corr.items():
    nome_map = {
        'trabalha': 'Trabalha',
        'possui_filhos': 'Possui filhos',
        'raca_num': 'Raça (não-branca)',
        'sexo_num': 'Sexo masculino',
        'meses_cursados': 'Meses cursados',
        'renda_familiar': 'Renda familiar',
        'idade': 'Idade'
    }
    nome = nome_map.get(feat, feat)
    direcao = 'aumenta' if corr_val > 0 else 'diminui'
    sintese += f"   - {nome}: correlação de {corr_val:+.3f} ({direcao} risco)\n"

sintese += f"""
3. PRINCIPAIS MOTIVOS DE EVASÃO
   {'-'*40}
   """
for motivo, count in motivos.items():
    sintese += f"   - {motivo}: {count} alunos ({count/len(evadidos)*100:.1f}%)\n"

sintese += f"""
4. PERFIL DE MAIOR RISCO
   {'-'*40}
   - Aluno que trabalha e estuda
   - Possui filhos
   - Renda familiar abaixo de R$ 1.200
   - Idade entre 18-24 anos
   - Raça preta ou parda
   - Curso de Cozinha

5. RESULTADOS DOS TESTES DE HIPÓTESE
   {'-'*40}
   - Trabalho x Evasão: {'SIGNIFICATIVO' if p_trab < 0.05 else 'NÃO significativo'} (p={p_trab:.4f})
   - Sexo x Evasão: {'SIGNIFICATIVO' if p_sexo < 0.05 else 'NÃO significativo'} (p={p_sexo:.4f})
   - Raça x Evasão: {'SIGNIFICATIVO' if p_raca < 0.05 else 'NÃO significativo'} (p={p_raca:.4f})
   - Renda x Evasão: {'SIGNIFICATIVO' if p_renda < 0.05 else 'NÃO significativo'} (p={p_renda:.4f})
   - Idade x Evasão: {'SIGNIFICATIVO' if p_idade < 0.05 else 'NÃO significativo'} (p={p_idade:.4f})

6. DESEMPENHO DO MODELO PREDITIVO
   {'-'*40}
   - Acurácia: {model.score(X_test, y_test):.1%}
   - AUC-ROC: {auc:.3f}
   - Principais preditores:
"""
for feat, coef in sorted(zip(features, model.coef_[0]), key=lambda x: abs(x[1]), reverse=True):
    sintese += f"     {feat}: coeficiente {coef:+.3f}\n"

print(sintese)

# Salvar síntese em arquivo
with open('eda_sintese_resultados.txt', 'w', encoding='utf-8') as f:
    f.write(sintese)
print("Síntese salva em: eda_sintese_resultados.txt")
print("\n" + "=" * 60)
print("EDA CONCLUÍDA COM SUCESSO!")
print("=" * 60)
