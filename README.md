# Social Media Analysis App 🚀
![OpenAI](https://img.shields.io/badge/LLM-GPT-orange)  
![](https://img.shields.io/badge/Powered%20by-Streamlit-ff4b4b)  
![Playwright](https://img.shields.io/badge/Web%20Scraping-Playwright-blue)  
![AsyncIO](https://img.shields.io/badge/Asynchronous-AsyncIO-brightgreen)


This application tries to predict characteristics of user such as gender, age, and personality traits, using data gathered from their Twitter and Instagram accounts. It scrapes user profiles **asynchronously**, analyzes text and images, and uses this data to generate insights and visual representations of the users using **OpenAI API**.

## **🌟 Features**
- 🔍 **Profile Analysis**: Analyzes Twitter and Instagram profiles.
- 📊 **Data Extraction**: Gathers data through web scraping.
- 🖼️ **Image Generation**: Creates avatars based on user data.
- 📝 **Content Generation**: Generates possible tweets or Instagram captions.

---

## **🛠️ Installation**

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/ShivaSoleimany/Social_Media_Analysis.git
cd Social_Media_Analysis
```


## 2️⃣ Install Dependencies
Make sure Python 3.8+ is installed and then run:

```bash
pip install -r requirements.txt
```

## 3️⃣ Set Environment Variables
set your openAI key in .env file

```bash
OPENAI_API_KEY='your_openai_key'
```

## **🖥️ How to Use**
Run the application using Streamlit:

```bash
streamlit run src/app/main.py
```
Navigate to the local web URL provided by Streamlit to interact with the app.

## **🛠️ Technologies Used**

🤖 AI Analysis: Text and image processing to infer user traits.

🌐 Web Scraping: Playwright for data extraction.

🖥️ Frontend: Streamlit for interactive web UI.

## **📩 Contact & Contribution**
🚀 Want to contribute? Open a PR!

💡 Found an issue? Report it under GitHub Issues.

📧 Contact: shiva.soleimany.dzch@gmail.com





