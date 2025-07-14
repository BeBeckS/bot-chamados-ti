from flask import Flask, request
import requests

app = Flask(__name__)

API_KEY = "AIzaSyBe6szrB-hv8ZrnS25f758W_twZPNU8J9U"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

@app.route("/", methods=["GET"])
def index():
    return "Bot de chamados da Prefeitura ativo!"

@app.route("/responder", methods=["POST"])
def responder():
    # Suporta texto puro ou JSON
    dados = request.json
    if dados and "message" in dados:
        mensagem_usuario = dados["message"]
    else:
        mensagem_usuario = request.data.decode("utf-8") or ""

    prompt = f"""
Você é um assistente virtual da Prefeitura de Santa Bárbara do Sul, responsável exclusivamente por registrar chamados de TI.

⚠️ Sua única função é ajudar usuários a abrir chamados. Qualquer outro tipo de conversa deve ser redirecionada para o assunto "chamado".

Link para registro manual: https://prefeitura.pethos.com.br/index.php/client

Fluxo obrigatório:
1. Perguntar: “Qual a prioridade deste chamado?” (A. Baixa / B. Média / C. Alta / D. Urgente)
2. Perguntar: “Qual a categoria?” com 10 opções
3. Solicitar:
   - Nome completo
   - Departamento ou setor
   - Localização (prédio)
4. Solicitar descrição detalhada:
   - O que está acontecendo
   - Desde quando
   - O que tentou
   - Mensagens de erro
   - Prints ou fotos, se possível
5. Esperar "Ok" do usuário
6. Gerar resumo claro e organizado

Mensagem inicial:
“Olá! Bem-vindo(a) ao atendimento da Prefeitura de Santa Bárbara do Sul.
Sempre que precisar abrir um novo chamado, digite *Chamado*.
Ou registre manualmente: https://prefeitura.pethos.com.br/index.php/client”

Usuário: {mensagem_usuario}
Resposta:
"""

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}],
                "role": "user"
            }
        ]
    }

    try:
        resposta = requests.post(
            f"{API_URL}?key={API_KEY}",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        dados_resposta = resposta.json()
        resposta_texto = dados_resposta["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        resposta_texto = f"Erro ao gerar resposta: {str(e)}"

    return resposta_texto, 200, {"Content-Type": "text/plain"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
