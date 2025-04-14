# Encode AI Hack 2025: Personal Finance Assistant 💸

Ever wondered if you've been making the most of your savings 💰? Found yourself grappling with the cumbersome calculations required to find the best investment strategy 📉📈? 
Been struggling to pay off your seemingly endless pile of debts? 😩

Look no further! With the help of our snazzy, AI-powered personal financial assistant 🤖, you'll be stress-free in no time! ✨

## ⚙️ How Does It Work?

Simply enter some basic details like your current income and savings, sit back, and let the AI do the work! Through the use of cutting-edge AI, you'll receive
the most intelligent yet concise financial advice, including:

* ⚠️ Immediate actions to take in order to tackle urgent issues like high debt-to-income ratios.
* 📊 Tailored long-term plans to help progressively increase income and maintain a healthy savings rate.
* 📉 Series of calculated metrics to give further insights into the user's spending habits.
* 💡 Alternative investment strategies and other options worth exploring based on the user's metrics.

By utilising Portia AI's open source SDK, we’ve tapped into the brainpower of pioneering models like Google’s Gemini and OpenAI’s ChatGPT 🧠. 
That means our trusty finance assistant doesn’t just give advice — it can even estimate how your choices might boost your credit score 📈, so you can make smarter moves with confidence.

## 🚀 Getting Started

Want to try it out for yourself? Follow these quick steps to get up and running:

### 1️⃣ Clone the repo

```bash
git clone https://github.com/ikemal12/encode-ai-hack-2025.git
cd encode-ai-hack-2025
```

### 2️⃣ Set Up a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```
Or if you don't have a `requirements.txt`, generate one by running `pip freeze > requirements.txt` in your virtual environment.

### 4️⃣ Run the app

```bash
python main.py
```

This should get the Flask server up and running but you won't be able to get any help from your AI-powered assistant 🤝 without access to the models, 
which is what the next section will help you do.

## 🔐 Configure Access to LLMs

To use the AI-powered features in this project, you’ll need to sign up and grab API keys from both OpenAI and Google Gemini. Don’t worry — it only takes a minute!

### 1️⃣ 🔑 OpenAI (for ChatGPT/GPT-4)
* Sign up or log in here: https://platform.openai.com/signup 
* Get your API key here: https://platform.openai.com/account/api-keys

Once you have your key, store it somewhere safe. You can add it to your environment variables like so (or create a .env file in your project directory):

```bash
export OPENAI_API_KEY=put_your_openai_api_key_here
```

### 2️⃣ 🧠 Google Gemini (via Google AI Studio)
* Sign up or log in here: https://aistudio.google.com/app/signup
* Get your API key here: https://aistudio.google.com/app/apikey

Add it to your environment:

```bash
export GEMINI_API_KEY=put_your_gemini_api_key_here
```

Start exploring!
Input your info and let the AI financial assistant do the heavy lifting.

