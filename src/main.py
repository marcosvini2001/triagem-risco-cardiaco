import os
import warnings
from dotenv import load_dotenv

# Oculta avisos do scikit-learn sobre versões de persistência do modelo
warnings.filterwarnings("ignore")

from tools import analisar_risco, obter_protocolo
from agents import (
    agente_analista,
    agente_especialista,
    agente_planejador,
    agente_orquestrador
)

load_dotenv()

def executar_sistema_multiagente(dados_paciente):
    print("=" * 60)
    print("🏥 SISTEMA MULTIAGENTE DE RISCO CARDÍACO - FIAP")
    print("=" * 60)
    
    # 1. Predição ML
    score = analisar_risco(dados_paciente)
    protocolo_base = obter_protocolo(dados_paciente)
    
    # 2. Agente Analista de Risco
    prompt_analista = f"Dados vitais: {dados_paciente}. Score: {score:.2f}. Protocolos base: {protocolo_base}."
    analise_clinica = agente_analista.executar(prompt_analista)

    # 3. Agente Especialista
    prompt_especialista = f"Análise Clínica: {analise_clinica}. Protocolos da base: {protocolo_base}."
    diretrizes_protocolo = agente_especialista.executar(prompt_especialista)

    # 4. Agente Planejador
    prompt_planejador = f"Análise: {analise_clinica}. Diretrizes: {diretrizes_protocolo}."
    plano_acao = agente_planejador.executar(prompt_planejador)

    # 5. Agente Orquestrador (Consolidando o fluxo multiagente)
    print("[5/5] 👑 Agente Orquestrador consolidando a equipe e formatando saída...")
    
    prompt_orquestrador = f"""
    Você é o Agente Orquestrador. Leia os relatórios da sua equipe para entender o contexto, mas obedeça estritamente à Regra de Ouro da formatação final.
    
    --- CONTEXTO DA EQUIPE ---
    Analista: {analise_clinica}
    Especialista: {diretrizes_protocolo}
    Planejador: {plano_acao}
    
    --- DADOS TÉCNICOS EXATOS ---
    Score Calculado: {score:.2f}
    Protocolos Originais do Sistema: {protocolo_base}

    REGRA DE OURO PARA A SAÍDA: 
    Para preencher a seção 'PROTOCOLOS SUGERIDOS', você é OBRIGADO a copiar palavra por palavra da lista 'Protocolos Originais do Sistema'. Você NÃO PODE usar os textos do Analista ou do Planejador para preencher esta seção.

    Gere a resposta final EXATAMENTE assim:

    RISCO PREVISTO: {score:.2f}

    PROTOCOLOS SUGERIDOS:
    - [Copie o item 1 dos Protocolos Originais do Sistema]
    - [Copie o item 2 dos Protocolos Originais do Sistema]
    - [Continue copiando os demais itens, se houver]
    """
    
    relatorio_final = agente_orquestrador.executar(prompt_orquestrador)
    
    print("\n" + "=" * 60)
    print(relatorio_final)
    print("=" * 60 + "\n")

if __name__ == "__main__":
    # Dados do paciente crítico (risco de 98% conforme enunciado)
    paciente_teste = {
        'idade_media': 75.0,
        'carga_sistema': 0.95,
        'tempo_espera': 45.0,
        'fc_media': 120.0,
        'spo2_media': 88.0,
        'pa_sistolica': 180.0,
        'temperatura': 38.2,
        'densidade_eventos': 0.9,
        'eventos_24h': 5.0,
        'disponibilidade_recursos': 0.2
    }
    
    try:
        executar_sistema_multiagente(paciente_teste)
    except Exception as e:
        print(f"❌ Erro crítico na execução do fluxo: {e}")
