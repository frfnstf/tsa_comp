# Main file containing the code for the actual application's design
from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import font, filedialog, messagebox
import os
import threading
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

# Import functions from other Python files
from classify import classify_image
from disease_info import text_to_map, generate_sustainable_solutions
from desktop_login import show_login_window



def logout():
    global is_logged_in, done_with_program
    is_logged_in = False
    done_with_program = True
    app.withdraw()
    setup_desktop_app(False)

def on_closing():
    if messagebox.askokcancel("Warning", "You will be automatically logged out. Click \"OK\" to accept."):
        logout()

# Setup the application
def setup_desktop_app(first_time):
    if first_time:
        global username, is_logged_in, done_with_program
        username, is_logged_in = show_login_window()
        done_with_program = False

    global app
    if is_logged_in:
        app = Tk()
        app.title('Crop Disease Detection')
        app.geometry("1910x990")
        app.resizable(False, False)
        app.protocol("WM_DELETE_WINDOW", on_closing)
        homepage_screen()
    elif done_with_program:
        sys.exit()
    else:
        username, is_logged_in = show_login_window()
        if is_logged_in:
            setup_desktop_app(False)

    app.mainloop()

# Define variables for frequently used colors
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

    # Creating the toggle menu at the top left of screen
    def toggle_menu():
        def collapse_toggle_menu():
            toggle_menu_frame.destroy()
            toggle_btn.config(text='☰', command=toggle_menu)


        toggle_menu_frame = Frame(app, bg=btn3_dark_green)

        btn1 = Button(toggle_menu_frame, text='My Dashboard', command=dashboard_screen)
        btn1.place(x=20, y=20)

        btn2 = Button(toggle_menu_frame, text='Detect Disease', command=detection_screen)
        btn2.place(x=20, y=80)

        btn3 = Button(toggle_menu_frame, text='About the App', command=homepage_screen)
        btn3.place(x=20, y=140)

        btn4 = Button(toggle_menu_frame, text='App Inspiration', command=inspiration_screen)
        btn4.place(x=20, y=200)

        btn5 = Button(toggle_menu_frame, text='Sources', command=sources_screen)
        btn5.place(x=20, y=260)

        for btn in [btn1, btn2, btn3, btn4, btn5]:
            btn.config(
                font=('Bold', 20),
                bd=0,
                bg=btn3_dark_green,
                fg='white',
                activebackground=btn3_dark_green,
                activeforeground='white',
                highlightthickness=0
            )

        toggle_menu_frame.place(x=0, y=50, height=app.winfo_height(), width=300)

        toggle_btn.config(text='✕', command=collapse_toggle_menu, highlightthickness=0)

    head_frame = Frame(
        app,
        bg=btn3_dark_green,
        highlightbackground='white',
        highlightthickness=1
    )

    toggle_btn = Button(head_frame,
        text='☰',
        bg=btn3_dark_green,
        fg='white',
        font=('bold', 20),
        bd=0,
        activebackground=btn3_dark_green,
        activeforeground='white',
        command=toggle_menu
    )
    toggle_btn.pack(side=LEFT)

    title_lb = Label(
        head_frame, 
        text='Menu', 
        bg=btn3_dark_green,
        fg='white',
        font=('bold', 20)
    )
    title_lb.pack(side=LEFT)

    def logout():
        global is_logged_in, done_with_program
        is_logged_in = False
        done_with_program = False
        app.destroy()
        setup_desktop_app(False)

    logout_btn = Button(head_frame,
        text='Log Out',
        bg=btn3_dark_green,
        fg='white',
        font=('bold', 17),
        bd=0,
        activebackground=btn3_dark_green,
        activeforeground='white',
        command=logout
    )
    logout_btn.pack(side=RIGHT, padx=(0,5))

    hello_lb = Label(
        head_frame, 
        text=f"Hello, {username}!", 
        bg=btn3_dark_green,
        fg='white',
        font=('bold', 20)
    )

    hello_lb.pack(side=RIGHT, padx=(0, 20))

    head_frame.place(x=0, y=0)
    head_frame.pack_propagate(False)
    head_frame.config(width=1910, height=50)

