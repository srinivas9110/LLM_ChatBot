# LLM_ChatBot

🚀 A conversational AI web app built with **Streamlit** and **Hugging Face Inference API**.  
This app lets you chat with multiple LLMs, switch between models, and view your chat history in a clean UI.  

---

## ✨ Features  
- 🧠 Chat with **Hugging Face hosted LLMs** (like Mistral, LLaMA, etc.)  
- 🔄 Switch between multiple models  
- 💬 Persistent chat history during a session  
- 🌓 Light/Dark theme toggle  
- 📄 Export chat history  

---

## 📦 Installation  

Clone the repository:  

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

Create a virtual environment:  

```bash
python -m venv venv
```

Activate it:  

- **Windows**  
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux**  
  ```bash
  source venv/bin/activate
  ```

Install dependencies:  

```bash
pip install -r requirements.txt
```

---

## 🔑 Hugging Face Token Setup  

This app requires a Hugging Face API token.  

1. Get your token from [Hugging Face Settings → Access Tokens](https://huggingface.co/settings/tokens)  
2. Create a **`.streamlit`** folder in your project root (if it doesn’t exist):  

   ```bash
   mkdir .streamlit
   ```

3. Inside it, create a file called **`secrets.toml`** and add:  

   ```toml
   HF_TOKEN = "your_huggingface_token_here"
   ```

⚠️ **Note:** The `.streamlit/secrets.toml` file is ignored in `.gitignore` to keep your token safe.  

---

## ▶️ Running the App  

Start the app with:  

```bash
streamlit run app.py
```

Then open the link shown in the terminal (usually `http://localhost:8501`).  

---

## 📂 Project Structure  

```
├── app.py                # Main Streamlit app
├── test_inference.py     # Testing Hugging Face models
├── requirements.txt      # Dependencies
├── .gitignore            # Ignore venv & secrets
└── README.md             # Project documentation
```

---

## 🌍 Deployment (Optional)  

You can deploy this app on:  
- [Streamlit Cloud](https://share.streamlit.io/)  
- [Render](https://render.com/)  
- [Hugging Face Spaces](https://huggingface.co/spaces)  

---

## 🤝 Contributing  

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to improve.  

---

## 📜 License  

This project is licensed under the MIT License.  
