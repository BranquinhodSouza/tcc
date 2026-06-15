function Get-MermaidImage {
    param([string]$MermaidCode, [string]$OutputName, [string]$Format = "png")

    $bytes = [System.Text.Encoding]::UTF8.GetBytes($MermaidCode)
    $base64 = [Convert]::ToBase64String($bytes)
    $urlsafe = $base64.Replace('+', '-').Replace('/', '_').TrimEnd('=')
    $url = "https://mermaid.ink/$Format/$urlsafe"

    $outputPath = Join-Path $PSScriptRoot "$OutputName.$Format"
    Write-Output "Baixando: $OutputName.$Format ..."

    try {
        $r = Invoke-WebRequest -Uri $url -Method Get -TimeoutSec 60 -UseBasicParsing
        [System.IO.File]::WriteAllBytes($outputPath, $r.Content)
        Write-Output "  OK - $(($r.Content).Length) bytes"
    } catch {
        Write-Output "  ERRO: $($_.Exception.Message)"
    }
}

$scriptPath = $PSScriptRoot
Write-Output "Gerando diagramas em: $scriptPath"
Write-Output ""

# 1. Diagrama de Arquitetura
Get-MermaidImage -MermaidCode @"
graph TB
    subgraph "Cliente Mobile"
        RN[React Native App]
    end
    subgraph "Backend - FastAPI"
        API[REST API]
        AUTH[Autenticação JWT]
        REC[Recommendation Engine]
        ML[Machine Learning - Futuro]
    end
    subgraph "Persistência"
        DB[(PostgreSQL)]
        STO[Cloud Storage]
    end
    RN -->|HTTP/JSON| API
    API --> AUTH
    API --> REC
    REC --> DB
    API -->|Upload| STO
    ML -.->|Integração futura| API
    API --> DB
"@ -OutputName "01-arquitetura"

# 2. Diagrama de Componentes
Get-MermaidImage -MermaidCode @"
graph LR
    subgraph "Frontend Mobile"
        UI[UI Components]
        NAV[Navigation]
        STATE[State Management]
        API_CLI[API Client]
    end
    subgraph "Backend"
        API_L[API Layer]
        SRV[Services Layer]
        REPO[Repository Layer]
        MODELS[Models/Entities]
    end
    subgraph "Externos"
        JWT_AUTH[JWT Auth]
        STORAGE[File Storage]
    end
    UI --> NAV
    UI --> STATE
    STATE --> API_CLI
    API_CLI --> API_L
    API_L --> SRV
    SRV --> REPO
    REPO --> MODELS
    SRV --> JWT_AUTH
    API_L --> STORAGE
"@ -OutputName "02-componentes"

# 3. Fluxo de Recomendacao
Get-MermaidImage -MermaidCode @"
flowchart TD
    A[Usuário acessa o app] --> B{Primeiro acesso?}
    B -->|Sim| C[Exibir Questionário de Preferências]
    B -->|Não| D[Carregar perfil existente]
    C --> E[Capturar preferências]
    E --> F[Salvar no banco de dados]
    D --> G[Gerar recomendações]
    F --> G
    G --> H[Aplicar filtros:<br/>Tipo de Pele / Tom de Pele /<br/>Tipo de Produto / Acabamento /<br/>Faixa de Preço / Ocasião]
    H --> I[Rankear produtos por relevância]
    I --> J[Exibir lista de recomendações]
    J --> K{Usuário interage?}
    K -->|Visualiza produto| L[Exibir detalhes]
    K -->|Avalia| M[Registrar feedback]
    L --> N{Produto atende?}
    N -->|Sim| M
    N -->|Não| J
    M --> O[Aprimorar modelo de recomendação]
    O --> G
"@ -OutputName "03-fluxo-recomendacao"

