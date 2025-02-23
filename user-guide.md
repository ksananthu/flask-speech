# 📖 **User Guide: Real-Time Speech Translator App**  

## 📌 **Overview**  
This application facilitates communication between **patients** and **health workers** by providing real-time **speech-to-text, translation, and text-to-speech** features. Users can record speech, translate it into another language, and listen to the translated speech.  

---

## 🔧 **System Requirements**  
### ✅ **Hardware & Software Requirements**  
- A **computer or mobile device** with a microphone and speakers.  
- A modern **web browser** (Chrome, Firefox, Edge).  
- **Internet access** for using Google APIs.  

### ✅ **API Setup (For Developers Only)**  
- Ensure your **Google Cloud Speech-to-Text API** is configured.  
- Set up a **.env file** with your API key.  

---

# 🏗 **How to Use the App**  

## **1️⃣ Open the App**  
- Open a web browser and go to `http://0.0.0.0:9045`.  
- The **homepage** will display two sections:  
  - **Patient's Panel**  
  - **Health Worker's Panel**  

## **2️⃣ Select Your Language**  
- Click on the **dropdown menu** under each section.  
- Choose the language for **both the patient and the health worker**.  

## **3️⃣ Record Your Speech**  
- Click the **🎤 Microphone Button** under your section.  
- Speak clearly into the microphone.  
- The app will transcribe your speech in real time.  

## **4️⃣ View the Transcription**  
- The transcribed text will appear in the **text area** below the language selection.  
- If the speech is unclear, an error message will be displayed.  

## **5️⃣ Translate the Speech**  
- Once transcription is complete, the app will **automatically translate** the text into the other language.  

## **6️⃣ Listen to the Translated Speech**  
- Click the **📢 Speaker Button** to hear the translated speech.  
- The system will generate an **audio file** and play it back.  

## **7️⃣ Replay or Record Again**  
- You can click **Record Again** to repeat the process.  
- The app automatically deletes old audio files before creating new ones.  

---

# 🎯 **Advanced Features**  

### ✅ **Real-Time Processing**  
- The app uses **Google Cloud Speech-to-Text** for **high-accuracy transcription**.  
- **Multilingual Support**: Translate between multiple languages.  

### ✅ **Secure API Handling**  
- API keys are stored securely in a `.env` file.  
- Communication is **encrypted** using SSL.  

### ✅ **Logging & Error Handling**  
- **Real-time logging** for tracking user interactions.  
- **Error messages** appear if speech is unclear or API errors occur.  

---

# 🚀 **Troubleshooting & FAQs**  

### ❓ **Why is my speech not being recognized?**  
✅ Ensure your **microphone is enabled** and the **volume is high enough**.  
✅ Speak clearly and in the selected **language**.  

### ❓ **Why is the translation incorrect?**  
✅ Some languages may have **accuracy limitations** in Google Translate.  
✅ Ensure you have selected the correct **source and target language**.  

### ❓ **How do I improve speech recognition?**  
✅ Reduce **background noise** when speaking.  
✅ Use a **good quality microphone**.  

---

# 🎉 **Conclusion**  
This app **bridges the language gap** between patients and health workers, making communication easier through **speech-to-text, translation, and text-to-speech**. Enjoy using it and let us know if you have any feedback!  

