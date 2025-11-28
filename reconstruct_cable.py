import numpy as np
import pandas as pd
from pathlib import Path


def wrap_deg(a):
    return (a + 180) % 360 - 180


def reconstruct_cable(df_v: pd.DataFrame, heading_correction_deg=180.0):
    
    heading_correct = wrap_deg(df_v["vehicle_heading_deg"] + heading_correction_deg)
    psi = np.radians(heading_correct)

    dx = df_v["cable_offset_x_m"].values
    dy = df_v["cable_offset_y_m"].values

    dN = dx * np.cos(psi) - dy * np.sin(psi)
    dE = dx * np.sin(psi) + dy * np.cos(psi)

    df_out = pd.DataFrame({
        "unix_time": df_v["unix_time"],
        "time_s": df_v["time_s"],
        "cable_easting_m": df_v["vehicle_easting_m"] + dE,
        "cable_northing_m": df_v["vehicle_northing_m"] + dN,
        "cable_height_m": df_v["vehicle_height_m"],
        "cable_lock": df_v["cable_lock"]
    })

    return df_out

def process_vcog_to_corrected_ccog(path_vcog_identified: str):
    df_v = pd.read_csv(path_vcog_identified)
    df_corr = reconstruct_cable(df_v, heading_correction_deg=180.0)

    path = Path(path_vcog_identified)
    new_path = path.with_name(path.stem.replace("_VCoG", "_CCoG") + "_corrected.csv")
    df_corr.to_csv(new_path, index=False)

    print(f"[reconstruct] Wrote corrected file: {new_path}")
    return new_path
