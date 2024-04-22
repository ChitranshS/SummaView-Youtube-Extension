from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
import together
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
from config import together_api_key
def luhn_method(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer_luhn = LuhnSummarizer()
    summary_1 = summarizer_luhn(parser.document, 70)  # Change the number of sentences you want in the summary
    dp = []
    for sentence in summary_1:
        dp.append(str(sentence))

    final_sentence = ' '.join(dp)
    return final_sentence

def count_words(text):
    # Split the text into words using whitespace as a delimiter
    words = text.split()
    # Return the count of words
    return len(words)

# Main function
def main_2(data):
    number_of_words = count_words(data)
    if number_of_words>2600:
        result_summary = luhn_method(data)
    else:
        result_summary = data

    together.api_key = together_api_key
    output = together.Complete.create(
    prompt = f"""
    Input Text:{result_summary}

    Summary Output:
    Generate a concise summary of the provided text, highlighting the main points and key details. The summary should contain enough information to convey the essence of the text and maintain the word count between 300 to 500 for maintaining brevity and clarity. Please focus on capturing the essential ideas, omitting redundant or extraneous information but include jargon and technical terms and number in it.
    """, 
    model = "togethercomputer/llama-2-70b-chat", 
    max_tokens = 512,
    temperature = 0.7,
    top_k = 50,
    top_p = 0.7,
    repetition_penalty = 1
    )

# print generated text
    text = output['output']['choices'][0]['text']
    sending_result = {"text":text}

    return sending_result
    
