import asyncio
import os
import json
from openai import AsyncOpenAI, OpenAIError
from playwright.async_api import async_playwright

async def extract_bio(page):

    selector = '.x7a106z'
    element = await page.query_selector(selector)

    if element:
        bio_text = await element.inner_text()
    else:
        bio_text = "Bio not found"

    return bio_text

async def extract_post_captions(post_element):

    caption = ""
    inner_selector = '.x1lliihq img[alt]'  # Assuming x1lliihq is a class
    inner_elements = await post_element.query_selector_all(inner_selector)

    for inner_element in inner_elements:
        caption = await inner_element.get_attribute('alt')

    return caption

async def extract_post_cover_images(post_element):
    image_url = ""
    inner_selector = 'img[alt]'  # Selecting img tags with an alt attribute, assuming these are the post images
    inner_elements = await post_element.query_selector_all(inner_selector)

    for inner_element in inner_elements:
        image_url = await inner_element.get_attribute('src')
    return image_url

async def extract_posts(page):

    post_image_urls, post_captions = [], []
    outer_selector = '._ac7v'
    outer_elements = await page.query_selector_all(outer_selector)

    if not outer_elements:
        return []

    for post_element in outer_elements:
        post_image_url = await extract_post_cover_images(post_element)
        post_image_urls.append(post_image_url)

        post_caption = await extract_post_captions(post_element)
        post_captions.append(post_caption)

    return post_image_urls, post_captions


async def scrape_instagram(page, username):


    await page.wait_for_selector('main', timeout=5000)
    # html_content = await page.content()

    screenshot_path = f'screenshots/{username}_instagram.png'
    await page.screenshot(path=screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")


    bio = await extract_bio(page)
    post_image_urls, post_captions = await extract_posts(page)

    return bio, post_captions, post_image_urls