# TSA Software Development - Crop Disease Detection
Team ID: 2003-1

Our project aims to bridge the gap between technology and agriculture by providing an innovative solution for crop disease detection and management. We are creating an application that allows users to upload images of their crops, utilizing machine learning techniques to identify specific crop diseases. Once a disease is identified, the application uses a prefabricated corpus and natural language processing (NLP) to extract relevant information about the symbptoms and treatment options. This information is then curated to emphasize environmentally friendly and sustainable practices. "Overall, the project not only facilitates timely interventions for crop diseases, but also educates users about sustainable agricultural practices. "A key feature of our application is its scalability; although it currently supports a limited range of crop types and diseases, we can easily add more training datasets to expand its capabilities in the future.

## Installation
Install all necessary libraries stated in the "requirements.txt" file. During the creation of this application, we used a computer that is equipped with a built-in dedicated graphics card (NVIDIA GeForce RTX 4060 Laptop GPU), which allows certain parts of the program to run faster. In order to use this as well, additional libraries related to the specific graphics card must be installed to your device.

Lastly, execute the line below in your terminal to download certain nltk corpora used in our program.

```bash
python -m nltk.downloader stopwords punkt_tab wordnet
```
## Usage
Here are brief explanations of the important sections:

assets: contains images/graphics displayed in the application

Disease_Corpus: holds .txt files with information about each disease

Image_Dataset: consists of images for each crop disease
** Note: Due to file size limitations on GitHub, we compressed the image datasets for each crop into .zip files.

Test_Images: not used by the program itself, but this holds images that can be user input in the app itself

classify.py: takes care of the TensorFlow model functionality

disease_info.py: utilizes information from the disease corpus and incorporates NLP techniques

main.py: holds the code for the app's design

## Sources

All sources used in the creation of our application are included in the "sources.txt" file.
