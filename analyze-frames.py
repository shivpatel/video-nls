import os
import base64
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llava"

def analyze_image_with_ollama(image_path):
    with open(image_path, "rb") as img_file:
        image_bytes = img_file.read()

    # Proper Base64 encoding of the image
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    # Send to Ollama
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": "You are a helpful assistant that analyzes images and provides a detailed description of the scene to a blind person. Return only the description and make sure to mention notable objects, celebrities, the setting, mood, emotions, actions, time of day, weather, notable features, and on-screen text when applicable.",
        # "prompt": """
        #         Analyze the contents of this image and provide a detailed JSON object describing only factual and observable elements.

        #         Include the following fields:
        #         - `objects`: List of recognizable physical items in the scene (e.g. "red car", "traffic light", "coffee mug").
        #         - `people`: List of people or characters in the scene, including known celebrities or general descriptors (e.g. "young man", "woman with glasses", "Barack Obama").
        #         - `setting`: The type of environment (e.g. "urban street", "beach", "kitchen", "concert").
        #         - `mood`: A few keywords to describe the emotional tone (e.g. "tense", "joyful", "melancholic").
        #         - `emotions`: Observable emotional expressions from people in the scene (e.g. "smiling", "crying", "angry").
        #         - `actions`: Key actions or motions visible (e.g. "running", "hugging", "driving").
        #         - `time_of_day`: Estimate (e.g. "morning", "sunset", "night").
        #         - `weather`: If outdoors, describe weather (e.g. "sunny", "rainy", "snowy").
        #         - `notable_features`: Any unique, unusual, or prominent visual elements that stand out.
        #         - `text`: Any visible text or signage in the image (e.g. "STOP sign", "Cafe Aroma").

        #         Be factual and avoid speculation. Return only the JSON output.
        #         """,
        "images": [image_b64],
        "stream": False
    })

    if response.status_code == 200:
        result = response.json()
        return result.get("response", "").strip()
    else:
        print(f"Error analyzing {image_path}: {response.status_code} {response.text}")
        return None

def process_images_in_folder(folder_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith(".jpg"):
            img_path = os.path.join(folder_path, filename)
            print(f"Analyzing {filename}...")
            description = analyze_image_with_ollama(img_path)
            if description:
                output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
                with open(output_file, "w") as f:
                    f.write(description)
                print(f"Saved description to {output_file}")
                # exit()

# Example usage
process_images_in_folder("./scene_keyframes", "descriptions")