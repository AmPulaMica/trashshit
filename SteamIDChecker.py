import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser
import base64
import sys
import os
import platform
import subprocess
import threading

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_key():
    b = ""
    return base64.b64decode(b).decode()

def is_debugger_present():
    return sys.gettrace() is not None

def is_vm():
    vm_signs = ["VBOX", "VIRTUAL", "VMWARE", "HYPER-V", "QEMU", "XEN"]
    try:
        if platform.system() == "Windows":
            output = subprocess.check_output('wmic computersystem get model', shell=True).decode()
            for sign in vm_signs:
                if sign in output.upper():
                    return True
        elif platform.system() == "Linux":
            output = subprocess.check_output('systemd-detect-virt', shell=True).decode().strip()
            if output != "none":
                return True
    except Exception:
        pass
    return False

if is_debugger_present():
    print("Debugger detected. Exiting.")
    sys.exit(1)

if is_vm():
    print("Virtual Machine detected. Exiting.")
    sys.exit(1)

API_KEY = get_key()

# Colors
BG_COLOR = "#121212"
CARD_BG = "#1e1e1e"
FG_COLOR = "#e0e0e0"
ACCENT_COLOR = "#00aaff"
ENTRY_BG = "#222222"
BTN_BG = "#333333"
BTN_HOVER_BG = "#005577"

PERSONA_STATES = {
    0: "Offline",
    1: "Online",
    2: "Busy",
    3: "Away",
    4: "Snooze",
    5: "Looking to Trade",
    6: "Looking to Play"
}

def open_profile(url):
    webbrowser.open(url)

def on_enter_btn(e):
    e.widget.config(bg=BTN_HOVER_BG)

def on_leave_btn(e):
    e.widget.config(bg=BTN_BG)

def lookup_steam_id():
    steamid = entry.get().strip()

    if not steamid.isdigit() or len(steamid) != 17:
        messagebox.showerror("Invalid SteamID64", "Please enter a valid 17-digit SteamID64.")
        return

    lookup_btn.config(state=tk.DISABLED)

    def fetch():
        try:
            summary_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={API_KEY}&steamids={steamid}"
            summary = requests.get(summary_url).json()["response"]["players"]
            if not summary:
                raise Exception("No player data found for this SteamID.")
            summary = summary[0]

            ban_url = f"https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={API_KEY}&steamids={steamid}"
            bans = requests.get(ban_url).json()["players"][0]

            owned_games_url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={API_KEY}&steamid={steamid}"
            owned_games_data = requests.get(owned_games_url).json()
            owned_games_count = owned_games_data.get("response", {}).get("game_count", "N/A")

            level_url = f"https://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?key={API_KEY}&steamid={steamid}"
            level_data = requests.get(level_url).json()
            steam_level = level_data.get("response", {}).get("player_level", "N/A")

            name = summary["personaname"]
            profile_url = summary["profileurl"]
            avatar_url = summary["avatarfull"]
            visibility = "Public" if summary["communityvisibilitystate"] == 3 else "Private"
            vac_bans = bans["NumberOfVACBans"]
            game_bans = bans["NumberOfGameBans"]
            persona_state_code = summary.get("personastate", 0)
            persona_state = PERSONA_STATES.get(persona_state_code, "Unknown")

            def update_ui():
                # Avatar
                img_data = requests.get(avatar_url).content
                avatar_img = Image.open(BytesIO(img_data)).resize((180, 180))
                avatar_photo = ImageTk.PhotoImage(avatar_img)
                avatar_label.config(image=avatar_photo)
                avatar_label.image = avatar_photo

                # Name
                name_label.config(text=name)

                # Profile Button
                def open_prof(event=None):
                    open_profile(profile_url)
                profile_btn.config(state=tk.NORMAL)
                profile_btn.bind("<Button-1>", open_prof)

                # Info Labels
                info_labels["Steam Level"].config(text=f"{steam_level}")
                info_labels["Status"].config(text=persona_state)
                info_labels["VAC Bans"].config(text=f"{vac_bans}")
                info_labels["Game Bans"].config(text=f"{game_bans}")
                info_labels["Visibility"].config(text=visibility)
                info_labels["Owned Games"].config(text=f"{owned_games_count}")

                lookup_btn.config(state=tk.NORMAL)

            root.after(0, update_ui)

        except Exception as e:
            root.after(0, lambda: [
                messagebox.showerror("Error", f"Failed to fetch Steam data: {e}"),
                lookup_btn.config(state=tk.NORMAL)
            ])

    threading.Thread(target=fetch, daemon=True).start()

