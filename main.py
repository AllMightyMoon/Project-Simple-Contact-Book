import json
import os
import re
import csv
from colorama import init, Fore

# Initialize colorama for Windows compatibility
init(autoreset=True)

CONTACTS_FILE = "contacts.json"

# Load contacts from file if it exists
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as file:
            return json.load(file)
    return {}

# Save contacts to file
def save_contacts():
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)

# Validate phone number (10 digits)
def is_valid_phone(phone):
    return re.fullmatch(r"\d{10}", phone) is not None

# Validate email format
def is_valid_email(email):
    return re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email) is not None

# Add a new contact
def add_contact():
    name = input(Fore.BLUE + "Enter contact name: ").strip().lower()
    if name in contacts:
        print(Fore.YELLOW + "Warning: Contact already exists!\n")
        return
    
    phone = input(Fore.BLUE + "Enter phone number: ").strip()
    while not is_valid_phone(phone):
        print(Fore.RED + "Error: Invalid phone number! Must be 10 digits.")
        phone = input(Fore.BLUE + "Enter phone number again: ").strip()
    
    email = input(Fore.BLUE + "Enter email (optional): ").strip()
    while email and not is_valid_email(email):
        print(Fore.RED + "Error: Invalid email format! Example: example@mail.com")
        email = input(Fore.BLUE + "Enter email again (optional): ").strip()
    
    contacts[name] = {"phone": phone, "email": email}
    save_contacts()
    print(Fore.GREEN + f"Success: Contact '{name.capitalize()}' added successfully!\n")

# View all contacts
def view_contacts():
    if not contacts:
        print(Fore.YELLOW + "Warning: No contacts found!\n")
        return
    print(Fore.BLUE + "\nContacts List:")
    for name, details in contacts.items():
        print(Fore.BLUE + f"Name: {name.capitalize()}, Phone: {details['phone']}, Email: {details['email']}")
    print()

# Search for a contact (case-insensitive)
def search_contact():
    name = input(Fore.BLUE + "Enter contact name to search: ").strip().lower()
    if name in contacts:
        print(Fore.GREEN + f"Found: Name: {name.capitalize()}, Phone: {contacts[name]['phone']}, Email: {contacts[name]['email']}\n")
    else:
        print(Fore.RED + "Error: Contact not found!\n")

# Update a contact
def update_contact():
    name = input(Fore.BLUE + "Enter the name of the contact to update: ").strip().lower()
    if name in contacts:
        phone = input(Fore.BLUE + "Enter new phone number: ").strip()
        while not is_valid_phone(phone):
            print(Fore.RED + "Error: Invalid phone number! Must be 10 digits.")
            phone = input(Fore.BLUE + "Enter phone number again: ").strip()
        
        email = input(Fore.BLUE + "Enter new email (optional): ").strip()
        while email and not is_valid_email(email):
            print(Fore.RED + "Error: Invalid email format! Example: example@mail.com")
            email = input(Fore.BLUE + "Enter email again (optional): ").strip()
        
        contacts[name] = {"phone": phone, "email": email}
        save_contacts()
        print(Fore.GREEN + f"Success: Contact '{name.capitalize()}' updated successfully!\n")
    else:
        print(Fore.RED + "Error: Contact not found!\n")

# Delete a contact
def delete_contact():
    name = input(Fore.BLUE + "Enter contact name to delete: ").strip().lower()
    if name in contacts:
        del contacts[name]
        save_contacts()
        print(Fore.GREEN + f"Success: Contact '{name.capitalize()}' deleted successfully!\n")
    else:
        print(Fore.RED + "Error: Contact not found!\n")

# Export contacts to CSV or HTML
def export_contacts():
    if not contacts:
        print(Fore.YELLOW + "Warning: No contacts to export!\n")
        return

    print(Fore.BLUE + "Select export format:")
    print(Fore.BLUE + "1. CSV File")
    print(Fore.BLUE + "2. HTML Table")
    choice = input(Fore.BLUE + "Enter your choice (1 or 2): ").strip()

    if choice == "1":
        filename = "contacts.csv"
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Phone", "Email"])
            for name, details in contacts.items():
                writer.writerow([name.capitalize(), details["phone"], details["email"]])
        print(Fore.GREEN + f"Success: Contacts exported successfully to {filename}!\n")

    elif choice == "2":
        filename = "contacts.html"
        with open(filename, "w") as file:
            file.write("<html><body><h2>Contact List</h2><table border='1'>")
            file.write("<tr><th>Name</th><th>Phone</th><th>Email</th></tr>")
            for name, details in contacts.items():
                file.write(f"<tr><td>{name.capitalize()}</td><td>{details['phone']}</td><td>{details['email']}</td></tr>")
            file.write("</table></body></html>")
        print(Fore.GREEN + f"Success: Contacts exported successfully to {filename}!\n")

    else:
        print(Fore.RED + "Error: Invalid choice! Export cancelled.\n")

# Main menu
def main():
    while True:
        print(Fore.CYAN + "Contact Book Menu:")
        print(Fore.CYAN + "1. Add Contact")
        print(Fore.CYAN + "2. View Contacts")
        print(Fore.CYAN + "3. Search Contact")
        print(Fore.CYAN + "4. Update Contact")
        print(Fore.CYAN + "5. Delete Contact")
        print(Fore.CYAN + "6. Export Contacts")
        print(Fore.CYAN + "7. Exit")
        
        choice = input(Fore.BLUE + "Enter your choice (1-7): ").strip()
        
        if choice == "1":
            add_contact()
        elif choice == "2":
            view_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            export_contacts()
        elif choice == "7":
            print(Fore.GREEN + "Exiting Contact Book. Goodbye!")
            break
        else:
            print(Fore.RED + "Error: Invalid choice! Please try again.\n")

# Load contacts at the start
contacts = load_contacts()

if __name__ == "__main__":
    main()
