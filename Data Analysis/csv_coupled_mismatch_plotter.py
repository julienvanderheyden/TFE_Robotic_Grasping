import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 20  

def plot_mismatch(csv_file, color_mode="same"):

    df = pd.read_csv(csv_file)

    time = df["Timestamp"] - df["Timestamp"].iloc[0]

    t_start = 1.0
    t_end = 7.0
    mask = (time >= t_start) & (time <= t_end)
    time_filtered = time[mask]

    uncoupled_joints = [
        "FFJ3", "FFJ4", "MFJ3", "MFJ4", "RFJ3", "RFJ4",
        "LFJ3", "LFJ4", "LFJ5", "THJ1", "THJ2", "THJ3", "THJ4", "THJ5",
        "WRJ1", "WRJ2"
    ]

    coupled_joint_map = {
        "FFJ0": ["FFJ1", "FFJ2"],
        "MFJ0": ["MFJ1", "MFJ2"],
        "RFJ0": ["RFJ1", "RFJ2"],
        "LFJ0": ["LFJ1", "LFJ2"]
    }

    mismatches = {}

    for joint in uncoupled_joints:
        mismatches[joint] = abs(df[f"cmd_{joint}"] - df[f"state_{joint}"])[mask]

    # Coupled: sum J1 + J2
    for virtual_joint, (j1, j2) in coupled_joint_map.items():
        cmd_j0 = df[f"cmd_{j1}"] + df[f"cmd_{j2}"]
        state_j0 = df[f"state_{j1}"] + df[f"state_{j2}"]
        mismatches[virtual_joint] = abs(cmd_j0 - state_j0)[mask]

    plt.figure(figsize=(12, 7))

    coupled_color = "tab:blue"
    uncoupled_color = "tab:orange"

    for joint, mismatch in mismatches.items():
        if color_mode == "same":
            if joint in coupled_joint_map:
                plt.plot(time_filtered, mismatch, color=coupled_color)
            else:
                plt.plot(time_filtered, mismatch, color=uncoupled_color)
        else: 
            plt.plot(time_filtered, mismatch, label=joint)
            

    if color_mode == "same":
        plt.plot([], [], color=coupled_color, label="coupled")
        plt.plot([], [], color=uncoupled_color, label="uncoupled")


    plt.xlabel("Time [s]")
    plt.ylabel("Mismatch (|cmd - state|) [rad]")
    #plt.title("Mismatch Between Commanded and Actual Joint States")
    plt.legend(loc="best")
    plt.grid()
    plt.tight_layout()
    plt.savefig("coupled_mismatch.svg")
    plt.show()

if __name__ == "__main__":
    csv_filename = "shadowhand_joint_data_medium_wrap.csv"

    plot_mismatch(csv_filename, color_mode="same")
