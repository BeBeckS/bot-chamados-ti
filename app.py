from flask import Flask, request
import requests

app = Flask(__name__)

API_KEY = "AIzaSyBe6szrB-hv8ZrnS25f758W_twZPNU8J9U"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

@app.route("/", methods=["GET"])
def index():
    return "Bot de chamados da Prefeitura ativo!"

@app.route("/responder", methods=["POST"])
def responder_post():
    # Tenta pegar JSON, se não existir pega texto cru
    dados = request.json
    if dados and "message" in dados:
        mensagem_usuario = dados["message"]
    else:
        mensagem_usuario = request.data.decode("utf-8") or ""

    prompt = f"""
Você é um assistente virtual da Prefeitura de Santa Bárbara do Sul, responsável exclusivamente por registrar chamados de TI.

⚠️ Sua única função é ajudar usuários a abrir chamados. Qualquer outra conversa deve ser gentilmente redirecionada para o tema de chamados.

Link para registro manual:
https://prefeitura.pethos.com.br/index.php/client

Fluxo obrigatório:
1. Perguntar: “Qual a prioridade deste chamado?” (A. Baixa / B. Média / C. Alta / D. Urgente)
2. Perguntar: “Qual a categoria?” com 10 opções
3. Solicitar:
   - Nome completo
   - Departamento ou setor
   - Localização (prédio)
4. Solicitar descrição detalhada do problema:
   - O que está acontecendo
   - Desde quando
   - O que tentou
   - Mensagens de erro (se houver)
   - Imagens ou prints (se possível)
5. Esperar o usuário digitar “Ok”
6. Gerar um resumo claro com todas as informações

Mensagem inicial (se o usuário digitar “Chamado” ou qualquer outra coisa):
“Olá! Bem-vindo(a) ao atendimento da Prefeitura de Santa Bárbara do Sul.
Sempre que precisar abrir um novo chamado de suporte técnico, digite Chamado.
Ou, se preferir, você mesmo pode registrar diretamente pelo sistema:
https://prefeitura.pethos.com.br/index.php/client
”

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

    # Retorna texto puro para o AutoReply entender
    return resposta_texto, 200, {"Content-Type": "text/plain"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
