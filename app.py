
from flask import Flask, render_template, request, send_file
from indic_transliteration.sanscript import transliterate, DEVANAGARI, ITRANS
import os

app = Flask(__name__)

def clean_hinglish(text):
    skip_words = ['plan', 'idea', 'job', 'fun', 'camera']
    for word in skip_words:
        text = text.replace(transliterate(word, DEVANAGARI, ITRANS), word)
    return text

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    uploaded_file = request.files["file"]
    if uploaded_file.filename != "":
        srt_data = uploaded_file.read().decode("utf-8")
        converted_lines = []
        for line in srt_data.split("\n"):
            if line.strip() and not line.strip().replace(":", "").replace(",", "").replace("-->", "").replace(" ", "").isdigit():
                try:
                    transliterated = transliterate(line, DEVANAGARI, ITRANS)
                    transliterated = clean_hinglish(transliterated)
                    converted_lines.append(transliterated)
                except Exception:
                    converted_lines.append(line)
            else:
                converted_lines.append(line)
        output_path = os.path.join("static", "converted.srt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(converted_lines))
        return send_file(output_path, as_attachment=True)
    return "No file uploaded."

if __name__ == "__main__":
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
