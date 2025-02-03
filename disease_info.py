# This file takes care of taking the information from the disease corpus and making it "usable"
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Get the solutions dictionary
from Disease_Corpus.sustainable_solutions import solutions_dict

# Function to turn the information from the .txt file into a dictionary
def text_to_map(crop, disease):
    disease = disease.lower().replace(" ", "_")
    file_path = f"Disease_Corpus/{crop.title()}/{disease}.txt"

    file = open(file_path, 'r')
    lines = file.readlines()
    file.close()

    map = {}
    for i in range(len(lines)):
        line = lines[i].strip().replace(":", "")
        if line.find("Source") == 0:
            map["Source"] = line[7:]
        elif line in ["Overview", "Symptoms", "Causes", "Treatments/Solutions", "Prevention"]:
            map[line] = lines[i + 1].strip()
    return map

# Given the dictionary (map), find sustainable solutions
def generate_sustainable_solutions(map):
    paragraphs = [map["Treatments/Solutions"], map["Prevention"]]
    
    keywords = []

    # Utilizing NLP to tokenize and lemmatize words from these paragraphs
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    for paragraph in paragraphs:
        words = word_tokenize(paragraph)
        filtered_words = [lemmatizer.lemmatize(word.lower()) for word in words if word.isalpha() and word.lower() not in stop_words]
        keywords.extend(filtered_words)

    tokens = set(keywords)
    solutions = []
    for keyword in solutions_dict.keys():
        keyword_tokens = set(keyword.lower().split(" "))
        if keyword_tokens.issubset(tokens):
            solutions.append(solutions_dict[keyword])

    return solutions