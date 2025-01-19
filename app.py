import tkinter as tk
from tkinter import messagebox
import requests
import base64
import json

# Function to authenticate API requests
def authenticate(username, password):
    # This example assumes Basic Authentication for the API
    auth_header = "Basic " + base64.b64encode(f"{username}:{password}".encode()).decode()
    return auth_header

# Function to fetch houses from the API
def get_houses(auth_header, api_url):
    response = requests.get(f"{api_url}/houses", headers={"Authorization": auth_header})
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to add points to a house
def add_points(auth_header, house_name, points, reason, api_url):
    data = {
        "house": house_name,
        "points": points,
        "reason": reason
    }
    response = requests.post(f"{api_url}/add_points", json=data, headers={"Authorization": auth_header})
    if response.status_code == 200:
        return response.json()['message']
    else:
        return response.json().get('error', 'Unknown error')

# Function to handle login and fetching houses
def on_login():
    username = username_entry.get()
    password = password_entry.get()
    api_url = api_url_entry.get()

    if not username or not password or not api_url:
        messagebox.showerror("Input Error", "Please enter username, password, and API URL.")
        return

    auth_header = authenticate(username, password)

    # Fetch houses from the API
    houses = get_houses(auth_header, api_url)
    if houses is not None:
        house_list.delete(0, tk.END)  # Clear the existing list
        for house in houses:
            house_list.insert(tk.END, house)  # Add house names to the list
    else:
        messagebox.showerror("API Error", "Failed to fetch houses. Check your credentials or server.")

# Function to handle adding points to a house
def on_add_points():
    username = username_entry.get()
    password = password_entry.get()
    house_name = house_list.get(tk.ACTIVE)
    points = points_entry.get()
    reason = reason_entry.get()
    api_url = api_url_entry.get()

    if not house_name or not points or not reason or not api_url:
        messagebox.showerror("Input Error", "Please fill all fields.")
        return

    try:
        points = int(points)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number of points.")
        return

    auth_header = authenticate(username, password)
    result = add_points(auth_header, house_name, points, reason, api_url)

    messagebox.showinfo("Result", result)

# Set up the Tkinter application
root = tk.Tk()
root.title("House Points Application")

# Create input fields for API URL, username, and password
api_url_label = tk.Label(root, text="API URL:")
api_url_label.pack()

api_url_entry = tk.Entry(root)
api_url_entry.pack()
api_url_entry.insert(0, "http://localhost:5000/api")  # Default API URL

username_label = tk.Label(root, text="Username:")
username_label.pack()

username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Password:")
password_label.pack()

password_entry = tk.Entry(root, show="*")
password_entry.pack()

login_button = tk.Button(root, text="Login", command=on_login)
login_button.pack()

# Listbox to display houses
house_list_label = tk.Label(root, text="Houses:")
house_list_label.pack()

house_list = tk.Listbox(root)
house_list.pack()

# Input fields for adding points
points_label = tk.Label(root, text="Points to Add:")
points_label.pack()

points_entry = tk.Entry(root)
points_entry.pack()

reason_label = tk.Label(root, text="Reason for Adding Points:")
reason_label.pack()

reason_entry = tk.Entry(root)
reason_entry.pack()

add_points_button = tk.Button(root, text="Add Points", command=on_add_points)
add_points_button.pack()

# Run the Tkinter application
root.mainloop()
