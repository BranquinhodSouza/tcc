# Gerador do Pre-Projeto de TCC - Versao simplificada
$docxPath = "$PSScriptRoot\Pre_projeto_Evasao_PROEJA_IFG.docx"

try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $doc = $word.Documents.Add()
    $sel = $word.Selection

    $sel.Font.Name = "Times New Roman"
    $sel.Font.Size = 12
    $sel.ParagraphFormat.LineSpacingRule = 4
    $sel.ParagraphFormat.SpaceAfter = 0
    $sel.ParagraphFormat.Alignment = 3

    function Center($txt, $sz, $b) {
        $sel.ParagraphFormat.Alignment = 1
        $sel.Font.Bold = $b; $sel.Font.Size = $sz
        $sel.TypeText($txt)
        $sel.TypeParagraph()
    }
    function Justify($txt) {
        $sel.ParagraphFormat.Alignment = 3
        $sel.Font.Bold = $false; $sel.Font.Size = 12
        $sel.TypeText($txt)
        $sel.TypeParagraph()
    }
    function H1($txt) {
        $sel.ParagraphFormat.Alignment = 1
        $sel.Font.Bold = $true; $sel.Font.Size = 14
        $sel.TypeText($txt)
        $sel.TypeParagraph()
        $sel.ParagraphFormat.Alignment = 3
    }
    function H2($txt) {
        $sel.Font.Bold = $true; $sel.Font.Size = 12
        $sel.TypeText($txt)
        $sel.TypeParagraph()
    }
    function Bullet($txt) {
        $sel.ParagraphFormat.Alignment = 3
        $sel.Font.Bold = $false; $sel.Font.Size = 12
        $sel.TypeText("- $txt")
        $sel.TypeParagraph()
    }

    # ===== CAPA =====
    for ($i=0; $i -lt 6; $i++) { $sel.TypeParagraph() }
    Center "INSTITUTO FEDERAL DE EDUCACAO, CIENCIA E TECNOLOGIA DE GOIAS" 12 $true
    Center "CAMPUS GOIANIA" 12 $true
    Center "DEPARTAMENTO DAS AREAS ACADEMICAS IV" 11 $false
    Center "COORDENACAO DE INFORMATICA" 11 $false
    Center "BACHARELADO EM SISTEMAS DE INFORMACAO" 12 $true
    $sel.TypeParagraph(); $sel.TypeParagraph()
    Center "ANALISE DE EVASAO NO PROEJA DO IFG CAMPUS GOIANIA:" 14 $true
    Center "IDENTIFICACAO DE PADROES, PROPOSTAS DE INTERVENCAO" 14 $true
    Center "E DESENVOLVIMENTO DE UM DASHBOARD PARA MONITORAMENTO" 14 $true
    $sel.TypeParagraph(); $sel.TypeParagraph()
    Center "Paulo Branquinho de Souza" 12 $true
    $sel.TypeParagraph(); $sel.TypeParagraph()
    Center "Goiania/GO" 12 $false
    $sel.Font.Size = 12; $sel.TypeText("2026"); $sel.TypeParagraph()
    $sel.InsertBreak(7)

    # ===== FICHA =====
    Justify "Paulo Branquinho de Souza"
    Justify "ANALISE DE EVASAO NO PROEJA DO IFG CAMPUS GOIANIA: IDENTIFICACAO DE PADROES, PROPOSTAS DE INTERVENCAO E DESENVOLVIMENTO DE UM DASHBOARD PARA MONITORAMENTO"
    $sel.TypeParagraph()
    Justify "Pre-projeto de Trabalho de Conclusao de Curso apresentado no Instituto Federal de Goias como requisito basico para a conclusao do curso de Sistemas de Informacao."
    $sel.TypeParagraph()
    $sel.Font.Bold = $true; $sel.TypeText("Orientador: Prof. <titulo>. <nome>"); $sel.Font.Bold = $false
    $sel.InsertBreak(7)

    # ===== SUMARIO =====
    H1 "SUMARIO"
    @("1 INTRODUCAO","2 JUSTIFICATIVA","3 OBJETIVOS","3.1 Objetivo Geral","3.2 Objetivos Especificos",
      "4 REFERENCIAL TEORICO","5 METODOLOGIA DA PESQUISA","5.1 Classificacao da Pesquisa",
      "5.2 Procedimentos Metodologicos","6 CRONOGRAMA","REFERENCIAS BIBLIOGRAFICAS") | ForEach-Object {
        $sel.TypeText($_); $sel.TypeParagraph()
    }
    $sel.InsertBreak(7)

    # ===== 1 INTRODUCAO =====
    H1 "1 INTRODUCAO"
    Justify "A Educacao de Jovens e Adultos (EJA) constitui uma modalidade de ensino fundamental para a promocao da inclusao social e do resgate da cidadania de sujeitos historicamente marginalizados do processo educacional brasileiro. Conforme dados do Anuario Brasileiro da Educacao Basica (2025), o acesso a EJA caiu 34,5% na ultima decada, registrando 2,4 milhoes de matriculas em 2024, o menor numero da serie historica. Paralelamente, 29% dos brasileiros de 15 a 64 anos sao analfabetos funcionais, evidenciando a persistencia de um grave deficit educacional."
    Justify "No ambito da Rede Federal de Educacao Profissional e Tecnologica, o Programa de Integracao da Educacao Profissional com a Educacao Basica na Modalidade de Educacao de Jovens e Adultos (PROEJA) foi instituido pelo Decreto no 5.478/2005, posteriormente ampliado pelo Decreto no 5.840/2006. No Instituto Federal de Goias (IFG) - Campus Goiania, o PROEJA teve inicio com os Cursos Tecnicos Integrados em Servicos de Alimentacao e Cozinha, enfrentando desde sua origem desafios significativos relacionados a evasao escolar. Estudos especificos como os de Pereira (2011) e Castro e Vitorette (2016) revelam um percurso contraditorio na construcao do direito a educacao."
    Justify "Diante deste cenario, identifica-se a necessidade de investigar de forma sistematica os padroes de evasao no PROEJA do IFG Campus Goiania, integrando analise de dados institucionais e referencial teorico sobre educacao de jovens e adultos. O desafio reside em como a tecnologia da informacao, por meio de ferramentas de Business Intelligence (BI) e analise preditiva, pode auxiliar na identificacao precoce de alunos em risco de abandono e no monitoramento continuo dos indicadores de permanencia."
    Justify "Nesse contexto, assume-se que o desenvolvimento de um dashboard interativo para visualizacao e analise dos dados de evasao, combinado com a identificacao de padroes sociodemograficos e institucionais, permitira a gestao academica tomar decisoes mais informadas para a elaboracao de politicas de permanencia estudantil. Espera-se que esta pesquisa contribua para a reducao dos indices de abandono e para o fortalecimento do PROEJA como politica publica de inclusao educacional."

    # ===== 2 JUSTIFICATIVA =====
    H1 "2 JUSTIFICATIVA"
    Justify "A escolha deste tema justifica-se pela relevancia social e academica da EJA no Brasil, modalidade que atende majoritariamente alunos pretos e pardos (76,8% das matriculas), trabalhadores de baixa renda e pessoas em situacao de vulnerabilidade social (Todos pela Educacao, 2025). A evasao escolar no PROEJA representa nao apenas o desperdicio de recursos publicos, mas tambem a perpetuacao de um ciclo de exclusao educacional que compromete a mobilidade social desses individuos."
    Justify "O presente trabalho contribui diretamente para a formacao esperada no Perfil do Egresso do curso de Sistemas de Informacao, uma vez que exige a aplicacao integrada de conhecimentos multidisciplinares das seguintes areas:"
    Bullet "Banco de Dados: modelagem e estruturacao dos dados institucionais de matricula, frequencia e evasao, aplicando tecnicas de modelagem dimensional para suporte a decisao."
    Bullet "Business Intelligence: desenvolvimento de dashboard interativo utilizando Power BI ou Google Looker Studio para analise de indicadores educacionais."
    Bullet "Mineracao de Dados: aplicacao de tecnicas de analise exploratoria e identificacao de padroes nos dados de evasao, permitindo a construcao de modelos preditivos de risco."
    Bullet "Engenharia de Software: levantamento de requisitos e modelagem do sistema de monitoramento, garantindo que a solucao siga padroes de qualidade e usabilidade."
    Justify "Do ponto de vista institucional, a pesquisa oferece ao IFG Campus Goiania um instrumento concreto para o monitoramento da evasao, permitindo a identificacao precoce de alunos em risco e a avaliacao do impacto das politicas de assistencia estudantil. Conforme Oliveira e Carmo (2021), a tematica da evasao no PROEJA ainda carece de estudos aprofundados que integrem analise quantitativa de dados e propostas de intervencao baseadas em evidencias."

    # ===== 3 OBJETIVOS =====
    H1 "3 OBJETIVOS"
    H2 "3.1 Objetivo Geral"
    Justify "Analisar os fatores associados a evasao no PROEJA do IFG Campus Goiania, identificando padroes sociodemograficos e institucionais, propondo medidas de intervencao e desenvolvendo um dashboard interativo para monitoramento continuo dos indicadores de permanencia estudantil."
    H2 "3.2 Objetivos Especificos"
    @("1. Levantar o referencial teorico sobre evasao escolar na EJA e no PROEJA, com enfase em estudos realizados no IFG Campus Goiania;",
      "2. Identificar os principais fatores que contribuem para a evasao nos cursos PROEJA do IFG Campus Goiania, a partir da analise de dados institucionais e da literatura existente;",
      "3. Mapear o perfil sociodemografico dos alunos evadidos (faixa etaria, sexo, raca, renda, situacao de trabalho, presenca de filhos) para identificacao de grupos de risco;",
      "4. Elaborar um conjunto de propostas de intervencao institucional, pedagogica e de apoio ao estudante visando a reducao das taxas de evasao;",
      "5. Modelar e desenvolver um dashboard interativo para visualizacao dos indicadores de evasao, utilizando ferramentas de Business Intelligence;",
      "6. Avaliar a eficacia do dashboard como ferramenta de apoio a gestao academica na tomada de decisoes relacionadas a permanencia estudantil.") | ForEach-Object { Justify $_ }

    # ===== 4 REFERENCIAL TEORICO =====
    H1 "4 REFERENCIAL TEORICO"
    Justify "A fundamentacao teorica deste projeto sustenta-se na necessidade de compreender a evasao escolar na Educacao de Jovens e Adultos como um fenomeno multidimensional, fortemente influenciado por fatores socioeconomicos, institucionais e pedagogicos. Os estudos de Oliveira e Carmo (2021) identificaram duas grandes categorias de causas no PROEJA: a necessidade de trabalho/remuneracao e a falta de preparo dos professores para atuar na modalidade."
    Justify "Para o contexto especifico do IFG Campus Goiania, a pesquisa fundamenta-se nos trabalhos de Pereira (2011), que investigou os fatores de acesso e permanencia no PROEJA, e de Castro e Vitorette (2016), que analisaram as contradicoes na implantacao do programa. Esses estudos revelam que a resistencia institucional, a focalizacao do programa e a inadequacao das metodologias de ensino contribuem significativamente para o abandono escolar. Apenas a Coordenacao de Turismo e Hospitalidade mostrou-se favoravel a oferta inicial, evidenciando a falta de adesao institucional."
    Justify "Do ponto de vista das politicas publicas, o trabalho dialoga com a analise de Silva, Silva e Oliveira (2023) sobre o cumprimento das metas 8, 9 e 10 do PNE 2014-2024 em Goias e Goiania. As autoras constatam que as metas estao distantes de se concretizar, com descontinuidade de estrategias e regressao dos indicadores."
    Justify "No campo da analise de dados educacionais, Assis (2017) demonstra que a mineracao de dados educacionais permite identificar perfis de estudantes com propensao a evasao, utilizando algoritmos de classificacao como CART e Random Forest. Essas tecnicas podem ser combinadas com dashboards interativos para fornecer a gestao academica informacoes em tempo real sobre o risco de abandono."
    Justify "Complementarmente, a abordagem de Freire (2023) sobre uma educacao dialogica e emancipadora serve como contraponto as praticas pedagogicas tradicionais identificadas como inadequadas para a EJA. A valorizacao dos saberes previos dos educandos e a contextualizacao do curriculo sao apontadas por Dutra, Melo e Silva (2026) como estrategias fundamentais para promover o engajamento e a permanencia dos estudantes."
    Justify "A construcao deste trabalho e uma sintese integradora de diversas competencias adquiridas ao longo do Bacharelado em Sistemas de Informacao. As disciplinas abaixo contribuem de forma predominante:"
    Bullet "Banco de Dados: modelagem e estruturacao dos dados institucionais, aplicando conceitos de modelagem dimensional e otimizacao de consultas para suporte a decisao."
    Bullet "Business Intelligence: desenvolvimento do dashboard e aplicacao de tecnicas de visualizacao de dados e indicadores de desempenho (KPIs)."
    Bullet "Engenharia de Software: levantamento de requisitos e modelagem do sistema de monitoramento, garantindo arquitetura robusta e documentada."
    Bullet "Interacao Homem-Computador (IHC): desenvolvimento da interface do dashboard com foco na usabilidade e experiencia do usuario."
    Bullet "Probabilidade e Estatistica: analise descritiva dos dados e aplicacao de tecnicas de correlacao e regressao."

    # ===== 5 METODOLOGIA =====
    H1 "5 METODOLOGIA DA PESQUISA"
    H2 "5.1 Classificacao da Pesquisa"
    Justify "Quanto a sua natureza, esta e uma pesquisa aplicada, pois objetiva gerar conhecimentos para aplicacao pratica na solucao de um problema real de evasao escolar. Do ponto de vista dos objetivos, a pesquisa e exploratoria e descritiva. Quanto a abordagem, caracteriza-se como mista (quantitativa e qualitativa): quantitativa na analise estatistica dos dados de evasao e na validacao dos indicadores do dashboard; qualitativa na interpretacao dos fatores contextuais e institucionais."
    H2 "5.2 Procedimentos Metodologicos"
    Justify "O desenvolvimento sera dividido em seis fases fundamentais:"
    Bullet "Revisao Sistematica da Literatura: levantamento bibliografico em bases como Google Academico, SciELO e Portal CAPES, focando em artigos e dissertacoes sobre evasao na EJA/PROEJA, com enfase no IFG Campus Goiania."
    Bullet "Coleta e Preparacao dos Dados: solicitacao de dados institucionais junto a Coordenacao de Registro Academico do IFG Campus Goiania, incluindo matriculas, frequencia e registros de evasao dos cursos PROEJA. Os dados serao anonimizados conforme a LGPD."
    Bullet "Analise Exploratoria de Dados (EDA): aplicacao de tecnicas de analise estatistica descritiva utilizando Python para caracterizacao do perfil dos alunos evadidos e identificacao de correlacoes entre variaveis sociodemograficas e evasao."
    Bullet "Modelagem Preditiva: desenvolvimento de modelos de classificacao (Regressao Logistica, Random Forest) para identificacao precoce de alunos com propensao a evasao, utilizando variaveis como frequencia, desempenho e perfil socioeconomico."
    Bullet "Desenvolvimento do Dashboard: criacao de dashboard interativo utilizando Power BI ou Google Looker Studio, com paineis de KPIs, graficos de evolucao temporal e tabela de alerta precoce."
    Bullet "Elaboracao de Propostas de Intervencao: recomendacoes institucionais, pedagogicas e de apoio ao estudante organizadas por prioridade e viabilidade."

    # ===== 6 CRONOGRAMA =====
    H1 "6 CRONOGRAMA"
    $sel.Font.Size = 10
    # Usar tabulacao para simular tabela
    $sel.TypeText("Atividade / Mes`tAbr`tMai`tJun`tJul`tAgo`tSet`tOut`tNov"); $sel.TypeParagraph()
    $cron = @(
        "1. Revisao Bibliografica e Refinamento do Tema`tX`tX`t`t`t`t`t`t",
        "2. Coleta e Preparacao dos Dados`t`tX`tX`t`t`t`t`t",
        "3. Escrita do Relatorio de Qualificacao (TCC 1)`tX`tX`tX`tX`t`t`t`t",
        "4. Analise Exploratoria e Modelagem Preditiva`t`t`t`tX`tX`t`t`t",
        "5. Desenvolvimento do Dashboard`t`t`t`t`tX`tX`t`t",
        "6. Elaboracao das Propostas de Intervencao`t`t`t`t`t`tX`t`t",
        "7. Escrita da Monografia Final (TCC 2)`t`t`t`t`t`tX`tX`tX",
        "8. Preparacao para Defesa`t`t`t`t`t`t`t`tX"
    )
    foreach ($l in $cron) { $sel.TypeText($l); $sel.TypeParagraph() }

    # ===== REFERENCIAS =====
    $sel.InsertBreak(7)
    H1 "REFERENCIAS BIBLIOGRAFICAS"
    $sel.Font.Size = 11
    @(
        "ANUARIO BRASILEIRO DA EDUCACAO BASICA 2025. Sao Paulo: Todos pela Educacao, 2025.",
        "ASSIS, L. R. S. Perfil de evasao no ensino superior brasileiro: uma abordagem de mineracao de dados. 2017. Dissertacao (Mestrado) - Universidade de Brasilia, Brasilia, 2017.",
        "CASTRO, M. D. R.; VITORETTE, J. M. B. O Programa de Integracao da Educacao Profissional com a Educacao Basica na Modalidade de Educacao de Jovens e Adultos (PROEJA) no IFG - Campus Goiania: um percurso contraditorio na construcao do direito a educacao. HOLOS, v. 2, p. 301-318, 2016.",
        "CASTRO, M. D. R. O PROEJA no IFG - Campus Goiania: contradicoes, limites e perspectivas. 2018. Dissertacao (Mestrado em Educacao) - PUC Goias, Goiania, 2018.",
        "DUTRA, M. F. C.; MELO, A. C. L.; SILVA, R. I. P. Desafios e Perspectivas da Educacao de Jovens e Adultos (EJA): um olhar sobre a evasao e a pratica pedagogica no Brasil Contemporaneo. REASE, v. 12, n. 5, 2026.",
        "FREIRE, P. Pedagogia do Oprimido. 87. ed. Rio de Janeiro: Paz e Terra, 2023.",
        "NERY, M. C. R.; PEREIRA, J. O.; AMARAL, P. G. Educacao de Jovens e Adultos - EJA - seus impasses e suas contradicoes. Revista Eletronica Cientifica da UERGS, v. 6, n. 1, p. 29-41, 2020.",
        "OLIVEIRA, P. L.; CARMO, N. C. A tematica evasao escolar no contexto do PROEJA: uma revisao integrativa. Revista Ponto de Vista, v. 10, n. 1, p. 01-21, 2021.",
        "PEREIRA, J. V. O PROEJA no Instituto Federal de Goias - Campus Goiania: um estudo sobre os fatores de acesso e permanencia na escola. 2011. 154 f. Dissertacao (Mestrado em Educacao) - Universidade de Brasilia, Brasilia, 2011.",
        "SANTOS, A. F. et al. Desafios da Educacao de Jovens e Adultos no Brasil: entre metodologias inadequadas e politicas instaveis. Missioneira, v. 27, n. 1, p. 103-114, 2025.",
        "SILVA, T. G. C.; SILVA, R. B. B.; OLIVEIRA, G. L. Educacao de Jovens e Adultos em Goias e Goiania a luz dos dados do INEP. Revista Sapiencia, v. 12, n. 2, p. 88-104, 2023.",
        "TOLENTINO FILHO, D. Educacao de jovens e adultos no Brasil: Avancos, desafios e perspectivas. International Integralize Scientific, v. 5, n. 46, 2025."
    ) | ForEach-Object { $sel.TypeText($_); $sel.TypeParagraph() }

    $doc.SaveAs2([ref]$docxPath)
    $doc.Close()
    $word.Quit()
    Write-Output "Documento gerado: $docxPath"
} catch {
    Write-Output "ERRO: $_"
    try { $word.Quit() } catch {}
} finally {
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect(); [System.GC]::WaitForPendingFinalizers()
}
