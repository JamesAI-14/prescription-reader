from flask import Flask, request, jsonify, render_template
from google import genai
import PIL.Image
import io
import os
import base64

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/read", methods=["POST"])
def read_prescription():
    file = request.files["image"]
    image = PIL.Image.open(io.BytesIO(file.read()))

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=[
            "Read this prescription image and reply using ONLY this exact format below. "
            "Do NOT use any asterisks, hashtags, dashes, bold text, or markdown. "
            "Do NOT add any extra information or disclaimers. "
            "Just fill in the blanks using plain text only:\n\n"
            "PATIENT NAME: \n"
            "AGE: \n"
            "DATE: \n"
            "DOCTOR: \n"
            "CLINIC: \n"
            "CONTACT: \n\n"
            "SYMPTOMS:\n"
            "\n"
            "VITALS:\n"
            "Blood Pressure: \n"
            "Heart Rate: \n"
            "Temperature: \n"
            "SPO2: \n"
            "\n"
            "MEDICATIONS:\n"
            "1. [Medicine name] [dosage] - [instructions]\n"
            "2. [Medicine name] [dosage] - [instructions]\n"
            "3. [Medicine name] [dosage] - [instructions]\n"
            "\n"
            "SPECIAL INSTRUCTIONS:\n"
            "\n"
            "Use simple plain English only. No symbols. No extra text.",
            image,
        ]
    )

    return jsonify({"result": response.text})

if __name__ == "__main__":
    app.run(debug=True)
