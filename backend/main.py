from brain_agent import EEGAgent
import jarvis
import os
from vision import AgentCoordinator
def main():
    # Use absolute path instead of relative
    current_dir = os.path.dirname(os.path.abspath(__file__))
    vision_data_path = os.path.join(current_dir, "data")
    valid_extensions = {".jpg", ".jpeg", ".png"}
    
    image_paths = []
    for filename in os.listdir(vision_data_path):
        # Split out the file extension
        _, ext = os.path.splitext(filename)
        # Check if the extension is one of the valid ones
        if ext.lower() in valid_extensions:
            # Create full path and add it to the list
            full_path = os.path.join(vision_data_path, filename)
            image_paths.append(full_path)

    brain_agent = EEGAgent("o3-mini-2025-01-31")
    vision_agent = AgentCoordinator()
    jarvis_agent = jarvis.TopLevelAgent(vision_agent=vision_agent, eeg_agent=brain_agent)
    eeg_data = {
        "window_length": 10,
        "sampling_rate": 10,
        "alpha_waves": [23, 45, 67, 54, 32, 71, 49, 50, 19, 30],
        "beta_waves": [42, 68, 86, 90, 72, 56, 44, 99, 86, 63],
        "gamma_waves": [150, 200, 198, 220, 180, 210, 240, 255, 230, 190],
        "delta_waves": [5, 3, 10, 7, 25, 22, 15, 8, 2, 14],
        "theta_waves": [10, 20, 35, 40, 25, 45, 30, 38, 12, 27],
        "attention_levels": [70, 72, 68, 90, 55, 60, 85, 92, 100, 77]
    }

    print("Starting EEG Processing \n")
    resp = jarvis_agent.run_analysis(eeg_data, image_paths)
    if resp:
        print("Got Agent Response: ", resp)
    else:
        print("Failed to Get Response", resp)


if __name__ == "__main__":
    main()