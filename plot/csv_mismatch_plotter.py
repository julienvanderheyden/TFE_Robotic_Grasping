#! /usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 20  

def plot_mismatch(csv_file):

    df = pd.read_csv(csv_file)
    
    time = df["Timestamp"] - df["Timestamp"].iloc[0]  # Normalize time to start at 0
    
    t_start = 1.0
    t_end = 7.0

    mask = (time >= t_start) & (time <= t_end)
    time_filtered = time[mask]

    all_joints = ["WRJ1","WRJ2", "FFJ1", "FFJ2", "FFJ3", "FFJ4", "MFJ1", "MFJ2", "MFJ3", "MFJ4", "RFJ1", "RFJ2", "RFJ3", "RFJ4",
                            "LFJ1", "LFJ2", "LFJ3", "LFJ4", "LFJ5", "THJ1", "THJ2", "THJ3", "THJ4", "THJ5"]
    ff_joints = ["FFJ1", "FFJ2", "FFJ3", "FFJ4"]
    mf_joints = ["MFJ1", "MFJ2", "MFJ3", "MFJ4"]
    rf_joints = ["RFJ1", "RFJ2", "RFJ3", "RFJ4"]
    lf_joints = ["LFJ1", "LFJ2", "LFJ3", "LFJ4", "LFJ5"]
    th_joints = ["THJ1", "THJ2", "THJ3", "THJ4", "THJ5"]
    wr_joints = ["WRJ1", "WRJ2"]
    
    uncoupled_joints = ["WRJ1","WRJ2", "FFJ3", "FFJ4", "MFJ3", "MFJ4", "RFJ3", "RFJ4",
                        "LFJ3", "LFJ4", "LFJ5", "THJ1", "THJ2", "THJ3", "THJ4", "THJ5"]
    
    joint_names = all_joints

    mismatches = {joint: abs(df[f"cmd_{joint}"] - df[f"state_{joint}"])[mask] for joint in joint_names}
    
    plt.figure(figsize=(10, 6))
    for joint, mismatch in mismatches.items():
        plt.plot(time_filtered, mismatch, label=joint)
    
    
    plt.xlabel("Time [s]")
    plt.ylabel("Mismatch (|cmd - state|) [rad]")
    #plt.title("Mismatch Between Commanded and Actual Joint States - hand moving")
    
    # Filter legend to only show WRJ1 and WRJ2
    handles, labels = plt.gca().get_legend_handles_labels()
    filtered = [(h, l) for h, l in zip(handles, labels) if l in ["WRJ1", "WRJ2"]]
    if filtered:
        handles, labels = zip(*filtered)
        plt.legend(handles, labels, loc="best")

    plt.grid()
    plt.tight_layout()
    plt.savefig("overall_mismatch.svg")
    plt.show()

if __name__ == "__main__":
    csv_filename = "shadowhand_joint_data_medium_wrap.csv"
    plot_mismatch(csv_filename)