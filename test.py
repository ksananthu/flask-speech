from googletrans import Translator
import asyncio  # Import the asyncio library

translator = Translator()

async def translate_text(text, target_language):  # Define an async function
    translation = await translator.translate(text, dest=target_language)  # Await the result
    return translation.text  # Now you can access the .text attribute

async def main():  # Another async function to run the translation
    text = "Hello, world!"
    target_lang = "ml"
    translated_text = await translate_text(text, target_lang)  # Await the translation
    print(translated_text)

if __name__ == "__main__":
    asyncio.run(main())  # Run the main async function