# 4. Casos de Uso
Get-MermaidImage -MermaidCode @"
graph TB
    subgraph "Sistema de Recomendação de Maquiagem"
        UC1[Realizar Cadastro]
        UC2[Realizar Login]
        UC3[Responder Questionário]
        UC4[Visualizar Recomendações]
        UC5[Filtrar Produtos]
        UC6[Visualizar Detalhes do Produto]
        UC7[Avaliar Produto]
        UC8[Gerenciar Catálogo]
        UC9[Gerenciar Perfil Profissional]
        UC10[Atualizar Preferências]
        UC11[Ver Histórico]

        UC1 --> UC3
        UC3 --> UC4
        UC5 --> UC4
    end

    subgraph "Atores"
        USUARIO[Usuário Cliente]
        PROF[Profissional]
        ADMIN[Administrador]
    end

    USUARIO --> UC1
    USUARIO --> UC2
    USUARIO --> UC3
    USUARIO --> UC4
    USUARIO --> UC5
    USUARIO --> UC6
    USUARIO --> UC7
    USUARIO --> UC10
    USUARIO --> UC11
    PROF --> UC1
    PROF --> UC2
    PROF --> UC9
    ADMIN --> UC8
    ADMIN --> UC2
"@ -OutputName "04-casos-de-uso"

