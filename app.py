from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "AIzaSyBe6szrB-hv8ZrnS25f758W_twZPNU8J9U"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

@app.route("/responder", methods=["POST"])
def responder():
    dados = request.json
    mensagem_usuario = dados.get("mensagem") or dados.get("message", "")

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

        return jsonify({"resposta": resposta_texto})

    except Exception as e:
        return jsonify({"resposta": f"Erro ao gerar resposta: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
