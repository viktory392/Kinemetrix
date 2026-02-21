################################################################################
# Kinemetrix Project, by Vikraanth Sinha.
# Mocked Leap Motion controller sensor and print to screen, with GUI.
################################################################################

from __future__ import print_function
import sys, time
from getkey import getkey, keys
import numpy as np
import pandas as pd
import datetime as dt
import math
import Tkinter as tk
from Tkinter import *
import ttk

class MockLeap(object):
    def __init__(self, patient_id, patient_age, patient_gender, controller = None, sleep_time = 2):
        self.controller = controller
        self.frame_id = 0
        self.timestamp = 0
        self.handType = "RIGHT"
        self.hand_id = 1
        self.sleep_time = sleep_time
        self.records = []
        self.patient_id = patient_id
        self.patient_age = patient_age
        self.patient_gender = patient_gender
        self.finger_names = ['Thumb', 'Index','Middle','Ring', 'Pinky']

    def get_records(self):
        return self.records

    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        print("Connected")

    def on_disconnect(self, controller):
        print("Disconnected")

    def on_exit(self, controller):
        print("Exited")

    def get_randint(self, minval, maxval):
        return np.random.randint(minval, maxval, (1,))[0]

    def on_frame(self, controller):
        print("Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              self.frame_id, self.timestamp, 1, 5, 0, 0))
        # Get hands
        for hand in [1, 2]:
            print("  %s, id %d, position: %s" % (self.handType, self.hand_id, 0))
            # Get the hand's normal vector and direction
            # Get fingers
            for finger in range(5):
                if self.finger_names[finger] in ['Index','Middle','Ring', 'Pinky']:
                    print("    %s finger, id: %d, length: %fmm, width: %fmm" % (
                    self.finger_names[finger],
                    finger,
                    self.get_randint(5, 12),
                    self.get_randint(1, 2)))

                    # create empty list to store angles
                    angles = []
                    angles.append(self.get_randint(5, 20))
                    angles.append(self.get_randint(5, 20))
                    angles.append(self.get_randint(5, 20))
                    
                    # store all data for this measurement and add to list of measurements
                    current_date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    rec = (self.patient_id, self.patient_age, self.patient_gender, current_date,
                            self.finger_names[finger],
                            angles[0], angles[1], angles[2])
                    self.records.append(rec)
        time.sleep(self.sleep_time)  # Sleep for 2 seconds.

    def state_string(self, state):
        if self.get_randint(0, 4) == 0:
            return "STATE_START"

        if self.get_randint(0, 4) == 1:
            return "STATE_UPDATE"

        if self.get_randint(0, 4) == 2:
            return "STATE_STOP"

        if self.get_randint(0, 4) == 3:
            return "STATE_INVALID"

class StdoutRedirector(object):
    def __init__(self,text_widget):
        self.text_space = text_widget

    def write(self,string):
        self.text_space.insert('end', string)
        self.text_space.see('end')

    def flush(self):
        pass

class CoreGUI(object):
    def __init__(self, parent, listener):
        self.parent = parent
        self.listener = listener
        self.csv_file = None
        self.summary_file = None
        self.patient_id = None
        self.InitUI()
        startbutton = Button(self.parent, text="Start", command=self.custom_main)
        startbutton.grid(column=0, row=1, columnspan=2)
        endbutton = Button(self.parent, text="Stop", command=self.custom_stop)
        endbutton.grid(column=1, row=1, columnspan=2)

    def InitUI(self):
        self.text_box = Text(self.parent, wrap='word', height = 20, width=70)
        self.text_box.grid(column=0, row=0, columnspan = 2, sticky='NSWE', padx=5, pady=5)
        sys.stdout = StdoutRedirector(self.text_box)

    def custom_main(self):
        start_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_id = self.listener.patient_id
        # record data to csv file
        self.csv_file = str(self.patient_id) + "_" + start_time + ".csv"
        print("Data will be recorded to file: %s" % self.csv_file)

        print("Starting measurement. Press Enter to stop.")
        print("Press Enter to stop measuring...")
        key = getkey()
        cnt = 0
        # Keep this process running until Enter is pressed
        while getkey() != keys.ENTER:
            self.listener.on_frame(self.listener.controller)
        print("Measurement complete.")

    def custom_stop(self):
        # Collect all the data.
        column_names = ['Patient ID', 'Age', 'Gender', 'Date', 'Finger', 'Proximal Phalanx Angle',
                        'Intermediate Phalanx Angle', 'Distal Phalanx Angle']
        records = self.listener.get_records()
        df = pd.DataFrame.from_records(records, columns=column_names)
        print("Dataframe:")
        print(df)
        df.to_csv(self.csv_file, index=False)
        print("Data written to %s" % self.csv_file)
        ops = ['min','max']
        summary = df.groupby(['Patient ID', 'Finger']).agg({'Proximal Phalanx Angle': ops,
                            'Intermediate Phalanx Angle': ops, 'Distal Phalanx Angle': ops})
        print('Summary of measurements: ')
        print(summary)
        summary_time = dt.datetime.now().strftime("%Y-%m-%d")
        self.summary_file = str(self.patient_id) + "_" + summary_time + ".csv"
        df.to_csv(self.summary_file, index=False)
        print("Data written to %s" % self.summary_file)
        print('done.')
        # To stop redirecting stdout:
        sys.stdout = sys.__stdout__


def main():

    root = Tk()
    root.title("Kinemetrix")
    root.geometry('600x400')
    root['bg'] = '#ffbf00'
    # Create a mock listener and controller
    listener = MockLeap(patient_id=1, patient_age=392, patient_gender='M', sleep_time=2)
    gui = CoreGUI(root, listener)
    root.mainloop()


if __name__ == "__main__":
    main()

# future enhancements: changing sleep time, averaging last 10 frames