# 5. Modelo Entidade-Relacionamento
Get-MermaidImage -MermaidCode @"
erDiagram
    USERS {
        int id PK
        string name
        string email UK
        string password_hash
        enum role
        string phone
        timestamp created_at
        timestamp updated_at
    }

    PROFESSIONAL_PROFILES {
        int id PK
        int user_id FK
        string specialty
        int experience_years
        text bio
        string photo_url
    }

    SKIN_TYPES {
        int id PK
        string name
        string description
    }

    SKIN_TONES {
        int id PK
        string name
        string hex_code
        int order
    }

    PRODUCT_TYPES {
        int id PK
        string name
        string category
        string icon
    }

    FINISHES {
        int id PK
        string name
        string description
    }

    OCCASIONS {
        int id PK
        string name
        string description
    }

    PRICE_RANGES {
        int id PK
        string name
        decimal min_value
        decimal max_value
    }

    BRANDS {
        int id PK
        string name
        text description
        string logo_url
    }

    PRODUCTS {
        int id PK
        string name
        text description
        int brand_id FK
        int product_type_id FK
        int finish_id FK
        decimal price
        string image_url
        int price_range_id FK
        boolean is_active
        timestamp created_at
    }

    PRODUCT_SKIN_TYPES {
        int product_id FK
        int skin_type_id FK
    }

    PRODUCT_SKIN_TONES {
        int product_id FK
        int skin_tone_id FK
    }

    PRODUCT_OCCASIONS {
        int product_id FK
        int occasion_id FK
    }

    USER_PREFERENCES {
        int id PK
        int user_id FK
        int skin_type_id FK
        int skin_tone_id FK
        int price_range_id FK
        timestamp created_at
        timestamp updated_at
    }

    USER_PREFERENCE_PRODUCT_TYPES {
        int preference_id FK
        int product_type_id FK
    }

    USER_PREFERENCE_OCCASIONS {
        int preference_id FK
        int occasion_id FK
    }

    USER_PREFERENCE_FINISHES {
        int preference_id FK
        int finish_id FK
    }

    RECOMMENDATIONS {
        int id PK
        int user_id FK
        timestamp created_at
    }

    RECOMMENDATION_ITEMS {
        int id PK
        int recommendation_id FK
        int product_id FK
        float relevance_score
    }

    FEEDBACKS {
        int id PK
        int user_id FK
        int product_id FK
        int rating
        text comment
        timestamp created_at
    }

    USERS ||--o{ PROFESSIONAL_PROFILES : possui
    USERS ||--o{ USER_PREFERENCES : possui
    USERS ||--o{ RECOMMENDATIONS : recebe
    USERS ||--o{ FEEDBACKS : registra

    USER_PREFERENCES ||--|| SKIN_TYPES : define
    USER_PREFERENCES ||--|| SKIN_TONES : define
    USER_PREFERENCES ||--|| PRICE_RANGES : define
    USER_PREFERENCES ||--o{ USER_PREFERENCE_PRODUCT_TYPES : inclui
    USER_PREFERENCES ||--o{ USER_PREFERENCE_OCCASIONS : inclui
    USER_PREFERENCES ||--o{ USER_PREFERENCE_FINISHES : inclui

    USER_PREFERENCE_PRODUCT_TYPES ||--|| PRODUCT_TYPES : refere-se
    USER_PREFERENCE_OCCASIONS ||--|| OCCASIONS : refere-se
    USER_PREFERENCE_FINISHES ||--|| FINISHES : refere-se

    PRODUCTS ||--|| BRANDS : pertence
    PRODUCTS ||--|| PRODUCT_TYPES : categorizado
    PRODUCTS ||--|| FINISHES : possui
    PRODUCTS ||--|| PRICE_RANGES : enquadra
    PRODUCTS ||--o{ PRODUCT_SKIN_TYPES : adequado
    PRODUCTS ||--o{ PRODUCT_SKIN_TONES : adequado
    PRODUCTS ||--o{ PRODUCT_OCCASIONS : indicado
    PRODUCTS ||--o{ FEEDBACKS : avaliado

    PRODUCT_SKIN_TYPES ||--|| SKIN_TYPES : refere-se
    PRODUCT_SKIN_TONES ||--|| SKIN_TONES : refere-se
    PRODUCT_OCCASIONS ||--|| OCCASIONS : refere-se

    RECOMMENDATIONS ||--o{ RECOMMENDATION_ITEMS : contem
    RECOMMENDATION_ITEMS ||--|| PRODUCTS : refere-se
"@ -OutputName "05-modelo-dados"

# 6. Fluxo de Autenticacao (sequencia)
Get-MermaidImage -MermaidCode @"
sequenceDiagram
    participant U as Usuário (Mobile)
    participant APP as React Native App
    participant API as FastAPI Backend
    participant DB as PostgreSQL

    U->>APP: Acessa o app
    APP->>API: POST /auth/login<br/>{email, password}
    API->>DB: SELECT * FROM users<br/>WHERE email = ?
    DB-->>API: Dados do usuário
    API->>API: Verificar password<br/>com bcrypt
    API->>API: Gerar token JWT
    API-->>APP: {token, user}
    APP->>APP: Armazenar token<br/>no secure storage
    APP-->>U: Tela principal
"@ -OutputName "06-fluxo-autenticacao"

# 7. Fluxo de Recomendacao (sequencia)
Get-MermaidImage -MermaidCode @"
sequenceDiagram
    participant U as Usuário
    participant APP as Mobile App
    participant API as Backend
    participant DB as PostgreSQL

    U->>APP: Acessa tela de<br/>recomendações
    APP->>API: GET /recommendations<br/>{token}
    API->>API: Decodificar token JWT
    API->>DB: SELECT preferências<br/>do usuário
    DB-->>API: skin_type, skin_tone,<br/>product_types, etc.
    API->>DB: SELECT produtos com JOINs<br/>WHERE correspondem<br/>às preferências
    DB-->>API: Lista de produtos
    API->>API: Calcular relevance_score<br/>para cada produto
    API-->>APP: {products: [...], total}
    APP->>APP: Renderizar lista<br/>de produtos
    APP-->>U: Lista de<br/>recomendações
"@ -OutputName "07-fluxo-recomendacao-seq"

# 8. Fluxo de Avaliacao (sequencia)
Get-MermaidImage -MermaidCode @"
sequenceDiagram
    participant U as Usuário
    participant APP as Mobile App
    participant API as Backend
    participant DB as PostgreSQL

    U->>APP: Seleciona produto
    APP->>API: GET /products/{id}
    API-->>APP: Detalhes do produto
    APP-->>U: Tela de detalhes
    U->>APP: Avalia produto<br/>(nota + comentário)
    APP->>API: POST /feedbacks<br/>{product_id, rating, comment}
    API->>DB: INSERT INTO feedbacks
    DB-->>API: Confirmação
    API-->>APP: {success: true}
    APP-->>U: Confirmação visual
"@ -OutputName "08-fluxo-avaliacao"

Write-Output ""
Write-Output "Todos os diagramas gerados com sucesso!"