# Displays user's personalized dashboard
def dashboard_screen():
    # Create a new frame for the dashboard
    dashboard_frame = Frame(app, width=1910, height=990, bg=bg_color)
    dashboard_frame.place(x=0, y=0)
    setup_frame(dashboard_frame)

    title = Label(dashboard_frame, text="My Dashboard", background=bg_color, font=("Times", 40, 'bold'))
    title.place(x=955, y=90, anchor=CENTER)

    # Load user data from CSV file
    df = pd.read_csv("user_data/detection_data.csv")
    disease_counts = df.loc[df['username'] == username, 'healthy_or_no'].value_counts()
    crop_counts = df.loc[(df['username'] == username) & (df['predicted_disease'] != 'Healthy'), 'crop'].value_counts()

    # If there's enough data for this user, then display the charts
    if ((not df.loc[df.username == username].empty) and (len(dict(disease_counts)) == 2)) and (not crop_counts.empty):
        # Create a pie chart for disease vs healthy detections
        fig1 = plt.figure(figsize=(6, 4))
        ax1 = fig1.add_subplot(111)
        ax1.pie(disease_counts, labels=["Contains Disease", "Healthy"], autopct='%1.1f%%', startangle=90, colors=['#88bf94', '#ace6b9'])
        ax1.axis('equal')
        ax1.set_title('Distribution of Crop Health: Healthy vs. Diseased Detections')
        fig1.patch.set_edgecolor('#88bf94')
        fig1.patch.set_linewidth(3)
        canvas1 = FigureCanvasTkAgg(fig1, master=dashboard_frame)
        canvas1.draw()
        
        # Create a bar chart for number of diseases detected per crop
        if len(crop_counts) > 5:
            width = len(crop_counts)
        else:
            width = 5
        fig2 = plt.figure(figsize=(width, 4))
        ax2 = fig2.add_subplot(111)
        ax2.bar(crop_counts.index, crop_counts, color='#88bf94')
        ax2.set_title("Number of Disease Detections per Crop")
        ax2.set_xlabel("Crop")
        ax2.set_ylabel("Disease Count")
        plt.xticks(rotation=45, ha='right')
        fig2.patch.set_edgecolor('#88bf94')
        fig2.patch.set_linewidth(2)
        plt.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, master=dashboard_frame)
        canvas2.draw()

        # Make the placement of everything dynamic, based on the width of the bar graph
        canvas1_width = canvas1.get_width_height()[0]
        canvas2_width = canvas2.get_width_height()[0]
        total_canvas_width = canvas1_width + canvas2_width
        space_between = (1910 - total_canvas_width) // 3
        canvas1.get_tk_widget().place(x=space_between, y=160, anchor='nw')
        canvas2.get_tk_widget().place(x=space_between * 2 + canvas1_width, y=160, anchor='nw')

        # Create a scrollable checklist that displays sustainable solutions (personalized per user)
        def load_checklist():
            try:
                with open("user_data/sustainability_checklist.txt", "r") as file:
                    for line in file:
                        user, item, checked = line.strip().split('|')
                        if user == username:
                            var = BooleanVar(value=(checked == 'True'))
                            checkboxes[item] = var
            except FileNotFoundError:
                pass

        def save_checklist():
            data = []
            try:
                with open('user_data/sustainability_checklist.txt', 'r') as file:
                    data = file.readlines()
            except FileNotFoundError:
                pass
            
            user_checklist = {item: var.get() for item, var in checkboxes.items()}
            new_data = []
            for line in data:
                user, item, checked = line.strip().split('|')
                if user == username:
                    if item in user_checklist:
                        checked = str(user_checklist[item])
                    else:
                        continue
                    new_data.append(f"{user}|{item}|{checked}")
                else:
                    new_data.append(line.strip())

            for item, checked in user_checklist.items():
                if not any(line.startswith(f"{username}|{item}|") for line in new_data):
                    new_data.append(f"{username}|{item}|{checked}")
            with open("user_data/sustainability_checklist.txt", 'w') as file:
                for line in new_data:
                    file.write(line + "\n")

        checklist_frame = Frame(dashboard_frame, bg='#88bf94')
        checklist_frame.place(x=space_between, y=650)

        Label(dashboard_frame, text="Sustainability Checklist:", background=bg_color, font=("Arial", 16)).place(x=space_between, y=615)
        # Vertical scrollbar
        v_scrollbar = Scrollbar(checklist_frame, orient=VERTICAL, bg='#88bf94', troughcolor=btn2_light_green)
        v_scrollbar.pack(side=RIGHT, fill=Y)

        # Horizontal scrollbar
        h_scrollbar = Scrollbar(checklist_frame, orient=HORIZONTAL, bg='#88bf94', troughcolor=btn2_light_green)
        h_scrollbar.pack(side=BOTTOM, fill=X)

        canvas = Canvas(checklist_frame, bg='#88bf94', yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Configure scrollbars
        v_scrollbar.config(command=canvas.yview)
        h_scrollbar.config(command=canvas.xview)

        checkbox_frame = Frame(canvas, bg='#88bf94')
        canvas.create_window((0, 0), window=checkbox_frame, anchor=NW)

        checkboxes = {}
        load_checklist()
        solutions = []

        # Load sustainable solutions and remove duplicates
        for input_list in (df.loc[(df['username'] == username), 'sustainable_solutions']):
            if input_list != "[]":
                input_list = input_list[1:-1].split('\', ')
                for solution in input_list:
                    new_solution = solution[1:]
                    if new_solution[-1] == '\'':
                        new_solution = new_solution[:-1]
                    input_list[input_list.index(solution)] = new_solution
                solutions += input_list
        solutions = list(set(solutions))

        # Create checkboxes with styled appearance
        for item in solutions:
            var = checkboxes.get(item, BooleanVar(value=False))
            checkboxes[item] = var
            checkbox = Checkbutton(
                checkbox_frame, 
                text=item, 
                variable=var,
                bg='#88bf94',
                fg='black',
                font=('Arial', 14),
                selectcolor=bg_color,
                activebackground=btn2_light_green,
                activeforeground='black'
            )
            checkbox.pack(anchor=W)
        checkbox_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        canvas.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))
        checklist_frame.config(width=850, height=250)
        checkbox_frame.config(width=850, height=250)
        canvas.config(width=850, height=250)
        save_checklist_btn = Button(dashboard_frame, text="Save Checklist", command=save_checklist, background=btn2_dark_green, foreground='white', font=('Arial', 20))
        save_checklist_btn.place(x=425 + space_between, y=925, anchor=N)

        # Create feature for user to look back at disease info (for only detected diseases)
        # Prompts user to select a crop
        select_label = Label(
            dashboard_frame,
            text="View Info for a Disease:",
            background=bg_color,
            font=("Arial", 16)
        )
        select_label.place(x=(1060 - space_between * 2) // 2  + space_between + 850, y=675, anchor=CENTER)

        global caret_down_img_white
        caret_down_img_white = ImageTk.PhotoImage(Image.open('assets/caret-down-white-icon.png').resize((15, 15)))
        options = sorted(list(set(list(df.loc[(df['username'] == username), 'crop']))))
        variable1 = StringVar(dashboard_frame)
        variable1.set("Crop")
        option_menu1 = OptionMenu(dashboard_frame, variable1, *options)
        option_menu1.place(x=(1060 - space_between * 2) // 2  + space_between + 850, y=725, anchor=CENTER)

        menu = dashboard_frame.nametowidget(option_menu1.menuname)
        option_menu1.config(
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
            activeborder=3,
        )

        options = sorted(list(set(list(df.loc[(df['username'] == username) & (df['predicted_disease'] != 'Healthy'), 'predicted_disease']))))
        variable2 = StringVar(dashboard_frame)
        variable2.set("Disease")
        option_menu2 = OptionMenu(dashboard_frame, variable2, *options)
        option_menu2.place(x=(1060 - space_between * 2) // 2  + space_between + 850, y=800, anchor=CENTER)

        menu = dashboard_frame.nametowidget(option_menu2.menuname)
        option_menu2.config(
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
            width=400
        )

        menu.config(
            bg=color_bg1,
            fg=color_fg1,
            activebackground=color_bg2,
            activeforeground=color_fg2,
            font=('Arial', 16),
            border=0,
            activeborder=3,
        )

        crop_name = ""
        disease_name = ""
        # If the user selects a crop and clicks the checkbox, it is no longer editable
        def view_info():
            crop_name = variable1.get()
            disease_name = variable2.get()

            if crop_name == "Crop" or disease_name == "Disease":
                messagebox.showerror("Invalid", "Must select a crop and disease")
            # If user tries to finalize selection and does not pick, display error message
            elif disease_name not in os.listdir(f"Image_Datasets/{crop_name}"):
                messagebox.showerror("Error", "The selected disease does not match the selected crop")
            else:
                map = text_to_map(crop_name, disease_name)
                sustainable = generate_sustainable_solutions(map)
                option_menu1.configure(state="disabled")
                option_menu2.configure(state="disabled")
                dashboard_frame.destroy()
                new_frame = Frame(app, width=1910, height=990)
                new_frame.place(x=0, y=0)
                setup_frame(new_frame)
                title = Label(new_frame, text=f"Information for {disease_name}", background=bg_color, font=("Times", 40, 'bold'))
                title.place(x=955, y=90, anchor=CENTER)

                back_to_dashboard = Button(
                    new_frame,
                    text="Back to Dashboard",
                    command=dashboard_screen,
                    background=btn3_dark_green,
                    foreground = 'white',
                    activebackground=btn1_light_green,
                    activeforeground='white',
                    highlightthickness=2,
                    highlightbackground=btn3_dark_green,
                    highlightcolor='white', font=('Arial', 20))
                back_to_dashboard.place(x=1850, y=90, anchor=E)

                overview_title = Label(new_frame, text="Overview", background=bg_color, font=("Times", 23, 'bold'))
                overview_text = Label(new_frame, text=map["Overview"], background= bg_color, font=("Arial", 13), wraplength=1000, justify=LEFT)
                overview_title.place(x=955, y=170, anchor=CENTER)
                overview_text.place(x=955, y=200, anchor='n')

                # Coordinates list for placement of labels & headings
                coords = [[475, 330], [1400, 350], [475, 550], [1400, 550]]
                i = 0
                for heading in map:
                    if heading == "Overview" or heading == "Source":
                        continue
                    if map[heading] != "":
                        title_label = Label(new_frame, text=heading, background=bg_color, font=("Times", 23, 'bold'))
                        text_label = Label(new_frame, text=map[heading], background=bg_color, font=("Arial", 13), wraplength=850, justify=LEFT)
                        title_label.place(x=coords[i][0], y=coords[i][1], anchor=CENTER)
                        text_label.place(x=coords[i][0], y=coords[i][1] + 30, anchor='n')
                        if heading == "Treatments/Solutions":
                            bottom_y_treat = 580 + text_label.winfo_reqheight()
                        elif heading == "Prevention":
                            bottom_y_prevent = 580 + text_label.winfo_reqheight()                
                        i += 1
                
                source_label = Label(new_frame, text=f"Website Source:\n{map['Source']}", background=bg_color, font=("Arial", 13))
                source_label.place(x=475, y=(990 - bottom_y_treat) // 2 + bottom_y_treat, anchor=CENTER)

                # Displays sustainable suggestions, with a button to toggle visibility
                solution_text = ""
                for solution in sustainable:
                    if solution_text == "":
                        solution_text += " - " + solution + "\n"
                    else:
                        solution_text += " - " + solution + "\n"
                sustainable_label = Label(
                    new_frame, text=" " + solution_text.strip(), 
                    background=middle_green, font=("Arial", 13), borderwidth=2, relief="solid", 
                    wraplength=850, justify=LEFT
                )

                def toggle_label():
                    if sustainable_label.winfo_ismapped():
                        sustainable_label.place_forget()
                    else:
                        sustainable_label.place(x=1400, y=bottom_y_prevent + 80, anchor='n')
                    
                sustainable_button = Button(
                    new_frame,
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

        # Button to launch new_frame
        info_btn = Button(dashboard_frame, text="Go!", command=view_info, background=btn2_dark_green, foreground='white', font=('Arial', 20))
        info_btn.place(x=(1060 - space_between * 2) // 2  + space_between + 850, y=875, anchor=CENTER)
    
    # If there's not enough data for the user yet
    else:
        no_data_label = Label(dashboard_frame, text="Not enough detection data.", bg=bg_color, font=("Arial", 20))
        no_data_label.place(x=955, y=450, anchor=CENTER)

        info_btn = Button(dashboard_frame,
            text="Detect a Disease",
            command=detection_screen,
            background=btn2_dark_green,
            foreground='white',
            font=('Arial', 20)
        )
        info_btn.place(x=955, y=525, anchor=CENTER)

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
    overview_text += "Once a disease is identified, the application uses a prefabricated corpus and natural language processing (NLP) to extract relevant information about the symptoms and treatment options. "
    overview_text += "This information is then curated to emphasize environmentally friendly and sustainable practices. "
    overview_text += "Overall, the project not only facilitates timely interventions for crop diseases, but also educates users about sustainable agricultural practices. "
    overview_text += "The app also contains personalized data charts and other features based on their detected diseases. "
    overview_text += "A key feature of our application is its scalability; although it currently supports a limited range of crop types and diseases, we can easily add more training datasets to expand its capabilities in the future."

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
                text="Loading trained model...",
                background=bg_color,
                font=("Arial", 26)
            )
            
            detecting_label.place(x=955, y=175, anchor=CENTER)
    
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
    # Loading Circle Animation
    class LoadingCircle(Canvas):
        def __init__(self, master, size=400, num_segments=8, segment_length=60, color='green', animation_speed=100):
            super().__init__(master, width=size, height=size, highlightthickness=0, bg=bg_color)
            self.size = size
            self.num_segments = num_segments
            self.segment_length = segment_length
            self.color = color
            self.animation_speed = animation_speed
            self.angle = 0
            self.segments = []

        def start(self):
            self.is_running = True
            self.create_segments()

            self.animate()

        def stop(self):
            self.is_running = False

        def create_segments(self):
            center = self.size / 2
            outer_radius = center - 20
            inner_radius = outer_radius - self.segment_length

            for i in range(self.num_segments):
                angle_deg = i * 360 / self.num_segments
                angle_rad = math.radians(angle_deg)

                x1 = center + inner_radius * math.cos(angle_rad)
                y1 = center + inner_radius * math.sin(angle_rad)
                x2 = center + outer_radius * math.cos(angle_rad)
                y2 = center + outer_radius * math.sin(angle_rad)

                segment = self.create_line(x1, y1, x2, y2, width=6, fill=self.color, state=HIDDEN)
                self.segments.append(segment)

        def animate(self):
            if self.is_running:
                for i in range(self.num_segments):
                    self.itemconfigure(self.segments[(i + self.angle) % self.num_segments], state=NORMAL)
                    self.itemconfigure(self.segments[(i + self.angle - 3) % self.num_segments], state=HIDDEN)
                self.angle = (self.angle + 1) % self.num_segments
                self.after(self.animation_speed, self.animate)
            else:
                for segment in self.segments:
                    self.delete(segment)
                self.segments.clear()
                

    # Create a thread so that the program will both run classify image AND display loading circle
    def start_training():
        global loading_frame
        loading_frame = Frame(detect_frame, width=450, height=450, bg=bg_color)
        loading_frame.place(x=955, y=455, anchor=CENTER)

        loading = LoadingCircle(loading_frame)
        loading.pack()
        loading.start()

        thread = threading.Thread(target=run_training, daemon = True, args=(loading,)).start()
        
    def run_training(loading):
        def update_status(message):
            detecting_label.config(text=message)
        # Predict the disease using the classify_image function
        global predicted_disease, percent_conf
        predicted_disease, percent_conf = classify_image(crop, filepath, update_status)

        update_status("Loading Results...")
        global map, sustainable
        if predicted_disease != "Healthy":
            map = text_to_map(crop, predicted_disease)
            sustainable = generate_sustainable_solutions(map)
        else:
            sustainable = []
        update_status("Results are Ready!")

        loading.stop()
        img = Image.open("assets/check_circle.png")
        img = img.resize((400, 400), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        global check_pic
        check_pic = Label(detect_frame, image=img_tk, bg=bg_color)
        check_pic.image = img_tk
        check_pic.place(x=955, y=410, anchor=CENTER)
        results_button.place(x=955, y=800, anchor=CENTER)


    def save_user_data(crop, predicted_disease, percent_conf, sustainable):
        if predicted_disease == "Healthy":
            healthy = True
        else:
            healthy = False
        data = {
            'username': username,
            'crop': crop,
            'predicted_disease': predicted_disease,
            'confidence': percent_conf,
            'healthy_or_no': healthy,
            'sustainable_solutions': sustainable
        }
        
        df = pd.DataFrame([data])
        
        # Append to CSV file
        file_path = "user_data/detection_data.csv"
        if not os.path.isfile(file_path):
            df.to_csv(file_path, index=False)
        else:
            df.to_csv(file_path, mode='a', header=False, index=False)


    # Changes the screen to display all information on the disease
    def view_results():
        results_button.destroy()
        detecting_label.destroy()
        loading_frame.destroy()
        check_pic.destroy()
        title.config(text="Results")

        rectangle = Label(detect_frame, text="", background=middle_green, borderwidth=2, relief="solid", width=72, height=6)
        disease_label = Label(detect_frame, text=f"Predicted Disease: {predicted_disease}", background=middle_green, font=("Times", 22, 'bold'))
        percent_label = Label(detect_frame, text=f"Percent Confidence: {percent_conf}", background=middle_green, font=("Arial", 15))
        
        # Save the user data
        save_user_data(crop, predicted_disease, percent_conf, sustainable)

        # If some disease was detected
        if predicted_disease != "Healthy":
            rectangle.place(x=155, y=160, anchor='nw')
            disease_label.place(x=475, y=195, anchor=CENTER)  
            percent_label.place(x=475, y=230, anchor=CENTER)

            overview_title = Label(detect_frame, text="Overview", background=bg_color, font=("Times", 23, 'bold'))
            overview_text = Label(detect_frame, text=map["Overview"], background= bg_color, font=("Arial", 13), wraplength=900, justify=LEFT)
            overview_title.place(x=1400, y=170, anchor=CENTER)
            overview_text.place(x=1400, y=200, anchor='n')

            # Coordinates list for placement of labels & headings
            coords = [[475, 330], [1400, 350], [475, 550], [1400, 550]]
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
    file = open("Text_Files/inspiration.txt", "r")
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
    sources_file = open("Text_Files/sources.txt", "r", errors="ignore")
    lines = sources_file.readlines()
    sources_file.close()

    listbox.insert(END, "")
    for line in lines:
        listbox.insert(END, "   " + line.rstrip())
    
    listbox.place(x=955, y=575, width=1400, height=700, anchor=CENTER)
    scrollbar.place(x=1655, y=225, height=700)
