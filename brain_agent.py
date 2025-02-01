import openai
import json
openai.api_key = "key"
from openai import OpenAI
from typing import List, Dict, Any

brain_agent_instructions = "You are an expert in neuroscience and behavioral analysis."

class EEGAgent:
    """
    The EEG Agent is responsible for processing EEG data.
    It exposes a function 'process_eeg' that the assistant can call
    to analyze the EEG data and return a summary.
    """

    def __init__(self, model_name: str = "gpt-4-0613"):
      self.model_name = model_name
      self.client = OpenAI()
      self.assistant = self.client.beta.assistants.create(
      instructions= brain_agent_instructions,
      model="gpt-4o",
      tools=[
        {
          "type": "function",
          "function": {
            "name": "process_eeg",
            "description": "Get the summary statistics (mean, deviation of alpha, beta, gamma waves and attention levels) for the eeg data you have been provided",
            "parameters": {
              "type": "object",
              "properties": {
                "eeg_data": {
                  "type": "json",
                  "description": ""
                },
              },
              "required": ["eeg_data"]
            }
          }
        }
      ]
    )

    def get_function_schema(self) -> Dict[str, Any]:
      """
      Returns a JSON schema describing the function that the AI assistant can call.
      """
      return {
        "name": "process_eeg",
        "description": "Have an OpenAI Assistant, specialising in EEG brainwave Data analysis, analyze EEG data (focus levels, wave changes) and return a textual summary.",
        "parameters": {
            "type": "object",
            "properties": {
                "eeg_data": {
                    "type": "object",
                    "description": (
                      "Structured EEG information, e.g. {'time_window': ..., 'focus_level': ..., "
                      "'alpha_wave': ..., 'beta_wave': ... }"
                    )
                }
            },
            "required": ["eeg_data"]
        }
      }

    def process_eeg(self, eeg_data: Dict[str, Any]) -> str:
