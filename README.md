# 🏥 Sistema Multiagente para Triagem de Risco Cardíaco

**Instituição:** FIAP - Fase 6 (2º Ano)  
**Projeto:** Predição de Pico de Risco Cardíaco com Inteligência Artificial e Orquestração de Agentes

## 📖 Sobre o Projeto
Este projeto integra Machine Learning clássico com a nova arquitetura de Agentes Autônomos baseados em LLMs (Large Language Models). O sistema foi projetado para atuar na triagem hospitalar inteligente, avaliando sinais vitais de pacientes para prever a probabilidade de um pico de risco cardíaco e acionar, de forma estruturada, os protocolos operacionais cabíveis.

O sistema é dividido em duas frentes:
1. **Machine Learning (`modelo_risco.pkl`):** Um modelo `RandomForestClassifier` treinado em uma base de dados sintética de 5.000 pacientes, responsável pela predição exata (Score).
2. **Sistema Multiagente (Python + OpenRouter):** Um pipeline sequencial (*handoff*) de 4 agentes cognitivos (Analista, Especialista, Planejador e Orquestrador) que interpretam o risco e formatam o laudo final segundo as regras de negócio do hospital.

## 🗂️ Estrutura do Repositório

```text
PROJETO_RISCO_CARDIACO/
 ┣ 📂 docs/
 ┃ ┗ 📜 relatorio_tecnico.pdf      # Documentação e análise de métricas do ML
 ┣ 📂 models/
 ┃ ┗ 🧠 modelo_risco.pkl           # Modelo Random Forest serializado
 ┣ 📂 notebooks/
 ┃ ┗ 📓 treinamento_modelo.ipynb   # Notebook de EDA e treinamento do modelo
 ┣ 📂 src/
 ┃ ┣ 📜 main.py                    # Script principal de execução e fluxo de handoff
 ┃ ┣ 📜 agents.py                  # Configuração dos Agentes e System Prompts (LLMs)
 ┃ ┗ 📜 tools.py                   # Funções Python utilizadas pelos agentes (Validação de Regras)
 ┣ 📜 .env                         # Variáveis de ambiente (IGNORADO NO GIT)
 ┣ 📜 requirements.txt             # Dependências do projeto
 ┗ 📜 README.md                    # Este arquivo
```

## ⚙️ Pré-requisitos
- Python 3.8 ou superior instalado.
- Chave de API do **OpenRouter** para inferência dos LLMs (família Google Gemini).

## 🚀 Como Configurar e Executar

**1. Instale as dependências**
Abra o terminal na pasta raiz do projeto e instale os pacotes listados:
```bash
pip install -r requirements.txt
```

**2. Configure as Variáveis de Ambiente**
Crie um arquivo chamado `.env` na raiz do projeto (mesmo nível do `requirements.txt`) e adicione a sua chave do OpenRouter:
```text
OPENROUTER_API_KEY="sk-or-v1-sua-chave-aqui"
```

**3. Execute a Orquestração**
Com o ambiente virtual ativado e as dependências instaladas, rode o script principal:
```bash
python src/main.py
```

## 📊 Saída Esperada (Exemplo)
O terminal exibirá o *log* do handoff entre os 5 passos do sistema, culminando no laudo estritamente formatado exigido pelos critérios do projeto:

```text
============================================================
RISCO PREVISTO: 0.95

PROTOCOLOS SUGERIDOS:
- Se disponibilidade_recursos < 30% → redistribuir insumos
- Se temperatura > 38°C média → iniciar protocolo infeccioso
============================================================
```

## 🛠️ Tecnologias Utilizadas
- **Pandas & Numpy:** Manipulação de dados estruturados.
- **Scikit-Learn & Joblib:** Treinamento e persistência do modelo preditivo.
- **OpenAI SDK:** Framework base de roteamento para comunicação com a API.
- **OpenRouter (Gemini Flash/Lite):** Motor cognitivo gratuito e ultrarrápido dos Agentes.