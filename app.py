"""
Traductor español -> italiano (HTML interactivo + Flask)
Modelo: Qwen/Qwen2-0.5B-Instruct
Curso: CD3002C.601 - Modelos de IA para Datos No Estructurados
"""

from flask import Flask, request, jsonify, render_template
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

MODEL_NAME = "Qwen/Qwen2-0.5B-Instruct"

app = Flask(__name__)

print(f"Cargando {MODEL_NAME} (la primera vez baja ~1GB)...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto",
    device_map="auto",
)
print("Modelo listo. Abre http://127.0.0.1:5000 en el navegador.\n")


def translate(text: str) -> str:
    """Traduce de español a italiano usando el chat template de Qwen2."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional translator. "
                "Translate the user's text from Spanish to Italian. "
                "Return ONLY the Italian translation. "
                "No quotes, no explanation, no source text, no notes."
            ),
        },
        {"role": "user", "content": text},
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=128,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

    new_tokens = outputs[0][inputs.input_ids.shape[1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate_endpoint():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"translation": ""})
    try:
        result = translate(text)
        return jsonify({"translation": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
