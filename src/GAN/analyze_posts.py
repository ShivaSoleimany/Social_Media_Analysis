import os
import json
import logging
from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAIError

load_dotenv()
def load_templates():
    template_paths = {
        "analyze_post_texts": "/Users/shiva/Desktop/Courses/twitter/src/GAN/templates/analyze_post_texts.txt",
        "analyze_post_images": "/Users/shiva/Desktop/Courses/twitter/src/GAN/templates/analyze_post_images.txt",
        "extract_information": "/Users/shiva/Desktop/Courses/twitter/src/GAN/templates/extract_information.txt"
    }
    templates = {}
    for key, path in template_paths.items():
        with open(path, 'r') as file:
            templates[key] = file.read()
    return templates

templates = load_templates()

def default_results(keys):
    return {key: None for key in keys}


async def analyze_post_texts(bio, post_texts):

    print("analyze_post_texts")

    prompt = templates["analyze_post_texts"].format(bio=f"||{bio}||", post_texts_str=f"<{post_texts}>")

    async with AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY')) as client:
        try:
            response = await client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-4o-mini")
            results = json.loads(response.choices[0].message.content)

            print(f"analyze_post_texts results:{results}")
            return  {key: results.get(key) for key in ["gender", "life_stage", "nationality", "ethnicity", "personality", "explanation"]}

        except OpenAIError as e:
            print(f"OpenAI API Error: {e}")
            return default_results(["gender", "life_stage", "nationality", "ethnicity", "personality", "explanation"])

async def analyze_post_images(image_urls):

    print("analyze_post_texts")

    prompt = templates["analyze_post_images"]

    messages = [{
        "role": "user",
        "content": [ {"type": "text", "text": prompt}] + 
        [{"type": "image_url", "image_url": {"url": url}} for url in image_urls ]
            }]

    async with AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY')) as client:
        try:
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=300,
            )
            if response:
                result = response.choices[0].message.content
                print("result", result, "\n-----------------------------------")
            return result
        except OpenAIError as e:
            print(f"OpenAI API Error: {e}")
            return []

async def analyze_all_information(text_results, image_results):

    print("analyze_all_information")

    text_results_str = json.dumps(text_results)
    image_results_str = json.dumps(image_results)

    prompt = templates["extract_information"].format(text_results_str=text_results_str, image_results_str=image_results_str)

    async with AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY')) as client:
        try:
            response = await client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-4o-mini",
            )
            data = response.choices[0].message.content
            results = json.loads(data.strip('`\n'))
            return  {key: results.get(key) for key in ["gender", "life_stage", "hair_length", "hair_color", "hair_texture", "face_shape", "nationality", "ethnicity", "personality", "vibe", "explanation"]}
        except OpenAIError as e:
            print(f"OpenAI API Error: {e}")
            return default_results(["gender", "life_stage", "hair_length", "hair_color", "hair_texture", "face_shape", "nationality", "ethnicity", "personality", "vibe", "explanation"])

async def main():

    bio = "Sample Bio"
    post_texts = ["Post 1", "Post 2"]
    image_urls = ["http://example.com/image1.jpg", "http://example.com/image2.jpg"]

    text_results = await analyze_post_texts(bio, post_texts)
    image_results = await analyze_post_images(image_urls)
    all_results = await analyze_all_information(text_results, image_results)

    print("Final Results:", all_results)

if __name__ == "__main__":
    asyncio.run(main())