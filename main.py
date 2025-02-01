from brain_agent import EEGAgent
def main() :
  agent = EEGAgent("gpt-4o")
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
  resp = agent.process_eeg_data(eeg_data)
  if resp : 
    print("Got Agent Response : ", resp)
  else : 
    print("Failed to Get Response")
  

if __name__ == "__main__" :
  main()
