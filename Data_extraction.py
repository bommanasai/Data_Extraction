import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import os
import glob
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

def extract_article(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1').text.strip()
        article_text = ' '.join([p.text for p in soup.select('div.td-post-content p')])
        return title, article_text
    else:
        print(f"Failed to fetch the content. Status code: {response.status_code}")
        return None, None
file_list = glob.glob(os.path.join(os.getcwd(), r"C:\Users\HP\Downloads\StopWords", "*.txt"))
stop_words = []

for file_path in file_list:
    with open(file_path, 'r') as f:
        stop_words.extend(f.read().splitlines())

def clean_text(text):
    words = word_tokenize(text)
    filtered_words = [word.lower() for word in words if word not in stop_words]
    cleaned_text = ' '.join(filtered_words)
    return cleaned_text

def calculate_positive_score(article_text):
    if article_text:
        cleaned_text = clean_text(article_text)
        positive_score = 0
        for word in cleaned_text.split():
            if word in positive_dict:
                positive_score += 1
        return positive_score
    else:
        return None
    
def calculate_negative_score(article_text):
    if article_text:
        cleaned_text = clean_text(article_text)
        negative_score = 0
        for word in cleaned_text.split():
            if word in negative_dict:
                negative_score -= 1*(-1)
        return negative_score
    else:
        return None

def count_syllables(word):
    if word.endswith("es") or word.endswith("ed"):
        return 0
    vowels = "aeiouy"
    syllable_count = 0
    prev_char = ""
    for char in word:
        if char in vowels :
            syllable_count += 1
        prev_char = char
    if word.endswith("e"):
        syllable_count -= 1
    return max(syllable_count, 1)

url_list = []
positive_score_list = []
negative_score_list = []
Polarity_score_list=[]
Subjective_score_list=[]
Avg_sentence=[]
Percent_of_complex_words=[]
Fog_Index_list=[]
Avg_number_of_words_per_sentence=[]
Complex_word_count=[]
word_count_list=[]
Syllable_per_word_list=[]
personal_prononus_list=[]
Avg_word_length=[]

positive_words= "C:\\Users\\HP\\Downloads\\positive-words.txt"
with open(positive_words, 'r') as f:
    positive_words = f.read().splitlines()
positive_dict = {word for word in positive_words if word not in stop_words}

negative_words= "C:\\Users\\HP\\Downloads\\negative-words.txt"
with open(negative_words, 'r') as f:
    negative_words = f.read().splitlines()
negative_dict = {word for word in negative_words if word not in stop_words}

excel_file_path = r"C:\Users\HP\Downloads\Input.xlsx"
df = pd.read_excel(excel_file_path)

for index, row in df.iterrows():
    url =row['URL']
    title, article_text = extract_article(url)

    if title and article_text:
        print(f"Title for URL {index + 1}: {title}")
    #         print(f"Article Text for URL {index + 1}: {article_text[:200]}...")  # Displaying only the first 200 characters
    #         print("\n" + "-"*50 + "\n")
    else:
        print(f"Extraction failed for URL {index + 1}.\n" + "-"*50 + "\n")
    if article_text==None:
        continue
    if article_text:
        cleaned_text = clean_text(article_text)
    #         print(f"Cleaned Article Text{index + 1}::", cleaned_text)
    else:
        print("Extraction failed.")

    positive_score = calculate_positive_score(article_text)
    if positive_score is not None:
        print(f"Positive Score for '{index + 1}': {positive_score}")
    else:
        print(f"Failed to calculate positive score for '{index + 1}'")

    negative_score = calculate_negative_score(article_text)
    if negative_score is not None:
        print(f"Negative Score for '{index + 1}': {negative_score}")
    else:
        print(f"Failed to calculate negative score for '{index + 1}'")

    Polarity_Score = (positive_score - negative_score)/((positive_score + negative_score) + 0.000001)
    print("Polarity Socre:",Polarity_Score)
    total_words=len(cleaned_text)
    print("total_words:",total_words)
    Subjectivity_Score = (positive_score + negative_score)/((total_words) + 0.000001)
    print("Subjectivity Score:",Subjectivity_Score)
    
    cleaned_words = word_tokenize(cleaned_text)
    syllable_counts = [count_syllables(word) for word in cleaned_words]
    for word, syllable_count in zip(cleaned_words, syllable_counts):
        print(f"Word: {word}, Syllable Count: {syllable_count}")
        
    complex_words = [word for word in cleaned_words if count_syllables(word) > 2]
    complex_word_count = len(complex_words)
    print(f"Number of complex words (more than two syllables): {complex_word_count}")
    
    number_of_words=len(cleaned_words)
    sentence = sent_tokenize(cleaned_text)
    num_sentence = len(sentence)
    Average_sentence=number_of_words/num_sentence 
    percentage_of_complex_words=complex_word_count/number_of_words
    Fog_Index = 0.4 * (Average_sentence + percentage_of_complex_words)
    print("number of sentences:",num_sentence)
    print("number of words:",number_of_words)
    print("Average_sentences:",Average_sentence)
    print("percentage:",percentage_of_complex_words)
    print("Fog Index:",Fog_Index)
    
    Average_Number_of_Words_Per_Sentence = number_of_words / num_sentence
    print("Average number of words per sentence:",Average_Number_of_Words_Per_Sentence)

    personal_pronouns_count = sum(1 for _ in re.finditer(r'\b(?:I|we|my|ours|us)\b', cleaned_text, flags=re.IGNORECASE))
    print(f"Count of personal pronouns in the cleaned text: {personal_pronouns_count}")
    
    total_characters = sum(len(word) for word in cleaned_text)
    total_words = len(cleaned_text)
    average_word_length = total_characters / total_words
    print(f"Average Word Length: {average_word_length}")

    # response = requests.get(url, timeout=10)
    url_list.append(url)
    positive_score_list.append(positive_score)
    negative_score_list.append(negative_score)
    Polarity_score_list.append(Polarity_Score)
    Subjective_score_list.append(Subjectivity_Score)
    Avg_sentence.append(Average_sentence)
    Percent_of_complex_words.append(percentage_of_complex_words)
    Fog_Index_list.append(Fog_Index)
    Avg_number_of_words_per_sentence.append(Average_Number_of_Words_Per_Sentence )
    Complex_word_count.append(complex_word_count)
    word_count_list.append(total_words)
    Syllable_per_word_list.append(syllable_count)
    personal_prononus_list.append(personal_pronouns_count)
    Avg_word_length.append(average_word_length)

result_df = pd.DataFrame({
    'URL': url_list,
    'POSITIVE SCORE': positive_score_list,
    'NEGATIVE SCORE': negative_score_list,
    'POLARITY SCORE':Polarity_score_list,
    'SUBJECTIVITY SCORE':Subjective_score_list,
    'AVG SENTENCE LENGTH':Avg_sentence,
    'PERCENTAGE OF COMPLEX WORDS':Percent_of_complex_words,
    'FOG INDEX':Fog_Index_list,
    'AVG NUMBER OF WORDS PER SENTENCE':Avg_number_of_words_per_sentence,
    'COMPLEX WORD COUNT':Complex_word_count,
    'WORD COUNT':word_count_list,
    'SYLLABLE PER WORD':Syllable_per_word_list,
    'PERSONAL PRONOUNS':personal_prononus_list,
    'AVG WORD LENGTH':Avg_word_length
})

output_csv_path = r"C:\Users\HP\Downloads\output_scores.csv"
result_df.to_csv(output_csv_path, index=False)

print(f"Results saved to: {output_csv_path}")