root = tk.Tk()
root.title("SteamID Lookup")
root.geometry("480x680")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

try:
    root.iconbitmap(resource_path("test.ico"))
except:
    pass

FONT_LARGE = ("Segoe UI", 24, "bold")
FONT_MEDIUM = ("Segoe UI", 14)
FONT_SMALL = ("Segoe UI", 11)

# --- Top input area ---
top_frame = tk.Frame(root, bg=BG_COLOR)
top_frame.pack(pady=15, padx=20, fill='x')

tk.Label(top_frame, text="Enter SteamID64:", fg=FG_COLOR, bg=BG_COLOR, font=FONT_MEDIUM).pack(anchor='w')

input_frame = tk.Frame(top_frame, bg=BG_COLOR)
input_frame.pack(fill='x', pady=8)

entry = tk.Entry(input_frame, font=FONT_MEDIUM, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR, relief=tk.FLAT)
entry.pack(side='left', fill='x', expand=True, ipady=6)

lookup_btn = tk.Button(input_frame, text="Lookup", font=FONT_MEDIUM, bg=BTN_BG, fg=FG_COLOR, relief=tk.FLAT, command=lookup_steam_id, width=12, cursor="hand2")
lookup_btn.pack(side='left', padx=(10,0))
lookup_btn.bind("<Enter>", on_enter_btn)
lookup_btn.bind("<Leave>", on_leave_btn)

# --- Avatar ---
avatar_label = tk.Label(root, bg=BG_COLOR, bd=3, relief="groove")
avatar_label.pack(pady=10)

# --- Username ---
name_label = tk.Label(root, text="", fg=ACCENT_COLOR, bg=BG_COLOR, font=FONT_LARGE)
name_label.pack(pady=(5, 0))

# --- Profile Button ---
profile_btn = tk.Label(root, text="View Steam Profile", fg=ACCENT_COLOR, bg=BG_COLOR, font=FONT_MEDIUM, cursor="hand2")
profile_btn.pack(pady=(0, 15))
profile_btn.config(state=tk.DISABLED)

# --- Info Card ---
info_card = tk.Frame(root, bg=CARD_BG, bd=0, relief="ridge")
info_card.pack(padx=25, pady=10, fill="both")

# We'll arrange info labels in two columns for neatness
info_labels = {}

left_col_keys = ["Steam Level", "VAC Bans", "Visibility"]
right_col_keys = ["Status", "Game Bans", "Owned Games"]

for i, key in enumerate(left_col_keys):
    lbl_key = tk.Label(info_card, text=key + ":", bg=CARD_BG, fg=FG_COLOR, font=FONT_MEDIUM, anchor="w")
    lbl_key.grid(row=i, column=0, sticky="w", padx=15, pady=10)
    lbl_val = tk.Label(info_card, text="", bg=CARD_BG, fg=ACCENT_COLOR, font=FONT_MEDIUM, anchor="w")
    lbl_val.grid(row=i, column=1, sticky="w", padx=5, pady=10)
    info_labels[key] = lbl_val

for i, key in enumerate(right_col_keys):
    lbl_key = tk.Label(info_card, text=key + ":", bg=CARD_BG, fg=FG_COLOR, font=FONT_MEDIUM, anchor="w")
    lbl_key.grid(row=i, column=2, sticky="w", padx=15, pady=10)
    lbl_val = tk.Label(info_card, text="", bg=CARD_BG, fg=ACCENT_COLOR, font=FONT_MEDIUM, anchor="w")
    lbl_val.grid(row=i, column=3, sticky="w", padx=5, pady=10)
    info_labels[key] = lbl_val

# Add some grid column weight for spacing
info_card.grid_columnconfigure(0, weight=1)
info_card.grid_columnconfigure(2, weight=1)

# --- Footer ---
footer = tk.Label(root, text="Powered by Steam Web API", fg="#666666", bg=BG_COLOR, font=FONT_SMALL)
footer.pack(side="bottom", pady=12)

root.mainloop()
