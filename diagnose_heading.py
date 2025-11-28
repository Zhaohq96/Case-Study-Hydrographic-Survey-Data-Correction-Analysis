import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def wrap_deg(a):
    return (a + 180) % 360 - 180


def diagnose_heading_from_vcog(path_str: str):
    
    df = pd.read_csv(path_str)

    e = df["vehicle_easting_m"].values
    n = df["vehicle_northing_m"].values
    heading = df["vehicle_heading_deg"].values

    dE = np.diff(e)
    dN = np.diff(n)

    track_bearing = np.degrees(np.arctan2(dE, dN))

    heading_used = heading[1:]
    error = wrap_deg(heading_used - track_bearing)

    print(f"Mean heading error: {error.mean():.2f}°")
    #print(f"Std  heading error: {error.std():.2f}°")

    plt.figure(figsize=(6, 4))
    plt.hist(error, bins=60)
    plt.title("Heading Error Distribution (Logged - Track)")
    plt.xlabel("Degrees")
    plt.ylabel("Count")
    plt.grid(True)
    plt.show()

    return error

