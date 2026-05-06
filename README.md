# Traductor ES → IT (HTML interactivo + Qwen2-0.5B-Instruct)

🌐 **Demo en vivo:** https://emilioram1.github.io/app-traductora/
> Corre directo en el navegador, sin servidor. El modelo se descarga la primera vez (~75 MB) y queda en caché.
<img width="2548" height="1327" alt="image" src="https://github.com/user-attachments/assets/130b9408-7402-424b-ae3e-8b7ffd985202" />

App web pequeña que traduce de **español a italiano** usando el modelo
**`Qwen/Qwen2-0.5B-Instruct`** corriendo localmente. Backend en Flask,
frontend HTML/CSS/JS (sin frameworks).

Curso: **CD3002C.601 — Modelos de IA para Datos No Estructurados**

---

## Cómo correrlo

### 1. Crear entorno e instalar dependencias

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Levantar el servidor

```bash
python app.py
```

Cuando termine de cargar el modelo verás:

```
Modelo listo. Abre http://127.0.0.1:5000 en el navegador.
```

### 3. Abrir en el navegador

Vas a `http://127.0.0.1:5000` y ya. Puedes:

- Hacer clic en cualquiera de los **3 ejemplos** (`Me gusta el fútbol`,
  `¿Cómo estás?`, `¿Qué hora es?`) para traducir al instante.
- Escribir tu propio texto en español en el panel izquierdo y darle
  **Traducir** (o `Ctrl + Enter` / `Cmd + Enter`).
- La traducción aparece en el panel derecho.

> La primera vez que corras `app.py` descargará el modelo (~1 GB) desde
> Hugging Face. Las siguientes veces ya queda en caché y abre rápido.

---

## Cómo funciona (en una corrida)

```
[ Browser ]
   │  POST /translate  { "text": "Me gusta el fútbol" }
   ▼
[ Flask app.py ]
   │  apply_chat_template + system prompt "Spanish → Italian"
   ▼
[ Qwen/Qwen2-0.5B-Instruct ]
   │  generate(max_new_tokens=128, do_sample=False)
   ▼
[ Browser ]   { "translation": "Mi piace il calcio" }
```

`do_sample=False` (greedy) → traducción determinista, reproducible.

---

## Versión estática (GitHub Pages)

`index.html` en la raíz usa **Transformers.js** para correr el modelo
**`Helsinki-NLP/opus-mt-es-it`** directo en el navegador, sin backend.

```
[ Browser ]
   │  escribe texto en español
   ▼
[ Transformers.js · Xenova/opus-mt-es-it · ONNX en WebAssembly ]
   │  inference local en el navegador
   ▼
[ Browser ]   traduzione in italiano
```

---

## Archivos

```
app-traductora/
├── index.html          # versión estática (GitHub Pages, sin servidor)
├── app.py              # backend Flask + Qwen2 (versión local)
├── templates/
│   └── index.html      # UI para la versión Flask
├── requirements.txt    # flask, transformers, torch, accelerate
└── README.md
```

---

## Notas

- Qwen2-0.5B es chico (0.5B parámetros), así que en frases de cajón
  funciona bien pero en oraciones largas o con argot puede equivocarse.
- El system prompt está en inglés porque Qwen2 sigue mejor instrucciones
  en inglés; eso no afecta el idioma de salida (sigue traduciendo a
  italiano).
- Si quieres probar otro par de idiomas, cambia la línea del
  system prompt en `app.py`:
  `"Translate the user's text from Spanish to Italian."`
