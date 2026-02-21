# Kinemetrix: Mock Leap Motion Tracker

Kinemetrix is a Python-based diagnostic tool designed to simulate and record hand kinematics. It mimics the data stream of a **Leap Motion Controller**, tracking finger joint angles for medical analysis, physical therapy progress monitoring, and data modeling.

## Project Overview

This implementation provides a **Mock Sensor** environment. This allows developers and researchers to test the data pipeline, GUI, and statistical reporting without requiring the physical Leap Motion hardware. It captures 3D joint angles for the Proximal, Intermediate, and Distal phalanges of each finger.

## Features

* **Real-time Simulation:** Generates randomized, biologically plausible joint angle data.
* **Integrated GUI:** Built with `Tkinter`, featuring a live console output redirection to the window.
* **Automated Reporting:** * **Raw Data:** Saves every frame to a timestamped CSV.
* **Statistical Summary:** Automatically calculates `min` and `max` angles per finger using `pandas`.
* **Legacy Support:** Optimized for Python 2.7 environments required by the Leap Motion hardware.

## Technical Requirements

To run this project, you must have **Python 2.7** installed along with the following libraries:

| Library | Purpose |
| --- | --- |
| `numpy` | Numerical operations and random data generation |
| `pandas` | Data manipulation and CSV export |
| `getkey` | Capturing keyboard interrupts for measurement control |
| `Tkinter` | Standard GUI framework for Python 2.7 |

Install dependencies via pip:

```bash
pip install numpy pandas getkey

```

## How to Use

1. **Launch the App:** Run the script using the Python 2.7 interpreter:
```bash
python kinemetrix.py
```

2. **Initialize:** The GUI will appear. Click **Start** to begin the measurement session.
3. **Monitor Data:** The console within the GUI will display live frame IDs and captured angles.
4. **Stop Measurement:** Press **Enter** to stop the data loop.
5. Click the **Stop** button on the GUI to finalize the data processing and generate the CSV files.
6. **View Results:** Check the project folder for two files:
* `[PatientID]_[Timestamp].csv` (Raw data)
* `[PatientID]_[Date].csv` (Summary report)



## Data Structure

The system records the following metrics for the Index, Middle, Ring, and Pinky fingers:

* **Proximal Phalanx Angle:** Base joint of the finger.
* **Intermediate Phalanx Angle:** Middle knuckle.
* **Distal Phalanx Angle:** Knuckle closest to the fingertip.

---

**Author:** Vikraanth Sinha

**Version:** 1.0.0 (Legacy Support)

---
