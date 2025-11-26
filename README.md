# Case-Study-Hydrographic-Survey-Data-Correction-Analysis
## Instruction
This repository contains a complete analysis and correction pipeline for the Spaarnwoude hydrographic cable-tracking case study, designed as part of an ML Engineer internship assessment. 

## Problem Statement
During the Spaarnwoude field trial, cable-tracking data was collected using a cart equipped with dual-antenna GPS and an electromagnetic offset sensor. The processed cable positions (CCOG) are derived from the cart’s position (VCOG) and the algorithm’s offset estimates. However, the GPS antennas were mounted perpendicular to the direction of travel, and an incorrect heading correction was applied (–90° instead of +90°). The correct results can be seen in internal software but cannot be exported, requiring a manual mathematical reconstruction.

## Requirement
1. **Ingest and decipher the data:**  
   The files lack headers, so you must infer the column meanings based on the file content and the provided description.

2. **Diagnose the problem:**  
   Visualize the data to reveal the heading/orientation issue described in the documentation.

3. **Attempt a fix:**  
   Using the information about the heading error, mathematically reconstruct the *true* cable path or correct the heading logic.

4. **Analyze the results:**  
   After applying the correction (or using the raw data), evaluate the consistency and accuracy of the cable tracking. How well does the algorithm perform?

## Setup
This repository consists of three main components:

1. **A Jupyter Notebook (`.ipynb`)** that serves as the primary execution file.  
2. **Several Python modules (`.py` files)** that define reusable functions called by the notebook.  
3. **A shell script** used for automated batch processing.

The project uses **Python 3.12** and requires the following dependencies:

- `numpy`  
- `pandas`  
- `matplotlib`

You can install them with:

```
pip install numpy pandas matplotlib
```

## Ingest and Decipher the Data

The raw VCOG and CCOG files contain no headers, so the first step is to infer the meaning of each column using:

- **Numerical ranges** (e.g., timestamps, ENU coordinates, offsets).
- **Cross-file consistency** (VCOG vs. CCOG structure).
- **Physical constraints** described in the case study:
  - VCOG contains the cart’s world position and the algorithm’s cable offsets.
  - CCOG contains the cable’s world position (cart position + rotated offsets).
  - Some files may include an optional `cable_lock` quality indicator (integer).

By examining value patterns—such as UNIX-like timestamps, smooth increasing survey time, large-scale Easting/Northing coordinates, small-magnitude offsets, and unit-length direction vectors—we can uniquely map each column to its physical meaning.

---

### **Final Identified Column Headers**

#### **VCOG (Vehicle Center of Gravity)**  
1. `unix_time`  
2. `time_s`  
3. `vehicle_easting_m`  
4. `vehicle_northing_m`  
5. `vehicle_height_m`  
6. `vehicle_heading_deg`  
7. `cable_offset_x_m`  
8. `cable_offset_y_m`  
9. `cable_lock`   

#### **CCOG (Cable Center of Gravity / Real-World Cable Position)**  
1. `unix_time`  
2. `time_s`  
3. `cable_easting_m`  
4. `cable_northing_m`  
5. `cable_height_m`  
6. `cable_offset_x_m`  
7. `cable_offset_y_m`  
8. `cable_offset_z_m`  
9. `dir_x`  
10. `dir_y`  
11. `dir_z`  
12. `cable_lock`  

