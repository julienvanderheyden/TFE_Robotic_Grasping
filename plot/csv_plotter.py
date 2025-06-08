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
    ff_coupled_joints = ["FFJ1", "FFJ2"]
    
    joint_names = all_joints
    
    for joint in joint_names:
        
        cmd_values = df[f"cmd_{joint}"][mask]
        state_values = df[f"state_{joint}"][mask]
        mismatch_values = abs(cmd_values - state_values)

        plt.figure(figsize=(10, 6))
        plt.plot(time_filtered, cmd_values, label=f"Command", linestyle='--')
        plt.plot(time_filtered, state_values, label=f"State", linestyle='-')
        plt.plot(time_filtered, mismatch_values, label=f"Mismatch", linestyle=':', color='red')
        
        plt.xlabel("Time [s]")
        plt.ylabel("Value [rad]")
        #plt.title(f"Command vs State vs Mismatch while moving- {joint}")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        
        plt.savefig(f"{joint}_mw_data.svg")
        
        plt.show()

if __name__ == "__main__":
    csv_filename = "shadowhand_joint_data_medium_wrap.csv"
    plot_mismatch(csv_filename)
