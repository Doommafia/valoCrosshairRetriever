import os
import json
import tkinter as tk
from tkinter import filedialog

def beautify_json(json_data):
    return json.dumps(json_data, indent=4)

def convert_json_to_crosshair_code(json_data):
    primary_crosshair = json_data["primary"]
    ads_crosshair = json_data["aDS"]
    sniper_scope = json_data["sniper"]

    primary_code = f"0;P;c;8;u;{primary_crosshair['color']['r']},{primary_crosshair['color']['g']},{primary_crosshair['color']['b']},{primary_crosshair['color']['a']};b;{int(primary_crosshair['bUseCustomColor'])};t;{primary_crosshair['outlineThickness']};o;{primary_crosshair['outlineOpacity']};d;{int(primary_crosshair['bDisplayCenterDot'])};z;{primary_crosshair['centerDotSize']};a;{primary_crosshair['centerDotOpacity']};h;{int(primary_crosshair['bHasOutline'])};"
    ads_code = f"1;P;c;8;u;{ads_crosshair['color']['r']},{ads_crosshair['color']['g']},{ads_crosshair['color']['b']},{ads_crosshair['color']['a']};b;{int(ads_crosshair['bUseCustomColor'])};t;{ads_crosshair['outlineThickness']};o;{ads_crosshair['outlineOpacity']};d;{int(ads_crosshair['bDisplayCenterDot'])};z;{ads_crosshair['centerDotSize']};a;{ads_crosshair['centerDotOpacity']};h;{int(ads_crosshair['bHasOutline'])};"
    sniper_code = f"S;c;8;t;{sniper_scope['centerDotColor']['r']},{sniper_scope['centerDotColor']['g']},{sniper_scope['centerDotColor']['b']},{sniper_scope['centerDotColor']['a']};b;{int(sniper_scope['bUseCustomCenterDotColor'])};s;{sniper_scope['centerDotSize']};o;{sniper_scope['centerDotOpacity']};"

    return primary_code + ads_code + sniper_code

def write_to_files(json_data, beautified_output_file, codes_output_file):
    # Beautify JSON and write to file
    with open(beautified_output_file, "w") as f:
        f.write(beautify_json(json_data))

    # Extract crosshair codes and write to file
    with open(codes_output_file, "w") as f:
        f.write(convert_json_to_crosshair_code(json_data))

def parse_ini_to_json():
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window

    # Prompt the user to select the input .ini file
    input_file = filedialog.askopenfilename(title="Select Input .ini File", filetypes=[("INI files", "*.ini")])
    
    # Check if the user canceled file selection
    if not input_file:
        print("File selection canceled.")
        return

    # Set the output file names
    output_json_file = os.path.join(os.getcwd(), 'output.json')
    output_codes_file = os.path.join(os.getcwd(), 'codes.txt')

    # Initialize dictionaries to store the JSON data and crosshair codes
    json_data = {}

    with open(input_file, 'r') as f:
        for line in f:
            if line.startswith('EAresStringSettingName::SavedCrosshairProfileData'):
                # Extract the JSON string from the line
                json_str = line.split('=')[1].strip()

                # Remove backslashes from JSON string
                json_str = json_str.replace('\\', '')

                # Convert the JSON string to a dictionary
                json_data = json.loads(json_str)
                break

    # Check if JSON data was found
    if json_data:
        # Write beautified JSON and crosshair codes to files
        write_to_files(json_data, output_json_file, output_codes_file)
        print("Output JSON written to", output_json_file)
        print("Crosshair codes written to", output_codes_file)
    else:
        print("No JSON data found in the .ini file.")

if __name__ == "__main__":
    parse_ini_to_json()
