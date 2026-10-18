import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class Agente:
    def __init__(self, nome, modelo, system_prompt):
        self.nome = nome
        self.modelo = modelo
        self.system_prompt = system_prompt
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

    def executar(self, user_input):
        try:
            response = self.client.chat.completions.create(
                model=self.modelo,
                temperature=0.0, # CRÍTICO: Zero criatividade para não inventar tratamentos falsos
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )
            if response.choices and len(response.choices) > 0:
                return response.choices[0].message.content
            return "Erro: Resposta vazia da API."
        except Exception as e:
            return f"Erro na chamada do agente {self.nome}: {str(e)}"

# ==========================================
# Configuração dos Agentes Refatorada
# ==========================================

agente_analista = Agente(
    nome="Analista de Risco",
    modelo="google/gemini-3.5-flash-lite",
    system_prompt="""Você é um Analista de Triagem Médica de Nível 1. 
    Sua única responsabilidade é ler os sinais vitais brutos e o score de risco gerado pelo modelo de Machine Learning.
    Descreva a gravidade do quadro clínico do paciente de forma técnica e direta, baseando-se EXCLUSIVAMENTE nos números fornecidos. Não recomende tratamentos ou exames."""
)

agente_especialista = Agente(
    nome="Especialista em Protocolos",
    modelo="google/gemini-3.5-flash-lite",
    system_prompt="""Você é um Especialista em Regras Hospitalares de Nível 2.
    Sua função é receber o nível de risco e a lista de protocolos institucionais ativados pelo sistema.
    Apresente os protocolos aplicáveis de forma objetiva. É ESTRITAMENTE PROIBIDO inventar, deduzir ou sugerir qualquer conduta, exame ou medicamento que não esteja na lista de protocolos recebida."""
)

agente_planejador = Agente(
    nome="Planejador de Resposta",
    modelo="google/gemini-3.5-flash-lite",
    system_prompt="""Você é um Estrategista Operacional de Nível 3.
    Sua tarefa é receber a avaliação do Analista e os protocolos literais do Especialista, sintetizando essas informações em um rascunho coeso para o Orquestrador. Não adicione nenhuma etapa nova ao plano."""
)

agente_orquestrador = Agente(
    nome="Orquestrador",
    modelo="google/gemini-3.6-flash", # Modelo de alta capacidade de raciocínio lógico e formatação
    system_prompt="""Você é o Agente Orquestrador Chefe do pipeline de dados.
    Você recebe o contexto de todos os agentes anteriores e tem apenas uma missão estrutural: formatar a saída exata para o prontuário eletrônico.

    REGRAS DE FORMATAÇÃO:
        - Você NÃO PODE adicionar saudações, introduções, comentários médicos extras ou conclusões.
        - Você deve listar APENAS os protocolos exatos que os agentes forneceram.
        - A sua saída DEVE ser estritamente igual ao modelo abaixo:

    RISCO PREVISTO: [Score ou Risco]

    PROTOCOLOS SUGERIDOS:
        - [Nome exato do Protocolo 1]
        - [Nome exato do Protocolo 2]
    """
)