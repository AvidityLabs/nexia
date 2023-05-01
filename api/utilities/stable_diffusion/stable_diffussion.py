import os
import json
import openai
import requests

STABLE_DIFFUSION_API_KEY=os.environ.get('STABLE_DIFFUSION_API_KEY')

def generate_images(input):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[

            {"role": "user", "content": """You are an expert AI artist with over 30 years of experience

Here is a full matrix of styles, time periods, photography techniques, miscellaneous styles, artists, architects, color palettes, lighting, environment, and perspectives for you to utilize:

Style	Time Periods	Photography Techniques	Misc Styles	Artists	Architects	Color Palette	Lighting	Environment	Perspectives
Nouveau	Ancient Egypt	Macro Photography	Synthwave	Hayao Miyazaki	Frank Lloyd Wright	Bright Colors	Soft Light	Natural	Bird's Eye View
Film Noir	Ancient Greece	Tilt Shift	Polymer Clay	Peter Elson	Frank Gehry	Dark Colors	Hard Light	Urban	Worm's Eye View
Manga	Modern	Bokeh Effect	Cyberpunk	Katsuhiro Otomo	Zaha Hadid	Bold Colors	Mood Light	Futuristic	Isometric View
Post-Apocalyptic	Futuristic	Long Exposure	Pixel Art	Moebius	Mies van der Rohe	Desaturated	Spot Light	Dystopian	Low Angle View
Surrealism	Renaissance	High Dynamic Range	3D Printing	Salvador Dali	Le Corbusier	Dreamlike	Backlight	Cosmic	High Angle View
Abstract	Baroque	Panoramic	Pixel Sorting	Pablo Picasso	Antoni Gaudi	Geometric	Rim Light	Digital	Overhead View
Impressionism	Gothic	Timelapse	Collage	Claude Monet	Eero Saarinen	Pastel	Fill Light	Enchanted	Dutch Angle
Expressionism	Romanticism	Night Photography	Vexel Art	Edvard Munch	Philip Johnson	Intense	Key Light	Abstract	Worm's Eye View
Pop Art	Art Deco	Infrared	ASCII Art	Roy Lichtenstein	I. M. Pei	Bold Graphics	High-Key	Iconic	Eye Level View
Futurism	Art Nouveau	Long Exposure Light Painting	Low Poly	Umberto Boccioni	Santiago Calatrava	Futuristic	Low-Key	Technologic	Tilted View
Realism	Dadaism	Lens Flare	8-Bit Art	Johannes Vermeer	Norman Foster	Realistic	Shadow	Naturalistic	Oblique View
Minimalism	Abstract Expressionism	Silhouette	Vaporwave	Kazimir Malevich	Tadao Ando	Minimal	Flat Light	Simple	Front View
Gothic	Color Field	Action Photography	Aesthetic	Michelangelo	Frank Furness	Dark	Dramatic Light	Mysterious	Rear View
Romanticism	Hyperrealism	Zoom Blur	80's Retro	Caspar David Friedrich	Richard Rogers	Soft	Back Light	Nostalgic	Side View
Renaissance	Pop Surrealism	Slow Shutter	90's Grunge	Leonardo da Vinci	Foster + Partners	Rich	Spot Light	Cultural	Three-Quarter View
Baroque	Neo-Expressionism	Panning	Anime	Caravaggio	Thomas Heatherwick	Decorative	Key Light	Ornate	Full-Face View
Art Deco	Suprematism	Macro Action	Space Art	Tamara de Lempicka	Jean Nouvel	Elegant	High-Key	Glamorous	Half-Profile View
Art Nouveau	Futurism (Literary)	Time Warp	Dark Fantasy	Alph					

The goal is to create amazing and extremely detailed pictures that utilize the matrix above. When creating pictures, start a prompt with "/imagine prompt: "

/imagine prompt: A majestic lion , sits atop a rock formation, basking in the warm glow of a golden sunset . The surrounding grasslands stretch out as far as the eye can see, creating a vast and serene landscape . The lion's fur is painted in bold and striking colors, reminiscent of a Pop Art style . The composition of the image is a perfect balance between foreground and background, with the lion being the clear focal point, 4K,hyper detailed illustration,



Please keep this information in mind and generate a prompt about  """ + input}

        ]
    )

    try:
        promptGenerated = completion.choices[0].message.content

        # connect to stable diffusion API
        url = 'https://stablediffusionapi.com/api/v3/text2img'

        data = {
            "key": STABLE_DIFFUSION_API_KEY,
            "prompt": promptGenerated,
            "negative_prompt": "",
            "width": "512",
            "height": "512",
            "samples": "1",
            "num_inference_steps": "20",
            "seed": None,
            "guidance_scale": 7.5,
            "safety_checker": "yes",
            "webhook": None,
            "track_id": None
        }

        response = requests.post(url, json=data)
        JSONResult = json.loads(response.text)
        print("Generating Image...")
        imgURL = JSONResult["output"][0]
        return {
            "imgUrl": imgURL,
            "completion": completion
        }
    except Exception as e: 
        return None