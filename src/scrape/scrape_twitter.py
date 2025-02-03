import asyncio
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