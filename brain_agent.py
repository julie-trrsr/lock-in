import json
import math
from typing import List, Dict, Any
from openai import OpenAI
import time
from system_prompt import *

class EEGAgent:
    """
    The EEG Agent is responsible for processing EEG data.
    It exposes a function 'process_eeg_data' that the assistant can call
    to analyze the EEG data and return a summary.
    """

    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name

        # Prepare the function schema (tool) we'll allow the assistant to call
        self.eeg_tool = self.get_function_schema()

        # Summaries stored for references (if needed)
        self.analyse_eeg_prompt = brain_agent_prompt
        self.instructions = brain_agent_instructions

        # Initialize the OpenAI client
        self.client = OpenAI()

        # Create the assistant with instructions and "function-calling" capability
        self.assistant = self.client.beta.assistants.create(
            name="EEG Data Analyst",
            instructions=self.instructions,
            tools=[{"type": "function", "function": self.eeg_tool}], 
            model=self.model_name
        )

        # Create a fresh conversation thread
        self.thread = self.client.beta.threads.create()

    def set_default_prompt(self, prompt):
       self.analyse_eeg_prompt = prompt

    def process_eeg_data(self, eeg_data: Dict[str, Any]) -> str:
      """
      This method sends the EEG data to the assistant for analysis,
      handles any function calls requested by the assistant (e.g., 'get_eeg_summary'),
      and returns the final textual response from the assistant.
      """

      # 1. Create a "user" message in the conversation, providing a prompt plus the data.
      user_message_content = (
        f"{self.analyse_eeg_prompt}\n\n"
        f"Here is the EEG data in JSON format:\n{json.dumps(eeg_data)}\n\n"
        "Please analyze the data and provide your insights."
      )

      self.client.beta.threads.messages.create(
        thread_id=self.thread.id,
        role="user",
        content=user_message_content
      )

      # 2. Create a run to let the assistant process the conversation
      run = self.client.beta.threads.runs.create_and_poll(
        thread_id=self.thread.id,
        assistant_id=self.assistant.id,
        tool_choice = "required",
        tools = [{"type" : "function", "function" :  self.eeg_tool}]
      )

      # 3. We now step through the run until we reach a "final" response.
      response = None
      while True:

        if run.status == "requires_action":
          tool = run.required_action.submit_tool_outputs.tool_calls[0]
          tool_output = None
          
          # We check which function is being called. In this example, we have only "get_eeg_summary".
          if tool.function.name == "get_eeg_summary":
            # Execute the local Python function
            summary_result = self.get_eeg_summary(eeg_data)

            # Convert result to JSON
            summary_json = json.dumps(summary_result)
            tool_output = [{"tool_call_id" : tool.id, "output" : summary_json}]


          else:
            # If there's an unknown function name, handle appropriately
            error_msg = {"error": f"Unknown function '{tool.function.name}'."}
            self.client.beta.threads.messages.create(
              thread_id=self.thread.id,
              role="function",
              name=tool.function.name,
              content=json.dumps(error_msg)
            )

          if tool_output :
            run = self.client.beta.threads.runs.submit_tool_outputs_and_poll(
              thread_id=self.thread.id,
              run_id=run.id,
              tool_outputs=tool_output
            )


        elif run.status == "completed":

          response_id = self.client.beta.threads.messages.list(
            thread_id=self.thread.id
          ).first_id

          response = self.client.beta.threads.messages.retrieve(
             thread_id=self.thread.id,
             message_id=response_id
          ).content[0].text.value

          break


        elif run.status == "failed":
          print(run.status)
          print(f"[-] ERROR : {run.last_error} ")
          pass


        else :
          print(run.status)
          time.sleep(2)
          pass


        time.sleep(1)


      return response



    def get_eeg_summary(self, eeg_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate various summary statistics of the different EEG inputs
        (e.g., alpha_waves, beta_waves, gamma_waves, delta_waves, theta_waves,
        attention_levels) contained in 'eeg_data'.
        
        Returns a dictionary with statistics for each wave band and attention levels,
        along with sampling rate, window length, and other relevant info.
        """

        def compute_stats(values: List[float]) -> Dict[str, float]:
            if not values:
                return {
                    "mean": 0.0,
                    "min": 0.0,
                    "max": 0.0,
                    "std_dev": 0.0
                }
            mean_val = sum(values) / len(values)
            min_val = min(values)
            max_val = max(values)
            # Compute (sample) standard deviation
            variance = (
                sum((x - mean_val) ** 2 for x in values) / (len(values) - 1)
                if len(values) > 1
                else 0.0
            )
            std_dev = math.sqrt(variance)
            return {
                "mean": round(mean_val, 4),
                "min": round(min_val, 4),
                "max": round(max_val, 4),
                "std_dev": round(std_dev, 4)
            }

        # Extract top-level info
        window_length = eeg_data.get("window_length", 0)
        sampling_rate = eeg_data.get("sampling_rate", 0.0)

        alpha_waves = eeg_data.get("alpha_waves", [])
        beta_waves = eeg_data.get("beta_waves", [])
        gamma_waves = eeg_data.get("gamma_waves", [])
        delta_waves = eeg_data.get("delta_waves", [])
        theta_waves = eeg_data.get("theta_waves", [])
        attention_levels = eeg_data.get("attention_levels", [])

        # Compute stats for each wave band and attention
        alpha_stats = compute_stats(alpha_waves)
        beta_stats = compute_stats(beta_waves)
        gamma_stats = compute_stats(gamma_waves)
        delta_stats = compute_stats(delta_waves)
        theta_stats = compute_stats(theta_waves)
        attention_stats = compute_stats(attention_levels)

        # Build final summary
        summary = {
            "window_length": window_length,
            "sampling_rate": sampling_rate,
            "alpha_wave_stats": alpha_stats,
            "beta_wave_stats": beta_stats,
            "gamma_wave_stats": gamma_stats,
            "delta_wave_stats": delta_stats,
            "theta_wave_stats": theta_stats,
            "attention_level_stats": attention_stats
        }

        # Example derived insight: identify the dominant wave band
        wave_averages = {
            "alpha": alpha_stats["mean"],
            "beta": beta_stats["mean"],
            "gamma": gamma_stats["mean"],
            "delta": delta_stats["mean"],
            "theta": theta_stats["mean"]
        }
        dominant_wave = max(wave_averages, key=lambda k: wave_averages[k])
        summary["dominant_wave_band"] = dominant_wave

        return summary

    def get_function_schema(self) -> Dict[str, Any]:
        """
        Returns a JSON schema describing the function that the AI assistant can call
        to provide a thorough summary of EEG data.
        """
        return {
            "name": "get_eeg_summary",
            "description": (
                "Provides summary statistics and analysis of EEG brainwave data "
                "over a given window. Includes multiple wave bands, attention levels, "
                "sampling rate, and any noteworthy events."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "eeg_data": {
                        "type": "object",
                        "description": (
                            "Structured EEG information containing:\n"
                            " - window_length: Number of samples gathered.\n"
                            " - sampling_rate: The sampling rate in Hz.\n"
                            " - alpha_waves: Array of numeric alpha wave amplitudes.\n"
                            " - beta_waves: Array of numeric beta wave amplitudes.\n"
                            " - gamma_waves: Array of numeric gamma wave amplitudes.\n"
                            " - delta_waves: Array of numeric delta wave amplitudes.\n"
                            " - theta_waves: Array of numeric theta wave amplitudes.\n"
                            " - attention_levels: Array of numeric values for attention level.\n"
                        ),
                        "properties": {
                            "window_length": {
                                "type": "number",
                                "description": "Number of samples in the window."
                            },
                            "sampling_rate": {
                                "type": "number",
                                "description": "Sampling rate of the EEG Sensor in Hz."
                            },
                            "alpha_waves": {
                                "type": "array",
                                "description": "Array of numeric alpha wave amplitudes.",
                                "items": {"type": "number"}
                            },
                            "beta_waves": {
                                "type": "array",
                                "description": "Array of numeric beta wave amplitudes.",
                                "items": {"type": "number"}
                            },
                            "gamma_waves": {
                                "type": "array",
                                "description": "Array of numeric gamma wave amplitudes.",
                                "items": {"type": "number"}
                            },
                            "delta_waves": {
                                "type": "array",
                                "description": "Array of numeric delta wave amplitudes.",
                                "items": {"type": "number"}
                            },
                            "theta_waves": {
                                "type": "array",
                                "description": "Array of numeric theta wave amplitudes.",
                                "items": {"type": "number"}
                            },
                            "attention_levels": {
                                "type": "array",
                                "description": (
                                    "Array of numeric values indicating the user's "
                                    "attention/focus level at each sample."
                                ),
                                "items": {"type": "number"}
                            },
                        },
                        "additionalProperties":False,
                        "required": [
                            "window_length",
                            "sampling_rate",
                            "alpha_waves",
                            "beta_waves",
                            "gamma_waves",
                            "delta_waves",
                            "theta_waves",
                            "attention_levels"
                        ],
                    },
                },
              "additionalProperties" : False,
              "required": ["eeg_data"],
            },
            "strict" : True,
        }
