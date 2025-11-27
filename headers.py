import pandas as pd
from pathlib import Path

def identify_header_by_physics(df):
    
    n = df.shape[1]

    if n == 10:
        return [
            "unix_time",              
            "time_s",                 
            "vehicle_easting_m",      
            "vehicle_northing_m",     
            "vehicle_height_m",       
            "vehicle_heading_deg",   
            "cable_offset_x_m",       
            "cable_offset_y_m",
            "cable_offset_z_m",       
            "cable_lock",
        ]

    elif n == 12:
        return [
            "unix_time",
            "time_s",
            "cable_easting_m",
            "cable_northing_m",
            "cable_height_m",
            "cable_offset_x_m",
            "cable_offset_y_m",
            "cable_offset_z_m",
            "cable_direction_x",
            "cable_direction_y",
            "cable_direction_z",
            "cable_lock",
        ]

    else:
        raise ValueError(
            f"Unknown file format: expected 10 (VCOG) or 12 (CCOG) columns, got {n}"
        )


def process_file_add_header(path_str: str):
    
    path = Path(path_str)

    df = pd.read_csv(path, header=None)  

    header = identify_header_by_physics(df)
    df.columns = header

    new_path = path.with_name(path.stem + "_identified" + path.suffix)
    df.to_csv(new_path, index=False)

    return new_path

if __name__ == "__main__":
    # Example
    process_file_add_header(r"D:\Intern\Spaarnwoude\Exp_1_VCoG_TOC.csv")
    process_file_add_header(r"D:\Intern\Spaarnwoude\Exp_1_CCoG_TOC.csv")
