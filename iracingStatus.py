from pyracing import constants as ct
import tkinter as tk
from PIL import Image, ImageTk
from pyracing.helpers import encode_password
import httpx
import time
import asyncio

URL_FAILEDLOGIN = 'https://members.iracing.com/membersite/failedlogin.jsp'


async def authenticate(username, password):
    password_enc = encode_password(username, password)
    session = httpx.AsyncClient()

    login_data = {
        'username': username,
        'password': password_enc,
        'utcoffset': round(abs(time.localtime().tm_gmtoff / 60)),
        'todaysdate': ''  # Unknown purpose, but exists as a hidden form.
    }

    auth_response = await session.post(ct.URL_LOGIN2, data=login_data)
    await session.aclose()
    return auth_response

def update_status(root, canvas, label, green_photo, red_photo, username, password):
    auth_response = asyncio.run(authenticate(username, password))

    # Check if authentication was successful
    if auth_response.url == ct.URL_HOME:
        # Update the label with the success message
        label.config(text="Login successful. Online")

        # Display the green ball
        canvas.create_image(25, 25, anchor=tk.CENTER, image=green_photo)
    elif auth_response.url == ct.URL_MAINTENANCE:
        # Update the label with the failure message
        label.config(text="Login successful. Servers in Maintenance Mode")

        # Display the red ball
        canvas.create_image(25, 25, anchor=tk.CENTER, image=red_photo)
    
    elif auth_response.url == URL_FAILEDLOGIN:
        # Update the label with the failure message
        label.config(text="Failed Login. Bad Credentials")


    # Schedule the update_status function to run again after 30 seconds
    root.after(30000, lambda: update_status(root, canvas, label, green_photo, red_photo, username, password))

def run_app():
    # Get username and password from console input
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Create a Tkinter window
    root = tk.Tk()
    root.title("iRacing Status")

    # Load green and red balls
    green_image = Image.open("green_ball.png")  # Replace with your green ball image
    red_image = Image.open("red_ball.png")  # Replace with your red ball image

    green_photo = ImageTk.PhotoImage(green_image)
    red_photo = ImageTk.PhotoImage(red_image)

    # Create a canvas to display the ball
    canvas = tk.Canvas(root, width=50, height=50)
    canvas.pack()

    # Create a label for displaying login status messages
    status_label = tk.Label(root, text="", font=("Helvetica", 12))
    status_label.pack()

    # Run the update_status function initially
    update_status(root, canvas, status_label, green_photo, red_photo, username, password)

    # Start the Tkinter event loop
    root.mainloop()

# Run the app
run_app()
