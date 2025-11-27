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

#### **CCOG (Cable Center of Gravity)**  
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

The file 'headers.py' is to add header information to the raw files. The file with added header will be named with suffix '_identified'.

## Diagnose heading issue

To diagnose the GPS orientation issue, two independent estimates of the cart’s heading are compared:

1. **GPS-reported heading** (`vehicle_heading_deg`)  
2. **Track-derived heading**, computed from consecutive cart positions  
   (`vehicle_easting_m`, `vehicle_northing_m`)

The file 'diagnose_heading.py' is to diagnose and visualize the heading issue. Firstly, the cart’s actual direction of travel was computed and compared against the recorded GPS heading. The heading difference was then normalized into the \((-180^\circ,\;180^\circ]\) range. The wrapped heading error was visualized, and its mean value was calculated (as shown in the figure below).

<img width="541" height="407" alt="image" src="https://github.com/user-attachments/assets/13306902-5125-4397-b435-8545980b7e78" />


## Reconstruct the true path
Based on the description in the internal email, the intended +90° correction was mistakenly applied as –90°. Therefore, a +180° adjustment was applied to the heading values in the VCOG file, and the cable’s true position was recomputed from the corrected heading and the EM offsets. The cart trajectory, the original cable path, and the corrected cable path were then visualized for comparison (as shown in the figure below).

<img width="708" height="692" alt="image" src="https://github.com/user-attachments/assets/b0e79b39-6098-4782-9a6b-f8eda60fc80e" />

## Results analysis and visualization
After reconstructing the corrected cable path, the results were further analyzed to evaluate the performance of the cable-tracking algorithm.

### Mean difference between raw and corrected cable position
The mean difference between the raw and corrected cable positions is used to quantify the impact of the heading issue on the reconstructed path. The figure below (using Experiment 1 as an example) visualizes the distribution of distance errors between the original and corrected cable trajectories.

<img width="546" height="406" alt="image" src="https://github.com/user-attachments/assets/a79ab592-3cfd-47c8-bdaa-ebe6b9420333" />

### Error vector field
The error vector field provides a spatial visualization of how the cable reconstruction deviates between the raw and corrected results. Each vector represents both the magnitude and direction of the positional error at a given point along the trajectory. This allows the observation of systematic directional biases introduced by the heading issue and how they are resolved after applying the correction (using Experiment 1 as an example).

<img width="696" height="666" alt="image" src="https://github.com/user-attachments/assets/1555e0e9-1687-45a3-8d14-a1a5d5027ca5" />

### Error heatmap
The error heatmap illustrates how the positional error between the raw and corrected cable paths varies across space. By mapping error magnitude to color intensity, the heatmap highlights regions where the heading issue caused larger deviations and areas where the reconstruction remained relatively stable. This provides an intuitive spatial overview of error concentration along the survey line.

<img width="682" height="564" alt="image" src="https://github.com/user-attachments/assets/98717b7c-d1b9-4fb8-b5ae-073f19acad5d" />

### Offset-to-Error mapping
The offset-to-error mapping examines how the positional error varies as a function of the EM offset magnitude. By plotting the world-coordinate reconstruction error against the lateral offset distance, this analysis reveals how sensor performance changes with increasing separation from the cable. A near-linear trend indicates that larger offsets produce proportionally larger reconstruction errors, consistent with expected EM signal attenuation.

<img width="432" height="1127" alt="image" src="https://github.com/user-attachments/assets/9560c3b3-b76b-4f80-a2ba-d33ed269662b" />


