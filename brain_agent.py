import openai
import json

openai.api_key = "key"

def eeg_agent(eeg_data: dict) -> str:
    """
    Analyze EEG data and return a textual summary.
    
    Parameters:
      eeg_data (dict): Structured data, for example:
        {
          "time_window": "2025-01-01T12:00:00Z to 2025-01-01T12:05:00Z",
          "focus_level": {"average": 65, "min": 40, "max": 80},
          "alpha_wave": {"average": 20, "spikes": ["12:02:15", "12:03:40"]},
          "beta_wave": {"average": 15, "drops": ["12:02:50"]}
        }
    
    Returns:
      A string summary of the EEG analysis.
    """
    messages = [
        {"role": "system", "content": "You are an expert in neuroscience and behavioral analysis."},
        {"role": "user", "content": (
            "Please analyze the following EEG data and provide a detailed summary highlighting "
            "average focus levels, any significant dips or spikes, and any notable patterns in brain waves.\n\n"
            f"EEG Data: {json.dumps(eeg_data, indent=2)}"
        )}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",  # Replace with the model best suited for your needs.
        messages=messages,
        temperature=0.7
    )
    
    summary = response['choices'][0]['message']['content']
    return summary