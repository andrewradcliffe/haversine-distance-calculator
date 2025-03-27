import tkinter
from tkinter import ttk
from pywinstyles.py_win_style import windll
import sv_ttk
import pywinstyles
import sys
from math import sin, cos, sqrt, atan2, radians

def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # Radius of the Earth in kilometers
    return distance * 0.539957  # Convert kilometers to nautical miles

def apply_theme_to_titlebar(root):
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        # Set the title bar color to the background color on Windows 11 for better appearance
        pywinstyles.change_header_color(root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")

        # A hacky way to update the title bar's color on Windows 10 (it doesn't update instantly like on Windows 11)
        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)

def main():
    def process_coordinates():
        if not lat1_var.get() or not lon1_var.get() or not lat2_var.get() or not lon2_var.get():
            result_var.set("Please enter all coordinates")
            return
        if not lat1_var.get().replace(".", "").replace("-", "").isnumeric() or not lon1_var.get().replace(".", "").replace("-", "").isnumeric() or not lat2_var.get().replace(".", "").replace("-", "").isnumeric() or not lon2_var.get().replace(".", "").replace("-", "").isnumeric():
            result_var.set("Please enter valid coordinates")
            return
        result_var.set(f"Result: {haversine_distance(float(lat1_var.get()), float(lon1_var.get()), float(lat2_var.get()), float(lon2_var.get())):.2f} nautical miles")

    try:
        windll.shcore.SetProcessDpiAwareness(1)
    except AttributeError:
        pass

    root = tkinter.Tk()
    root.title("Haversine Distance Calculator")

    root.option_add("*TButton.Font", "Arial 12")
    root.option_add("*TLabel.Font", "Arial 12")
    root.option_add("*TEntry.Font", "Arial 12")

    tt_frame = ttk.Frame(root, padding="10")
    tt_frame.grid(row=0, column=0, sticky=(tkinter.W, tkinter.E, tkinter.N, tkinter.S))

    lat1_var = tkinter.StringVar()
    lon1_var = tkinter.StringVar()
    lat2_var = tkinter.StringVar()
    lon2_var = tkinter.StringVar()
    result_var = tkinter.StringVar(value="Result: ")

    # Labels and Inputs
    ttk.Label(tt_frame, text="Latitude 1:").grid(row=0, column=0, sticky=tkinter.W, padx=5, pady=10)
    ttk.Entry(tt_frame, textvariable=lat1_var).grid(row=0, column=1, padx=5, pady=10)

    ttk.Label(tt_frame, text="Longitude 1:").grid(row=1, column=0, sticky=tkinter.W, padx=5, pady=10)
    ttk.Entry(tt_frame, textvariable=lon1_var).grid(row=1, column=1, padx=5, pady=10)

    ttk.Label(tt_frame, text="Latitude 2:").grid(row=2, column=0, sticky=tkinter.W, padx=5, pady=10)
    ttk.Entry(tt_frame, textvariable=lat2_var).grid(row=2, column=1, padx=5, pady=10)

    ttk.Label(tt_frame, text="Longitude 2:").grid(row=3, column=0, sticky=tkinter.W, padx=5, pady=10)
    ttk.Entry(tt_frame, textvariable=lon2_var).grid(row=3, column=1, padx=5, pady=10)

    # Submit Button
    ttk.Button(tt_frame, text="Submit", command=process_coordinates).grid(row=4, column=0, columnspan=2, pady=10)

    # Result Label
    ttk.Label(tt_frame, textvariable=result_var).grid(row=5, column=0, columnspan=2)

    sv_ttk.set_theme("dark")
    apply_theme_to_titlebar(root)
    root.update_idletasks()
    # width = 
    # height = root.winfo_height()
    # root.minsize(width, height)
    # root.maxsize(width, height)
    # root.resizable(False, False)
    root.mainloop()

if __name__ == "__main__":
    main()
