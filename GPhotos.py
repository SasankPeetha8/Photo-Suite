from tkinter import *
from PIL import ImageTk, Image
from selenium import webdriver
#from bs4 import BeautifulSoup
#import requests
import time
import os
import glob
#Clear user_data
#os.remove("./data/user_data/Login_data.txt")

#Window Size Calculation.
def windows_size():
	display_width = window.winfo_screenwidth()
	display_height = window.winfo_screenheight()
	width_percent = 0.2
	height_percent = 0.2
	width = int(display_width - ( display_width*width_percent))
	height = int(display_height - ( display_height*height_percent))
	position_x = int((display_width/2)-(width/2))
	position_y = int((display_height/2)-(height/2))
	window.geometry('%dx%d+%d+%d' % (width, height, position_x, position_y))
	window.resizable(0,0)
	return width, height

#Definition to get input from Entry Boxes.
def getInput():
    global username
    global password
    username = username_box.get()
    password = password_box.get()
    login_details = open("./data/user_data/Login_data.txt","w")
    login_details.write(username)
    login_details.write("\n")
    login_details.write(password)
    login_details.close()
    window.destroy()

#Definition to read User Login Details.
def login_info():
	a = glob.glob("./data/user_data/Login_data.txt")
	if len(a) != 0:
		login_details = open("./data/user_data/Login_data.txt","r")
		username = login_details.readlines(1)
		password = login_details.readlines(2)
		login_details.close()
		return username, password
	else:
		return None, None

#Clearing previous login data
#os.chdir("./data/user_data")
a = glob.glob("./data/user_data/Login_data.txt")
if len(a) != 0:
	os.remove("./data/user_data/Login_data.txt")

#Window Configuration
window = Tk()
window.title("Uploader For Google Photos")
window.iconbitmap("./data/pics/icon.ico")
window.configure(bg="white")
width, height = windows_size()
window.configure(width=width, height=height, bg="white")
image=ImageTk.PhotoImage(Image.open("./data/pics/google_photos1.jpg"))
display_image = Label(window, image=image, bg="white")
display_image.pack()

#Login Data Text.
display_text = Label(window, text="Sign in into Google Account to access Google Photos",
					font="Times 12 italic", fg="#676767", bg="white")
username_text = Label(window, text="\n Email or phone:", font="Calibri 11", bg="white")
password_text = Label(window, text="\n Password:", font="Calibri", bg="white")
#Entry Boxes to Enter Usernames and Passwords
username_box = Entry(window, bd=1.8, width=25)
password_box = Entry(window, show="*", bd=1.8, width=25)

#Layout for "Login Data Text" and "Entry Boxes".
display_text.pack(anchor="center")
username_text.place(relx=0.38, rely=0.684, anchor="w")
username_box.place(relx=0.63, rely=0.7, anchor="e")
password_text = Label(window, text="\n Password:", font="Calibri", bg="white")
password_text.place(relx=0.407, rely=0.748, anchor="w")
password_box.place(relx=0.63, rely=0.768, anchor="e")

#Login button details and layout.
login_button = Button(window, text="Login", font="Times 11 italic", fg="white",
				bg="#1a73e9", height=1, width=25, bd=0.8, command=getInput)
login_button.place(relx=0.41, rely=0.9)

#Close Window
window.mainloop()

username, password = login_info()

def browser_data(username, password):
	#Adjusting Strings
	username = str(username)
	password = str(password)
	username = username[2:int(len(username)-4)]
	password = password[2:int(len(username)-4)]
	# create a new Chrome session
	browser = webdriver.Chrome()
	url = "https://accounts.google.com/signin/v2/identifier?passive=1209600&continue=https%3A%2F%2Fphotos.google.com%2Flogin&followup=https%3A%2F%2Fphotos.google.com%2Flogin&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
	# navigate to the application home
	browser.get(url)
	#get the username textbox
	browser.find_element_by_name("identifier").send_keys(username)
	#enter username
	browser.find_element_by_id('identifierNext').click()
	time.sleep(5)
	#get the password textbox
	browser.find_element_by_name("password").send_keys(password)
	#enter password
	browser.find_element_by_id("passwordNext").click()
	time.sleep(10)
	url = "https://photos.google.com/albums"
	browser.get(url)

	album_list = []
	album_elements = browser.find_elements_by_xpath("""//*[@id="yDmH0d"]/c-wiz/div[3]/c-wiz/div/div[2]/c-wiz/div/div/div[1]/a/div[2]/div[1]""")
	for album in album_elements:
		album_list.append(album.text)
	
	album_items = []
	items_elements = browser.find_elements_by_xpath("""//*[@id="yDmH0d"]/c-wiz/div[3]/c-wiz/div/div[2]/c-wiz/div/div/div[1]/a/div[2]/div[2]""")
	for item in items_elements:
		album_items.append(item.text)

	album = dict(zip(album_list, album_items))
	print(album)

if username != None:
	browser_data(username, password)

