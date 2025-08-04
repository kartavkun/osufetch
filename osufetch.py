__version__ = "1.4.0"

import os
import sys
import argparse
import httpx
from configparser import ConfigParser
from ossapi import Ossapi
from datetime import datetime
from colorama import Fore, Style, init

# === Initialize colorama for cross-platform coloring ===
init(autoreset=True)

# === Config defaults and paths ===
CONFIG_DIR = os.path.expanduser("~/.config/osufetch")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.ini")

ascii_arts = {
    "mania": """
         :!JPB#&@@@&#G5?~.         
      ^JB@@&BP5JJ?JY5G#@@&P?:      
    !G@@BJ~:     .    .:75&@&5^    
  ^G@@P~       !&&B.      .?#@@Y.  
 !&@&!         Y@@@^        .Y@@G. 
^&@&^    ~55!  J@@@^ .?5J:    J@@P 
G@@7     G@@#  J@@@^ ~@@@?     G@@7
@@&:     G@@#  J@@@^ ~@@@?     ?@@P
@@&:     G@@#  J@@@^ ~@@@?     ?@@P
G@@7     G@@#  J@@@^ ~@@@?     G@@7
^&@&^    ~55!  J@@@^ .?PY:    J@@P 
 !&@&!         Y@@@^        .Y@@G. 
  ^G@@P~       !&&B:      .?#@@Y.  
    7B@@BJ~.     .     :75&@@5^    
      ~YB@@&BP5J??JY5G#@@&G?:      
         :!JPB&&@@@&#B5?~.         
""",
    "osu": """
         :!JPB#&@@@&#G5?~.         
      ^JB@@&BP5J??JY5G#@@&P?:      
    !G@@BJ~.   ....    :75&@&5^    
  ^G@@P~  .!YG#&&&&#BPJ^  .?#@@Y.  
 !&@&!  :Y&@@@@@@@@@@@@@B?  .Y@@G. 
^&@&^  7&@@@@@@@@@@@@@@@@@G:  J@@P 
G@@7  !@@@@@@@@@@@@@@@@@@@@B.  G@@7
@@&:  P@@@@@@@@@@@@@@@@@@@@@!  ?@@P
@@&:  P@@@@@@@@@@@@@@@@@@@@@!  ?@@P
G@@7  !@@@@@@@@@@@@@@@@@@@@B.  G@@7
^&@&^  7&@@@@@@@@@@@@@@@@@B:  J@@P 
 !&@&!  :Y&@@@@@@@@@@@@@B?  .Y@@G. 
  ^G@@P~  .!YG#&&&&#BPJ^  .?#@@Y.  
    7B@@BJ~.   ....    :!5&@@5^    
      ~YB@@&BPYJ??JY5G#@@&G?:      
         :!JPB&&@@@&#B5?~.         
""",
    "taiko": """
         :!JPB#&@@@&#G5?~.         
      ^JB@@&BP5J??JY5G#@@&P?:      
    !G@@BJ~.   ....    :75&@&5^    
  ^G@@P~  .!YG#&&&&&#PJ^  .?#@@Y.  
 !&@&!  :Y&@@BYY@@#J5#@@B?  .Y@@G. 
^&@&^  7&@&J:  ^@@B   ~P@@G:  J@@P 
G@@7  !@@#^    ~@@B     7@@B.  G@@7
@@&:  P@@7     ~@@B      P@@!  ?@@P
@@&:  P@@7     ~@@B      P@@!  ?@@P
G@@7  !@@#^    ~@@B     7@@B.  G@@7
^&@&^  7&@&J:  ^@@B   ^5@@B:  J@@P 
 !&@&!  :Y&@@GYY@@#J5#@@B?  .Y@@G. 
  ^G@@P~  .!YG#&&&&&#PJ^  .?#@@Y.  
    7B@@BJ~.   ....    :!5&@@5^    
      ~YB@@&BPYJ??JY5G#@@&G?:      
         :!JPB&&@@@&#B5?~.         
""",
    "fruits": """
         :!JPB#&@@@&#B5?~:         
      ^JB@@&#G5YJJJY5G#@@&G?:      
    !G@@#Y!:           :!5&@@P~    
  :P@@G!                  .7B@@5.  
 ~&@&7      .JGBP!          .Y@@B: 
:#@&~       ?@@@@&.           ?@@G.
5@@J        .75PY~  ^~~.       P@@?
&@@:               P@@@&!      7@@G
&@@:              .P@@@&!      7@@G
5@@J        .75PY~  ^!~.       P@@?
:#@&~       ?@@@@&.           ?@@G.
 ~&@&7      .YGBP!          .J@@B: 
  :P@@G!                  .7B@@5.  
    !G@@#Y~:           :!5&@@P~    
      ^JB@@&BP5JJ?JY5G#@@&G?:      
         :!JPB#&@@@&#B5J~:         
"""
}

