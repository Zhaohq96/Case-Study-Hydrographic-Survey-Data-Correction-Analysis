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

