# Main file containing the code for the actual application's design
from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import font, filedialog, messagebox
import os
import threading

# Import functions from other Python files
from classify import classify_image
from disease_info import text_to_map, generate_sustainable_solutions

# Setup the application
app = Tk()
app.title('Crop Disease Detection')
app.geometry("1910x990")
app.resizable(False, False)

# Define variables for different colors
bg_color = '#e1ffd4'
btn1_dark_green = '#59836f'
btn1_light_green = '#739d89'
color_fg1 = 'white'
color_fg2 = 'black'
btn2_dark_green = '#578361'
btn2_light_green = '#67a374'
btn2_highlight = '#376842'
btn3_dark_green = '#4b6d53'
middle_green = '#a9c9ac'
color_bg1 = '#578361'
color_bg2 = '#67a374'

def setup_frame(frame):
    # Background image was created using Canva
    photo = Image.open("assets/Background.png")
    img = ImageTk.PhotoImage(photo)
    lbl_bk = Label(frame, image=img)
    lbl_bk.image = img
    lbl_bk.place(relx=0.5, rely = 0.5, anchor=CENTER)

    btn1 = Button(frame, text='Homepage', command=homepage_screen)
    btn1.place(x=10,y=10)
    btn2 = Button(frame, text='Detection', command=detection_screen)
    btn2.place(x=10,y=70)
    btn3 = Button(frame, text='Our Inspiration', command=inspiration_screen)
    btn3.place(x=10,y=130)
    btn4 = Button(frame, text='Sources', command=sources_screen)
    btn4.place(x=10,y=190)

    for button in [btn1, btn2, btn3, btn4]:
        button.config(
            background=btn1_dark_green,
            foreground = 'white',
            activebackground=btn1_light_green,
            activeforeground='white',
            highlightthickness=2,
            highlightbackground=btn1_dark_green,
            highlightcolor='white',
            width=16,
            height=2,
            font=('Arial', 12, 'bold')
        )

# Screen for Homepage, displaying overview of project
def homepage_screen():
    homepage_frame = Frame(app, width=1910, height=990)
    homepage_frame.place(x=0, y=0)
    setup_frame(homepage_frame)

    title = Label(
        homepage_frame,
        text="Crop Disease Detection",
        background=bg_color,
        font=("Times", 40, 'bold')
    )
    title.place(x=955, y=90, anchor=CENTER)

    # Display homepage photo (source is listed in sources tab)
    photo = Image.open("assets/Homepage_Image.jpg")
    img = ImageTk.PhotoImage(photo)
    picture = Label(homepage_frame, image=img)
    picture.image = img
    picture.place(x=955, y=345, anchor=CENTER)

    # Display paragraph of overview
    overview_text = "       Our project aims to bridge the gap between technology and agriculture by providing an innovative solution for crop disease detection and management. "
    overview_text += "We are creating an application that allows users to upload images of their crops, utilizing machine learning techniques to identify specific crop diseases. "
    overview_text += "Once a disease is identified, the application uses a prefabricated corpus and natural language processing (NLP) to extract relevant information about the symbptoms and treatment options. "
    overview_text += "This information is then curated to emphasize environmentally friendly and sustainable practices. "
    overview_text += "Overall, the project not only facilitates timely interventions for crop diseases, but also educates users about sustainable agricultural practices. "
    overview_text += "A key feature of our application is its scalability; although it currently supports a limited range of crop types and diseases, we can easily add more training datasets to expand its capabilities in the future. "
    
    overview_label = Label(homepage_frame, text=overview_text, background=bg_color, font=("Arial", 14), wraplength=1100, justify=LEFT, anchor="w")
    overview_label.place(x=955, y=675, anchor=CENTER)

    # Button to begin detection, has the same functionality as clicking the Detection tab on screen
    btn5 = Button(
        homepage_frame,
        text="Click Here to Begin Detection",
        background=btn2_dark_green,
        foreground = 'white',
        activebackground=btn2_light_green,
        activeforeground='white',
        highlightthickness=2,
        highlightbackground=btn2_highlight,
        highlightcolor='white',
        width=30,
        height=1,
        font=('Arial', 12, 'bold'),
        command=detection_screen
    )
    btn5.place(x=955, y=825, anchor=CENTER)

