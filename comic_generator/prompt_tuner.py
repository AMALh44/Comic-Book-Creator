from transformers import pipeline

emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)

def tune_prompt(scene, style="cartoon"):
    try:
        result = emotion_classifier(scene)
        if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list) and len(result[0]) > 0:
            emotion = result[0][0].get("label", "neutral").lower()
        else:
            raise TypeError("Unexpected structure returned by emotion classifier")
    except Exception as e:
        print(f"⚠️ Emotion detection failed: {e}")
        emotion = "neutral"

    prompt = f"{style} style, {emotion} mood, scene: {scene[:120]}"
    print(f"🧠 Emotion: {emotion} | Prompt: {prompt}")
    return emotion, prompt