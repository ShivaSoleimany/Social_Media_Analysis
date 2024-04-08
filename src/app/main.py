import streamlit as st
from pathlib import Path
import sys
import asyncio
from playwright.async_api import async_playwright

sys.path.append(str(Path(__file__).resolve().parent.parent))

from scrape.scrape_twitter import scrape_twitter
from scrape.scrape_instagram import scrape_instagram
from GAN.analyze_posts import analyze_post_texts, analyze_post_images, analyze_all_information
from GAN.generate_posts import generate_avatar, generate_post

async def analyze_social_media(twitter_username, instagram_username):
    posts, image_urls = [], []
    bio = ""

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            try:
                if twitter_username:
                    twitter_page = await browser.new_page()
                    await twitter_page.goto(f"https://twitter.com/{twitter_username}")
                    twitter_bio, tweet_texts, tweet_image_urls = await scrape_twitter(twitter_page, twitter_username)
                    posts.extend(tweet_texts)
                    image_urls.extend(tweet_image_urls)
                    bio += twitter_bio + " "

                if instagram_username:
                    instagram_page = await browser.new_page()
                    await instagram_page.goto(f"https://www.instagram.com/{instagram_username}/")
                    instagram_bio, post_captions, post_image_urls = await scrape_instagram(instagram_page, instagram_username)
                    posts.extend(post_captions)
                    image_urls.extend(post_image_urls)
                    bio += instagram_bio
            finally:
                await browser.close()

        text_results = await analyze_post_texts(bio, posts)
        image_results = await analyze_post_images(image_urls)
        final_results = await analyze_all_information(text_results, image_results)
        avatar = await generate_avatar(final_results)
        post = await generate_post(final_results, text_results)

        return final_results, avatar, post

    except Exception as e:
        st.error(f"Failed to analyze profiles: {e}")
        return None, None, None
        
def main():
    st.title('Social Media Analysis App')
    st.write("""
    This app allows you to analyze Twitter and Instagram profiles to predict characteristics such as gender, age, and personality traits of the users. 
    Enter a Twitter or Instagram username, and the app will scrape their webpage to gather this information. 
    Additionally, the app will generate a tweet or caption that the user is likely to post and create an image representing what the user might look like.
    """)

    if 'twitter_results' not in st.session_state:
        st.session_state.twitter_results = None, None, None

    if 'instagram_results' not in st.session_state:
        st.session_state.instagram_results = None, None, None

    col1, col2 = st.columns(2)

    with col1:
        twitter_username = st.text_input("Enter a Twitter Username", key="twitter_user", value="ylecun")
        button_col1, button_col2, button_col3 = st.columns([1, 2, 1])
        with button_col2:
            if st.button('Analyze Twitter', key="analyze_twitter"):
                if twitter_username:
                    final_results, avatar, post = asyncio.run(analyze_social_media(twitter_username, None))
                    st.session_state.twitter_results = final_results, avatar, post
                else:
                    st.error("Please enter a Twitter username.")

    with col2:
        instagram_username = st.text_input("Enter an Instagram Username", key="instagram_user", value="yannlecun")
        button_col4, button_col5, button_col6 = st.columns([1, 2, 1])
        with button_col5:
            if st.button('Analyze Instagram', key="analyze_instagram"):
                if instagram_username:
                    final_results, avatar, post = asyncio.run(analyze_social_media(None, instagram_username))
                    st.session_state.instagram_results = final_results, avatar, post
                else:
                    st.error("Please enter an Instagram username.")

    # Middle button across the border of two main columns
    if button_col3 and button_col4:
        middle_col1, middle_col2, middle_col3 = st.columns([1.5, 1, 1.5])
        with middle_col2:
            if st.button('Analyze Both', key="analyze_both"):
                if twitter_username and instagram_username:
                    final_results, avatar, post = asyncio.run(analyze_social_media(twitter_username, instagram_username))
                    if final_results:
                        st.image(avatar)
                        st.write(post)
                        st.write(final_results)
                else:
                    st.error("Please enter both usernames.")

    twitter_results, twitter_avatar, twitter_post = st.session_state.twitter_results
    instagram_results, instagram_avatar, instagram_post = st.session_state.instagram_results

    if twitter_results:
        with col1:
            st.image(twitter_avatar)
            st.write(twitter_post)
            st.write(twitter_results)

    if instagram_results:
        with col2:
            st.image(instagram_avatar)
            st.write(instagram_post)
            st.write(instagram_results)

if __name__ == "__main__":
    main()