def load_or_create_config():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    config = ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        # Проверим, что все нужные поля есть
        if ("DEFAULT" not in config or
            not config["DEFAULT"].get("client_id") or
            not config["DEFAULT"].get("client_secret") or
            not config["DEFAULT"].get("user_id")):
            print("Config file is missing required fields. Recreating...")
            os.remove(CONFIG_FILE)
            return load_or_create_config()
        return config
    else:
        print("Welcome to osufetch first run setup!")
        print("To get your OAuth tokens, please visit:")
        print("https://osu.ppy.sh/home/account/edit\n")
        client_id = input("Enter your osu! OAuth Client ID: ").strip()
        client_secret = input("Enter your osu! OAuth Client Secret: ").strip()
        while True:
            user_id = input("Enter your osu! User ID (number): ").strip()
            if user_id.isdigit():
                break
            print("Invalid user ID, it must be a number.")
        config["DEFAULT"] = {
            "client_id": client_id,
            "client_secret": client_secret,
            "user_id": user_id,
        }
        with open(CONFIG_FILE, "w") as f:
            config.write(f)
        print(f"Configuration saved to {CONFIG_FILE}\n")
        return config

def fetch_user_data(api, user_id):
    try:
        user = api.user(user_id)
        return user
    except Exception as e:
        print(f"Error fetching user data: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="osufetch — terminal osu! profile")
    parser.add_argument("id", nargs="?", help="Specify osu! user ID/Name for this run only (does NOT overwrite config)")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args()

    config = load_or_create_config()

    client_id = config["DEFAULT"].get("client_id")
    client_secret = config["DEFAULT"].get("client_secret")

    user_id = args.id if args.id else config["DEFAULT"].get("user_id")

    if not user_id:
        print("Error: osu! user ID is missing or invalid.")
        sys.exit(1)

    if not user_id.isdigit() and not user_id.startswith("@"):
        user_id = f"@{user_id}"
    
    api = Ossapi(client_id, client_secret)
    user = fetch_user_data(api, user_id)

    if not user_id.isdigit():
        user_id = user.id

    playmode = user.playmode
    url = f"https://osuworld.octo.moe/api/users/{user_id}?mode={playmode}"
    with httpx.Client(http2=True) as client:
        response = client.get(url)
        data = response.json()

    def load_regions():
        url = "https://osuworld.octo.moe/locales/en/regions.json"
        try:
            with httpx.Client(http2=True, timeout=10) as client:
                response = client.get(url)
                response.raise_for_status()
                data = response.json()
                # data — это словарь region_id -> region_name
                return data
        except Exception as e:
            print(f"Warning: Failed to fetch regions mapping: {e}")
            return {}

    regions = load_regions()

    region_id = data.get("region_id")

    state = "-"
    if region_id:
        region_id_str = str(region_id)
        country_code = region_id_str.split("-")[0]

        if country_code in regions:
            country_regions = regions[country_code]
            state = country_regions.get(region_id_str, "-")
        else:
            state = regions.get(region_id_str, "-")
    else:
        state = "—"

    grades = user.statistics.grade_counts

    ascii_art = ascii_arts.get(playmode, "(no ascii art)")

    ascii_lines = ascii_art.strip("\n").split("\n")
    info_lines = [
        f"{Fore.CYAN}Username:{Style.RESET_ALL}       {Fore.WHITE}{user.username}{Style.RESET_ALL}",
        f"{Fore.CYAN}Also known as:{Style.RESET_ALL}  {Fore.WHITE}{", ".join(user.previous_usernames) if user.previous_usernames else "-"}{Style.RESET_ALL}",
        f"{Fore.CYAN}Country:{Style.RESET_ALL}        {Fore.WHITE}{f"{user.country.code} | {user.country.name}"}{Style.RESET_ALL}",
        f"{Fore.CYAN}State:{Style.RESET_ALL}          {Fore.WHITE}{state}{Style.RESET_ALL}",
        f"{Fore.CYAN}Playmode:{Style.RESET_ALL}       {Fore.WHITE}{playmode}{Style.RESET_ALL}",
        f"{Fore.CYAN}Team:{Style.RESET_ALL}           {Fore.WHITE}{f"{user.team.short_name} | {user.team.name}" if user.team else "-"}{Style.RESET_ALL}",
        f"{Fore.CYAN}PP:{Style.RESET_ALL}             {Fore.WHITE}{round(user.statistics.pp)}{Style.RESET_ALL}",
        f"{Fore.CYAN}Accuracy:{Style.RESET_ALL}       {Fore.WHITE}{round(user.statistics.hit_accuracy, 2)}%{Style.RESET_ALL}",
        f"{Fore.CYAN}Global Rank:{Style.RESET_ALL}    {Fore.WHITE}#{user.statistics.global_rank}{Style.RESET_ALL}",
        f"{Fore.CYAN}Country Rank:{Style.RESET_ALL}   {Fore.WHITE}#{user.statistics.country_rank}{Style.RESET_ALL}",
        f"{Fore.CYAN}State Rank:{Style.RESET_ALL}     {Fore.WHITE}#{data.get("placement", "-")}{Style.RESET_ALL}",
        f"{Fore.CYAN}Play Count:{Style.RESET_ALL}     {Fore.WHITE}{user.statistics.play_count}{Style.RESET_ALL}",
        f"{Fore.CYAN}Max Combo:{Style.RESET_ALL}      {Fore.WHITE}{user.statistics.maximum_combo}{Style.RESET_ALL}",
        f"{Fore.CYAN}Grades:{Style.RESET_ALL}         {Fore.WHITE}SS: {grades.ss} | SSH: {grades.ssh} | S: {grades.s} | SH: {grades.sh} | A: {grades.a}{Style.RESET_ALL}",
        f"{Fore.CYAN}Supporter:{Style.RESET_ALL}      {Fore.WHITE}{"Yes" if user.is_supporter else "No"}{Style.RESET_ALL}",
        f"{Fore.CYAN}Joined:{Style.RESET_ALL}         {Fore.WHITE}{user.join_date.date()}{Style.RESET_ALL}",
    ]

    # Workaround for 4K/7K mania mode
    if playmode == "mania":
        info_lines[6] = f"{Fore.CYAN}PP:{Style.RESET_ALL}             {Fore.WHITE}{round(user.statistics.pp)} (4K: {round(user.statistics.variants[0].pp)}, 7K: {round(user.statistics.variants[1].pp)}){Style.RESET_ALL}"
        info_lines[8] = f"{Fore.CYAN}Global Rank:{Style.RESET_ALL}    {Fore.WHITE}#{user.statistics.global_rank} (4K: #{user.statistics.variants[0].global_rank}, 7K: #{user.statistics.variants[1].global_rank}){Style.RESET_ALL}"
        info_lines[9] = f"{Fore.CYAN}Country Rank:{Style.RESET_ALL}   {Fore.WHITE}#{user.statistics.country_rank} (4K: #{user.statistics.variants[0].country_rank}, 7K: #{user.statistics.variants[1].country_rank}){Style.RESET_ALL}"

    # Print ASCII art + info side by side
    max_lines = max(len(ascii_lines), len(info_lines))
    for i in range(max_lines):
        art_line = ascii_lines[i] if i < len(ascii_lines) else " " * 40
        info_line = info_lines[i] if i < len(info_lines) else ""
        print(f"{Fore.YELLOW}{art_line:<40}{Style.RESET_ALL}  {info_line}")

    print()

if __name__ == "__main__":
    main()

