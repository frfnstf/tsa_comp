# TSA Software Development - Crop Disease Detection

Our project aims to bridge the gap between technology and agriculture by providing an innovative solution for crop disease detection and management. We created an application that allows users to upload images of their crops, utilizing machine learning techniques to identify specific crop diseases. Once a disease is identified, the application uses a prefabricated corpus and natural language processing (NLP) to extract relevant information about the symptoms and treatment options. This information is then curated to emphasize environment-friendly and sustainable practices. Overall, the project not only facilitates timely interventions for crop diseases, but also educates users about sustainable agricultural practices. The app also contains personalized data charts and other features based on their detected diseases. A key feature of our application is its scalability; although it currently supports a limited range of crop types and diseases, we can easily add more training datasets to expand its capabilities in the future. Lastly, our app includes a graphical user interface (GUI) for both a mobile and a desktop screen.

## Installation
Install all necessary libraries stated in the "requirements.txt" file. 

```bash
pip install -r requirements.txt
```

During the creation of this application, we used a computer that is equipped with a built-in dedicated graphics card (NVIDIA GeForce RTX 4060 Laptop GPU), which allows certain parts of the program to run faster. However, our app will work just as well on a normal computer as well. In order to use this as well, additional libraries related to the specific graphics card must be installed to your device.

Lastly, execute the line below in your terminal to download certain nltk corpora used in our program.

```bash
python -m nltk.downloader stopwords punkt_tab wordnet
```

## Running the Code
To run this code, first make sure you have all necessary libraries/packages installed, along with all of the files in this GitHub repository. This includes opening up the saved_models folder and downloading all of the .keras files in the Google Drive Folder linked in the .txt file. Make sure to download all of these .keras files into the saved_models folder so they can be accessed by the program as intended. Then, execute one of the lines below, based on which version you would like to see.
```bash
python main.py mobile
```
```bash
python main.py desktop
```

If you would like to view the account of a premade user (who already has an account and detection data), login with the username "farmer1" and the password "111".

## Usage
Here are brief explanations of the files/folders:

Folders:

assets: contains images/graphics displayed in the application

Disease_Corpus: holds .txt files with information about each disease along with sustainable_solutions.py, which has a Python dictionary used to generate sustainable suggestions for the user

Image_Datasets: consists of images for each crop disease (due to f)

    ** Note: Due to file size limitations on GitHub, we decreased the size of our image datasets for each disease to be only 100 images. This folder is not used directly when our program is run; instead, it was used to create the saved models in the saved_models folder. So, our saved models were trained with the full datasets.

saved_models: holds the pre-trained machine learning models that are loaded and used in our application to make disease predictions

    ** Note: Again, due to file size limitations, the saved_models folder has a .txt file containing a link to a Google Drive folder with the model files.


Test_Images: not used by the program itself, but this holds images that can be user input in the app itself

Text_Files: holds .txt files of text that is displayed in the application.

user_data: contains 3 files - detection_data.csv (datasheet for all detections run, organized by username); sustainability_checklist (used to keep track of the sustainability checklist feature in our app); and user_datasheet.txt (maps usernames to encrypted passwords)

Files:
classify.py: takes care of the TensorFlow model functionality and crop disease detection

disease_info.py: utilizes information from the disease corpus and incorporates NLP techniques

desktop_gui.py / mobile_gui.py: holds code for the GUI of the desktop/mobile version of our app

desktop_login.py / mobile_login.py: allow users to have their own account and encrypts/decrypts their details (the respective file is called)

encryption_key.key: holds the encryption key used to encrypt/decrypt the users' passwords

main.py: maps the user to either display mobile or desktop version of app

requirements.txt: houses the libraries/packages and their respective versions that are required for this app (including dependencies)

## Sources

All sources used in the creation of our application are included in the "sources.txt" file.
