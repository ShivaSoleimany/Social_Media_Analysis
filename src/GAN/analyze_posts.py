import os
import json
from openai import AsyncOpenAI, OpenAIError

async def analyze_post_texts(bio, post_texts):

    print("analyze_post_texts")

    post_texts_str = f"<{post_texts}>"
    bio = f"||{bio}||"

    with open('/Users/shiva/Desktop/Courses/twitter/src/GAN/templates/analyze_post_texts.txt', 'r') as file:
        prompt_template = file.read()

    prompt = prompt_template.format(bio=bio, post_texts_str=post_texts_str)

    async with AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY')) as client:
        try:
            response = await client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-4",
                # model="gpt-4-vision-preview",
            )
            data = response.choices[0].message.content
            results = json.loads(data)
            return_results = {key: results.get(key) for key in ["gender", "life_stage", "nationality", "ethnicity", "personality", "explanation"]}
            return return_results
        except OpenAIError as e:
            print(f"OpenAI API Error: {e}")
            return {key: None for key in ["gender", "life_stage", "nationality", "ethnicity", "personality", "explanation"]}


async def analyze_post_images(image_urls):

    print("analyze_post_images")

    with open('/Users/shiva/Desktop/Courses/twitter/src/GAN/templates/analyze_post_images.txt', 'r') as file:
        prompt_text = file.read()

    print("prompt_text", prompt_text)

    messages = [{
        "role": "user",
        "content": [
            {"type": "text", "text": prompt_text}
        ] + [
            {"type": "image_url", "image_url": {"url": url}} for url in image_urls
        ]
    }]

    async with AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY')) as client:
        try:
            response = await client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=messages,
                max_tokens=300,
            )
            if response:
                cleaned_data = response.choices[0].message.content
                print("cleaned_data", cleaned_data, "\n-----------------------------------")
                # parsed_json = json.loads(cleaned_data)
            return cleaned_data
        except OpenAIError as e:
            print(f"OpenAI API Error: {e}")
            return []


async def analyze_all_information(text_results, image_results):

    print("analyze_all_information")

    text_results_str = json.dumps(text_results)

    image_results_str = json.dumps(image_results)

    with open('/Users/shiva/Desktop/Courses/twitter/src/GAN/templates/extract_information.txt', 'r') as file:
        prompt_template = file.read()

    prompt = prompt_template.format(text_results_str=text_results_str, image_results_str=image_results_str)
    print(f"prompt:{prompt}")

    async with AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY')) as client:
        try:
            response = await client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-4",
                # model="gpt-4-vision-preview",
            )
            data = response.choices[0].message.content
            results = json.loads(data.strip('`\n'))
            return_results = {key: results.get(key) for key in ["gender", "life_stage", "hair_length", "hair_color", "hair_texture", "face_shape", "nationality", "ethnicity", "personality", "vibe", "explanation"]}
            return return_results
        except OpenAIError as e:
            print(f"OpenAI API Error: {e}")
            return {key: None for key in ["gender", "life_stage", "hair_length", "hair_color", "hair_texture", "face_shape", "nationality", "ethnicity", "personality", "vibe", "explanation"]}

