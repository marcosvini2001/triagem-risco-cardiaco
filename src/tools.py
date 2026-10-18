import os
import joblib
import pandas as pd

# Caminho para o modelo treinado
MODEL_PATH = os.path.abspath("models/modelo_risco.pkl")

def carregar_modelo():
    """
    Carrega o modelo RandomForestClassifier treinado.
    Nota de Segurança: O modelo foi treinado e exportado internamente neste projeto acadêmico.
    O uso de joblib.load é seguro neste contexto controlado de ambiente de desenvolvimento local.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Modelo não encontrado em {MODEL_PATH}")
    return joblib.load(MODEL_PATH)

def analisar_risco(dados_vitais):
    """
    Prediz o risco com base nos sinais vitais.
    """
    modelo = carregar_modelo()
    df = pd.DataFrame([dados_vitais])
    score = modelo.predict_proba(df)[0][1] 
    return float(score)

def obter_protocolo(dados_paciente):
    """
    Avalia os sinais vitais do paciente contra as regras clínicas 
    e devolve a lista exata de protocolos acionados.
    """
    protocolos_sugeridos = []
    
    if dados_paciente.get('spo2_media', 100) < 88:
        protocolos_sugeridos.append("Se SPO2 < 88% → iniciar suporte respiratório imediato")
        
    if dados_paciente.get('carga_sistema', 0) > 85:
        protocolos_sugeridos.append("Se carga do sistema > 85% → abrir unidades temporárias")
        
    if dados_paciente.get('fc_media', 0) > 120:
        protocolos_sugeridos.append("Se FC > 120 → iniciar monitoramento intensivo")
        
    if dados_paciente.get('eventos_24h', 0) > 5:
        protocolos_sugeridos.append("Se eventos_24h > 5 → ativar equipe de resposta rápida")
        
    if dados_paciente.get('disponibilidade_recursos', 100) < 30:
        protocolos_sugeridos.append("Se disponibilidade_recursos < 30% → redistribuir insumos")
        
    if dados_paciente.get('tempo_espera', 0) > 90:
        protocolos_sugeridos.append("Se tempo_espera > 90 min → priorizar triagem emergencial")
        
    if dados_paciente.get('temperatura', 36) > 38:
        protocolos_sugeridos.append("Se temperatura > 38°C média → iniciar protocolo infeccioso")
        
    if dados_paciente.get('densidade_eventos', 0) > 6:
        protocolos_sugeridos.append("Se densidade_eventos > 6 → ativar plano de contingência")
        
    if dados_paciente.get('pa_sistolica', 120) < 90:
        protocolos_sugeridos.append("Se PA sistólica < 90 → iniciar protocolo de choque")
        
    if not protocolos_sugeridos:
        protocolos_sugeridos.append("Nenhum protocolo específico acionado.")
        
    return protocolos_sugeridos