# Main screen(s) of functionality - prompts user for crop and image, detects disease, and displays information
def detection_screen():
    detect_frame = Frame(app, width=1910, height=990)
    detect_frame.place(x=0, y=0)
    setup_frame(detect_frame)

    title = Label(detect_frame, text="Detection", background=bg_color, font=("Times", 40, 'bold'))
    title.place(x=955, y=90, anchor=CENTER)

    # Prompts user to select a crop
    select_label = Label(
        detect_frame,
        text="Select a Crop Name: ",
        background=bg_color,
        font=("Arial", 16)
    )
    select_label.place(x=685, y=188)

    global caret_down_img_white
    caret_down_img_white = ImageTk.PhotoImage(Image.open('assets/caret-down-white-icon.png').resize((15, 15)))
    
    options = sorted(os.listdir("Image_Datasets"))
    variable = StringVar(detect_frame)
    variable.set("Choose")

    option_menu = OptionMenu(detect_frame, variable, *options)
    option_menu.place(x=935, y=175)

    menu = detect_frame.nametowidget(option_menu.menuname)
    option_menu.config(
        bg=color_bg1,
        fg=color_fg1,
        activebackground=color_bg1,
        activeforeground=color_fg1,
        font=('Arial', 20),
        border=0,
        highlightthickness=1,
        highlightbackground=color_bg2,
        pady=10,
        indicatoron=False,
        image=caret_down_img_white,
        compound=RIGHT,
        width=200
    )

    menu.config(
        bg=color_bg1,
        fg=color_fg1,
        activebackground=color_bg2,
        activeforeground=color_fg2,
        font=('Arial', 16),
        border=0,
        # Change later if wanted
        activeborder=3,
    )

    # Function to display error message if user does not do as expected
    def show_error(message):
        messagebox.showerror("Error", message)

    # If the user selects a crop and clicks the checkbox, it is no longer editable
    def disable_selects():
        global crop
        crop = variable.get()
        # If user tries to finalize selection and does not pick, display error message
        if crop == "Choose":
            show_error("A valid crop must be selected")
        else:
            option_menu.configure(state="disabled")
            unchecked_label.destroy()
            global checked_box
            checked_box = ImageTk.PhotoImage(Image.open("assets/checkbox.png").resize((30, 30)))
            global checked_label
            checked_label = Label(
                detect_frame, 
                image=checked_box,
                bg=bg_color,
            )
            checked_label.place(x=1185, y=185)
            upload_button.place(x=955, y=300, anchor=CENTER)

    global unchecked_box
    unchecked_box = ImageTk.PhotoImage(Image.open("assets/unchecked.png").resize((30, 30)))
    unchecked_label = Button(
        detect_frame, 
        image=unchecked_box,
        command=disable_selects,
        bg=bg_color,
        activebackground = bg_color
    )
    unchecked_label.place(x=1185, y=185)

    # Functionality for uploading image
    def upload_image():
        def destroy_all_and_detect():
            for item in [select_label, option_menu, checked_label, upload_button, display_image, detect_button]:
                if item == display_image:
                    item.place_forget()
                else:
                    item.destroy()
            
            global detecting_label
            detecting_label = Label(
                detect_frame,
                text="Loading... ",
                background=bg_color,
                font=("Arial", 26)
            )
            
            detecting_label.place(x=955, y=175, anchor=CENTER)

            listbox.place(x=955, y=495, width=900, height=500, anchor=CENTER)
            scrollbar.place(x=1405, y=245, height=500)
    
            start_training()

        global filepath
        filepath = filedialog.askopenfilename()
        if filepath:
            try:
                global img, display_image
                img = Image.open(filepath).resize((500, 500))
                img = ImageTk.PhotoImage(img)
                
                display_image = Label(detect_frame, image=img)
                display_image.place(x=955, y=600, anchor=CENTER)
                detect_button = Button(
                    detect_frame,
                    text="Begin Detection",
                    command=destroy_all_and_detect,
                    background=btn3_dark_green,
                    foreground = 'white',
                    activebackground=btn1_light_green,
                    activeforeground='white',
                    highlightthickness=2,
                    highlightbackground=btn3_dark_green,
                    highlightcolor='white',
                    font=('Arial', 20),
                    width=12,
                    height=1
                )
                detect_button.place(x=1400, y=600, anchor=CENTER)
            except:
                # Diplay error message if image is not uploaded
                show_error("You must select a file that is an image (common file extensions are .png and .jpg).")
        else:
            # If nothing is selected, display error message
            show_error("A file must be selected.")


    upload_button = Button(
        detect_frame,
        text="Upload Image",
        command=upload_image,
        background=btn3_dark_green,
        foreground = 'white',
        activebackground=btn1_light_green,
        activeforeground='white',
        highlightthickness=2,
        highlightbackground=btn3_dark_green,
        highlightcolor='white',
        font=('Arial', 20),
        width=12,
        height=1
    )

    # Create a listbox to display the process of detection
    # This includes training the model, predicting the disease, and loading results/information
    scrollbar = Scrollbar(detect_frame, orient="vertical")
    listbox = Listbox(
        detect_frame, 
        yscrollcommand = scrollbar.set,
    )
    listbox.insert(END, "   Training Model...")
    scrollbar.config(command = listbox.yview)

    # Create a thread so that the program will both run classify image AND update the listbox
    def start_training():
        threading.Thread(target=run_training, daemon=True).start()

    def run_training():
        def update_scrollbar(text):
            listbox.insert(END, "   " + text)
        
        # Predict the disease using the classify_image function
        global predicted_disease, percent_conf
        predicted_disease, percent_conf = classify_image(crop, filepath, update_scrollbar)
        update_scrollbar("Loading Results...")
        if predicted_disease != "Healthy":
            global map, sustainable
            map = text_to_map(crop, predicted_disease)
            sustainable = generate_sustainable_solutions(map)
        update_scrollbar("Results are Ready!")

        detecting_label.config(text="Detection Complete!")
        results_button.place(x=955, y=800, anchor=CENTER)

    # Changes the screen to display all information on the disease
    def view_results():
        results_button.destroy()
        listbox.destroy()
        scrollbar.destroy()
        detecting_label.destroy()
        title.config(text="Results")

        rectangle = Label(detect_frame, text="", background=middle_green, borderwidth=2, relief="solid", width=72, height=6)
        disease_label = Label(detect_frame, text=f"Predicted Disease: {predicted_disease}", background=middle_green, font=("Times", 22, 'bold'))
        percent_label = Label(detect_frame, text=f"Percent Confidence: {percent_conf}", background=middle_green, font=("Arial", 15))
        
        # If some disease was detected
        if predicted_disease != "Healthy":
            rectangle.place(x=275, y=160, anchor='nw')
            disease_label.place(x=595, y=195, anchor=CENTER)  
            percent_label.place(x=595, y=230, anchor=CENTER)

            overview_title = Label(detect_frame, text="Overview", background=bg_color, font=("Times", 23, 'bold'))
            overview_text = Label(detect_frame, text=map["Overview"], background= bg_color, font=("Arial", 13), wraplength=900, justify=LEFT)
            overview_title.place(x=1400, y=170, anchor=CENTER)
            overview_text.place(x=1400, y=200, anchor='n')

            # Coordinates list for placement of labels & headings
            coords = [[475, 350], [1400, 350], [475, 550], [1400, 550]]
            i = 0
            for heading in map:
                if heading == "Overview" or heading == "Source":
                    continue
                if map[heading] != "":
                    title_label = Label(detect_frame, text=heading, background=bg_color, font=("Times", 23, 'bold'))
                    text_label = Label(detect_frame, text=map[heading], background=bg_color, font=("Arial", 13), wraplength=850, justify=LEFT)
                    title_label.place(x=coords[i][0], y=coords[i][1], anchor=CENTER)
                    text_label.place(x=coords[i][0], y=coords[i][1] + 30, anchor='n')
                    if heading == "Treatments/Solutions":
                        bottom_y_treat = 580 + text_label.winfo_reqheight()
                    elif heading == "Prevention":
                        bottom_y_prevent = 580 + text_label.winfo_reqheight()                
                    i += 1
            
            source_label = Label(detect_frame, text=f"Website Source:\n{map['Source']}", background=bg_color, font=("Arial", 13))
            source_label.place(x=475, y=(990 - bottom_y_treat) // 2 + bottom_y_treat, anchor=CENTER)

            # Displays sustainable suggestions, having a button to toggle visibility
            solution_text = ""
            for solution in sustainable:
                if solution_text == "":
                    solution_text += " - " + solution + "\n"
                else:
                    solution_text += " - " + solution + "\n"
            sustainable_label = Label(
                detect_frame, text=" " + solution_text.strip(), 
                background=middle_green, font=("Arial", 13), borderwidth=2, relief="solid", 
                wraplength=850, justify=LEFT
            )

            def toggle_label():
                if sustainable_label.winfo_ismapped():
                    sustainable_label.place_forget()
                else:
                    sustainable_label.place(x=1400, y=bottom_y_prevent + 80, anchor='n')
                
            sustainable_button = Button(
                detect_frame,
                text="See Sustainable Suggestions",
                command=toggle_label,
                background=btn3_dark_green,
                foreground = 'white',
                activebackground=btn1_light_green,
                activeforeground='white',
                highlightthickness=2,
                highlightbackground=btn3_dark_green,
                highlightcolor='white',
                font=('Arial', 18),
                width=30,
                height=1
            )
            sustainable_button.place(x=1400, y=bottom_y_prevent + 20, anchor='n')
        
        # If the crop is healthy, prompt user to either go to homepage or detect another crop
        else:
            rectangle.place(x=645, y=160, anchor='nw')
            disease_label.config(text= "Your crop seems to be healthy!")
            percent_label = Label(detect_frame, text=f"Percent Confidence: {percent_conf}", background=middle_green, font=("Arial", 15))
            disease_label.place(x=955, y=195, anchor=CENTER)
            percent_label.place(x=955, y=230, anchor=CENTER)
            display_image.place(x=955, y=600, anchor=CENTER)

            new_detection_btn = Button(
                detect_frame,
                text="Detect Another Crop",
                background=btn2_dark_green,
                foreground = 'white',
                activebackground=btn2_light_green,
                activeforeground='white',
                highlightthickness=2,
                highlightbackground=btn2_highlight,
                highlightcolor='white',
                width=25,
                height=2,
                font=('Arial', 15, 'bold'),
                command=detection_screen
            )
            new_detection_btn.place(x=1500, y=600, anchor=CENTER)

            homepage_btn = Button(
                detect_frame,
                text="Return to Homepage",
                background=btn2_dark_green,
                foreground = 'white',
                activebackground=btn2_light_green,
                activeforeground='white',
                highlightthickness=2,
                highlightbackground=btn2_highlight,
                highlightcolor='white',
                width=25,
                height=2,
                font=('Arial', 15, 'bold'),
                command=homepage_screen
            )
            homepage_btn.place(x=410, y=600, anchor=CENTER)

    # Button to click after prediction stage
    results_button = Button(
        detect_frame, 
        text="View Results",
        command=view_results,
        background=btn3_dark_green,
        foreground = 'white',
        activebackground=btn1_light_green,
        activeforeground='white',
        highlightthickness=2,
        highlightbackground=btn3_dark_green,
        highlightcolor='white',
        font=('Arial', 20),
        width=12,
        height=1
    )

# Screen that talks about our inspiration for this project
def inspiration_screen():
    inspire_frame = Frame(app, width=1910, height=990, bg=bg_color)
    inspire_frame.place(x=0,y=0)
    setup_frame(inspire_frame)

    title = Label(
        inspire_frame,
        text="Our Inspiration",
        background=bg_color,
        font=("Times", 40, 'bold')
    )
    title.place(x=955, y=90, anchor=CENTER)

    photo = Image.open("assets/Inspiration_Image.png")
    img = ImageTk.PhotoImage(photo.resize((720, 405)))
    picture = Label(inspire_frame, image=img)
    picture.image = img
    picture.place(x=955, y=345, anchor=CENTER)

    # Take paragraph from pre-written text file
    file = open("inspiration.txt", "r")
    inspiration_text = "       " + file.read().strip()
    file.close()

    overview_label = Label(
        inspire_frame, text=inspiration_text, background=bg_color, 
        font=("Arial", 14), wraplength=1100, justify=LEFT, anchor="w"
    )
    overview_label.place(x=955, y=725, anchor=CENTER)

# Screen to display sources
def sources_screen():
    sources_frame = Frame(app, width=1910, height=990, bg=bg_color)
    sources_frame.place(x=0,y=0)
    setup_frame(sources_frame)

    title = Label(
        sources_frame,
        text="Sources",
        background=bg_color,
        font=("Times", 40, 'bold')
    )
    title.place(x=955, y=90, anchor=CENTER)
    
    label = Label(
        sources_frame,
        text="We utilized multiple outside resources in the creation of this project.",
        background=bg_color,
        font=("Arial", 20)
    )
    
    label.place(x=955, y=175, anchor=CENTER)

    # Using a scrollable listbox to display all sources
    scrollbar = Scrollbar(sources_frame, orient="vertical")
    listbox = Listbox(
        sources_frame,
        font=("Arial", 12),
        yscrollcommand = scrollbar.set
    )    
    scrollbar.config(command = listbox.yview)

    # Take sources from pre-written file
    sources_file = open("sources.txt", "r", errors="ignore")
    lines = sources_file.readlines()
    sources_file.close()

    listbox.insert(END, "")
    for line in lines:
        listbox.insert(END, "   " + line.rstrip())
    
    listbox.place(x=955, y=575, width=1400, height=700, anchor=CENTER)
    scrollbar.place(x=1655, y=225, height=700)

# Open the application, starting with the homepage screen
homepage_screen()
app.mainloop()