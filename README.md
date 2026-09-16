# ✨ Imdu AI

![Imdu AI](https://img.shields.io/badge/Imdu%20AI-Chatbot-purple?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_3.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)

**Imdu AI** is an advanced, multi-modal AI assistant created by **Imdaad Shajahan**. Built entirely with Python and Streamlit, it features a completely custom, fully responsive User Interface that adapts seamlessly between desktop and mobile devices.

## 🌟 Key Features

### 💬 Intelligent Chat (Gemini 3.5 Flash)
- Powered by the lightning-fast `gemini-3.5-flash` model using the newest `google-genai` SDK.
- Retains conversational memory for natural dialogue.
- **Strict Safety Guards:** Built-in SDK safety settings aggressively block sexually explicit, harassing, hate speech, and dangerous content.

### 📄 Document Analysis (PDF Q&A)
- Upload any PDF document.
- Imdu AI automatically extracts the text using `pypdf` and stores it in context.
- You can instantly ask questions, summarize, or extract specific data points from the uploaded document directly within the chat interface.

### 🎨 High-Definition Image Generation
- Instantly generate sharp, `1024x1024` resolution images using Pollinations AI.
- **Built-in Style Selector:**
  - 📸 **Realistic (High Quality):** Photorealistic, 8k resolution masterpieces.
  - ✏️ **Pencil Sketch:** Detailed graphite drawings with fine shading.
  - 🖋️ **Pen Drawing:** Crisp, crosshatched pen and ink art.
  - 🖌️ **Watercolor:** Beautiful, artistic brush strokes with vibrant colors.

## 📱 Adaptive UI Design

Imdu AI abandons standard Streamlit styling for a highly custom, CSS-driven responsive design:

*   **Mobile View (< 768px):** A premium, native-app experience featuring a pitch-black background with a neon purple radial glow. User messages are vibrant pink-to-purple diagonal gradient bubbles, while the bot uses sleek `#1C1C1E` dark grey bubbles. Includes custom avatars and a glowing pill-shaped input bar.
*   **Desktop View (>= 768px):** Automatically switches to a clean, professional workspace mimicking the official Google Gemini interface. Features a flat `#131314` dark background, subtle `#282a2c` grey user bubbles, transparent bot text, and standard alignment.

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/ShajahanImdaad53/AI-CHATBOT.git
   cd AI-CHATBOT
   ```

2. **Install dependencies**
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API Key**
   Create a `.env` file in the root directory and add your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```
   *(Alternatively, if deploying to Streamlit Cloud, add the key to your App Secrets).*

4. **Run the app**
   ```bash
   streamlit run streamlit_app.py
   ```

## 🛠️ Tech Stack
- **Frontend/Backend:** [Streamlit](https://streamlit.io/)
- **LLM Integration:** [Google GenAI SDK](https://ai.google.dev/)
- **PDF Processing:** [pypdf](https://pypi.org/project/pypdf/)
- **Image Generation:** [Pollinations AI](https://pollinations.ai/)

---
*Developed with ❤️ by Imdaad Shajahan.*