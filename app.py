from flask import Flask, render_template, request, send_file
import os, uuid
import nltk
from nltk.tokenize import sent_tokenize
from comic_generator.prompt_tuner import tune_prompt
from comic_generator.image_generator import generate_image_with_bubble
from comic_generator.pdf_maker import build_comic_pdf

nltk.download('punkt')
app = Flask(__name__)

def split_story(story):
    sentences = sent_tokenize(story)
    scenes, temp = [], ""
    for i, sentence in enumerate(sentences):
        temp += sentence + " "
        if (i + 1) % 2 == 0:
            scenes.append(temp.strip())
            temp = ""
    if temp: scenes.append(temp.strip())
    return scenes

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        story = request.form["story"]
        style = request.form.get("style", "cartoon")
        title = request.form.get("title", "My Comic")
        output_dir = "static/generated"
        os.makedirs(output_dir, exist_ok=True)

        scenes = split_story(story)
        panel_data = []
        for idx, scene in enumerate(scenes):
            emotion, prompt = tune_prompt(scene, style)
            image_path = generate_image_with_bubble(scene, prompt, output_dir, idx)
            panel_data.append((scene, image_path))

        pdf_path = build_comic_pdf(panel_data, output_dir, title)
        return send_file(pdf_path, as_attachment=True)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
