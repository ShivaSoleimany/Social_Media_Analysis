import os
import json
from openai import AsyncOpenAI, OpenAIError
from playwright.async_api import async_playwright


async def generate_avatar(user_description):

    prompt = f"""
    I give you the user's description, in form of a dictionary. generate a headshot of that user in hyper realistic format.
    ## Instructions
    1. Do NOT write any text on the image.
    2. Generate the photo in square format and headshot format.
    {user_description}
    """

    async with AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY')) as client:
        try:
            image_response = await client.images.generate(prompt=prompt, model="dall-e-3", size="1024x1024", quality="standard", n=1)
            return image_response.data[0].url
        except OpenAIError as e:
            print(f"OpenAI API Error: {e}")
            return None
        
async def generate_post(user_description, user_posts):

    prompt = f"""
            I give you a user's description and some of user's previous tweets and post captions. Generate a post caption or a tweet this user is likely to post.

            ## Instructions
            . Make sure the text you generate is meaningful.
            . Generate the text in the language that most of user's tweets or post captions are in.
            . return the result in JSON format {{"post":"post"}}
            . Do NOT add any extra information to your returned value except the JSON output.
            . MAKE SURE your output in in JSON format.

        user_description: {user_description}

        user_posts: {user_posts}
        """

    async with AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY')) as client:
        try:
            response = await client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-4",
            )

            data = response.choices[0].message.content
            print(f"generate_post data:{data}")

            results = json.loads(data.strip('`\n'))
            print(f"generate_post results:{results}")

            post_text = results.get("post")
            return post_text
        except OpenAIError as e:
            print(f"OpenAI API Error: {e}")
            return None
