import asyncio
import os
from openai import AsyncOpenAI, OpenAIError
from playwright.async_api import async_playwright

from dotenv import load_dotenv

load_dotenv()

async def extract_bio(page):
    selector = 'div[data-testid="UserDescription"]'
    element = await page.query_selector(selector)

    bio_text = await element.inner_text() if element else "Bio not found"
    return bio_text

async def extract_tweet_image_url(post_element):
    try:
        image_selector = 'img[alt="Image"]'
        image_element = await post_element.query_selector(image_selector)
        return await image_element.get_attribute('src') if image_element else None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

async def extract_tweet_texts(post_element):
    inner_selector = 'div[data-testid="tweetText"]'
    inner_elements = await post_element.query_selector_all(inner_selector)

    tweets = [await element.inner_text() for element in inner_elements]
    return tweets

async def extract_tweets(page):
    outer_selector = 'div[data-testid="cellInnerDiv"]'
    outer_elements = await page.query_selector_all(outer_selector)

    tweet_texts, tweet_image_urls = [], []
    for post_element in outer_elements:
        tweet_texts.extend(await extract_tweet_texts(post_element))
        tweet_image_url = await extract_tweet_image_url(post_element)
        if tweet_image_url:
            tweet_image_urls.append(tweet_image_url)

    return tweet_texts, tweet_image_urls

async def scrape_twitter(page, username):

    await page.wait_for_selector('main', timeout=5000)

    screenshot_path = f'screenshots/{username}_twitter.png'
    await page.screenshot(path=screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")

    await asyncio.sleep(10)

    bio = await extract_bio(page)
    tweet_texts, tweet_image_urls = await extract_tweets(page)

    return bio, tweet_texts, tweet_image_urls


def scrape_twitter_sync(username):
    print(f"Starting synchronous Twitter scrape for username: {username}")
    return asyncio.run(scrape_twitter(username))


# async def extract_posts(page):

#     post_image_urls, post_captions = [], []
#     outer_selector = '._ac7v'
#     outer_elements = await page.query_selector_all(outer_selector)

#     if not outer_elements:
#         return []

#     for post_element in outer_elements:
#         post_image_url = await extract_post_cover_images(post_element)
#         post_image_urls.append(post_image_url)

#         post_caption = await extract_post_captions(post_element)
#         post_captions.append(post_caption)

#     return post_image_urls, post_captions


# async def scrape_twitter(username):
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)
#         page = await browser.new_page()
#         url = f"https://twitter.com/{username}/"

#         await page.goto(url)

#         await page.wait_for_selector('main.css-175oi2r', timeout=10000)
#         # html_content = await page.content()
#         # print(html_content)

#         await asyncio.sleep(10) 

#         screenshot_path = f'screenshots/{username}_twitter.png'
#         await page.screenshot(path=screenshot_path)
#         print(f"Screenshot saved to {screenshot_path}")

#         bio = await extract_bio(page)
#         tweets = await extract_tweets(page)


#         tweet, gender, age, nationality, ethnicity, personality = await analyze_tweets(tweets, bio)

#         if tweet:

#             image_url = await generate_image(gender, age, nationality, ethnicity, personality)

#         else:

#             image_url = None

#         await browser.close()
#     return bio, tweets, tweet, image_url