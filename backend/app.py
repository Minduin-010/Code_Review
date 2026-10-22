
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

# Define os caminhos do projeto.
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

# Configura o servidor e disponibiliza os arquivos do frontend.
app = Flask(
    __name__,
    static_folder=str(FRONTEND_DIR),
    static_url_path="/static"
)

# Configurações comerciais da loja.
CONFIG_LOJA = {
    "nome": "Nitro Sneakers",
    "taxa_frete": 30.00,
    "moeda": "BRL"
}

# Catálogo oficial de produtos e preços.
PRODUTOS = {
    "Nitro Max (M)": 300.00,
    "Nitro Pro (M)": 350.00,
    "Nitro Zoom (M)": 280.00,
    "Nitro Elite (M)": 400.00,
    "Nitro Air (F)": 300.00,
    "Nitro Glide (F)": 320.00,
    "Nitro Flex (F)": 290.00,
    "Nitro Aura (F)": 380.00
}


# Exibe a página inicial da loja.
@app.route("/")
def pagina_inicial():
    return send_from_directory(FRONTEND_DIR, "index.html")


# Recebe uma compra e calcula o total no backend.
@app.route("/api/compras", methods=["POST"])
def realizar_compra():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({
            "erro": "Envie os dados da compra em formato JSON."
        }), 400

    nome_produto = dados.get("nome")

    # Valida o produto usando o catálogo oficial.
    if not isinstance(nome_produto, str) or nome_produto not in PRODUTOS:
        return jsonify({
            "erro": "Produto inválido ou não encontrado."
        }), 400

    preco = PRODUTOS[nome_produto]
    frete = CONFIG_LOJA["taxa_frete"]
    total = round(preco + frete, 2)

    # Retorna os valores calculados pelo servidor.
    return jsonify({
        "loja": CONFIG_LOJA["nome"],
        "produto": nome_produto,
        "preco": preco,
        "frete": frete,
        "total": total,
        "moeda": CONFIG_LOJA["moeda"],
        "mensagem": "Compra calculada com sucesso."
    }), 200


# Inicia o servidor local.
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
