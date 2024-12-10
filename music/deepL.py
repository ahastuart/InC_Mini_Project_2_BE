from dotenv import load_dotenv
import os
import deepl

load_dotenv()

auth_key = os.getenv('DEEPL_API_KEY')

def translate(text):
    translator = deepl.Translator(auth_key)

    result = translator.translate_text(text, source_lang= "KO", target_lang="EN-US")
    print(result.text)

# if __name__ == "__main__":
#     translate("아주 행복한 꿈이었어. 친구들과 학교에서 놀았어.")
#   # 출력 : I had a very happy dream. I was playing at school with my friends.