import openai
import os
from dotenv import load_dotenv
load_dotenv("secrets.env")
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

openai.api_key = openai_api_key
MODEL_NAME = "o3-mini-2025-01-31"

jarvis_instructions = "YOU ARE A TOP LEVEL LLM AGENT RESPONSIBLE FOR THE FOLLOWING TASK : \
                        - GIVEN A COLLECTION OF IMAGES AND EEG DATA SAMPLES (BRAINWAVE SIGNAL AMPLITUDES) YOU MUST DETECT THE FOLLOWING \
                          1. THE MOMENT THE USER HAS LOST THEIR ATTENTIVENESS AND MOMEMNTS LEADING UP TO IT \
                          2. WHAT IN THE ENVIRONMENT/SURROUNDING HAS CAUSED THE USER TO LOSE THEIR ATTENTIVENESS \
                        \
                        YOU MUST THEN PROVIDE A DETAILED REPORT THAT EXPLAINS WHAT HAPPENED, IF THE USER HAS LOST THEIR ATTENTION IN THE GIVEN PERIOD AND MOST IMPORTANTLY YOU MUST PROVIDE A SUGGESTION ON WHAT THE USER SHOULD DO WITH THEIR ENVIRONMENT OR ELSEWISE IN ORDER TO REGAIN THEIR ATTENTION \
                        YOUR RESPONSE MUST NOT INCLUDE ANY MARKDOWN DECORATIONS SUCH AS '#', '**', etc \
                        YOUR RESPONSE MUST ADHERE TO THE FOLLOWING JSON FORMAT AT ALL TIMES : \
                              user_distracted : ['HAS THE USER GOTTEN DISTRACTED (YES OR NO)'], \
                              distraction_analysis : ['POSSIBLE REASONS FOR DISTRACTION'], \
                              advice_for_user : ['WHAT TO DO TO IMPROVE CURRENT ATTENTION'],"

jarvis_prompt = "HERE IS THE COLLECTED EEG DATA AND ACCOMPANYING IMAGES THAT SHOW THE USERS SURROUNDING WHILE THE EEG DATA HAS BEEN GATHERED \
                 ANALYZE THEM AND DETERMINE WHAT, IF ANYTHING, HAS DISTRACTED THE USER IN THIS TIME FRAME  - REMEMBER TO ADHERE TO YOUR INSTRUCTIONS: "


vision_agent_summary = {
   "name" : "process_images",
   "description": (
       "A multi-layer visual analysis system that processes images from the user's perspective "
       "to understand their work environment, activities, and productivity patterns. "
       "The system consists of several specialized sub-agents that work together to provide "
       "comprehensive analysis and recommendations."
   ),
   "parameters": {
       "type": "object",
       "properties": {
           "image_data": {
               "type": "object",
               "description": (
                   "Real-time image data from user's field of view containing:\n"
                   " - image_path: Path to the image file\n"
                   " - timestamp: When the image was captured\n"
                   " - resolution: Image dimensions\n"
               ),
               "properties": {
                   "perception_layer": {
                       "type": "object",
                       "description": "First layer analysis of visual data",
                       "properties": {
                           "objects": {
                               "type": "array",
                               "description": "Detected objects in view",
                               "items": {
                                   "type": "object",
                                   "properties": {
                                       "type": {"type": "string"},
                                       "confidence": {"type": "number"},
                                       "location": {
                                           "type": "object",
                                           "properties": {
                                               "x": {"type": "number"},
                                               "y": {"type": "number"},
                                               "w": {"type": "number"},
                                               "h": {"type": "number"}
                                           }
                                       },
                                       "relevance": {"type": "number"}
                                   }
                               }
                           },
                           "actions": {
                               "type": "array",
                               "description": "Detected user activities",
                               "items": {
                                   "type": "object",
                                   "properties": {
                                       "type": {"type": "string"},
                                       "confidence": {"type": "number"},
                                       "duration": {"type": "number"},
                                       "intensity": {"type": "number"}
                                   }
                               }
                           }
                       }
                   },
                   "goal_tracking": {
                       "type": "object",
                       "description": "Analysis of progress and goal alignment",
                       "properties": {
                           "goal_alignment": {"type": "number"},
                           "active_goals": {"type": "array", "items": {"type": "string"}},
                           "progress_score": {"type": "number"},
                           "velocity": {"type": "number"},
                           "bottlenecks": {"type": "array", "items": {"type": "string"}}
                       }
                   },
                   "scenario_analysis": {
                       "type": "object",
                       "description": "High-level situation understanding",
                       "properties": {
                           "scenario_type": {"type": "string"},
                           "context": {"type": "string"},
                           "success_score": {"type": "number"},
                           "trajectory": {"type": "string"}
                       }
                   },
                   "recommendations": {
                       "type": "object",
                       "description": "Actionable improvement suggestions",
                       "properties": {
                           "suggestion": {"type": "string"},
                           "priority": {"type": "number"},
                           "expected_impact": {"type": "number"},
                           "implementation_ease": {"type": "number"}
                       }
                   }
               },
               "required": [
                   "image_path",
                   "timestamp",
                   "resolution",
                   "perception_layer",
                   "goal_tracking",
                   "scenario_analysis",
                   "recommendations"
               ]
           }
       },
       "required": ["image_data"]
   }
}
eeg_agent_summary =  {
    "name": "process_eeg_data",
    "description": (
      "The EEG data is passed to an LLM agent that will process and analyze this data"
      "The LLM agent will then respond with a descriptive analysis of the brainwaves in a JSON Format as follows : \
                             alpha_wave_analysis : ['ANALYSIS OF ALPHA WAVES'], \
                              beta_wave_analysis : ['ANALYSIS OF BETA WAVES'], \
                              gamma_wave_analysis : ['ANALYSIS OF GAMMA WAVES'], \
                              delta_wave_analysis : ['ANALYSIS OF GAMMA WAVES'], \
                              attention_analysis : ['ANALYSIS OF ATTENTION VALUES']"

      "This analysis provides insight into the behaviour, trend and patterns in the users brainwaves over a given sampling window"
      "Use this to get a better understanding about what the state of the User's attentiveness and brainwaves"
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
                        "required": [
                            "window_length",
                            "sampling_rate",
                            "alpha_waves",
                            "beta_waves",
                            "gamma_waves",
                            "delta_waves",
                            "theta_waves",
                            "attention_levels"
                        ]
                    }
                },
                "required": ["eeg_data"]
 }}

brain_agent_instructions = "You are an expert in neuroscience and behavioral analysis.\
                            Your Goal is to analyze the EEG data sampled over a window interval. \
                            In your analysis you must describe the behaviour of the users brainwaves \
                            and provide an insightful hypothesis on what state the user is in (ie. focused, relaxed, attentive, losing attention). \
                            You must follow the following output format guidelines at ALL times \
                            1. Your response must not include any markdown decorations such as '#', '**', etc\
                            2. You must provide your response in the following JSON format : \
                            \
                              alpha_wave_analysis : ['YOUR ANALYSIS OF ALPHA WAVES'], \
                              beta_wave_analysis : ['YOUR ANALYSIS OF BETA WAVES'], \
                              gamma_wave_analysis : ['YOUR ANALYSIS OF GAMMA WAVES'], \
                              delta_wave_analysis : ['YOUR ANALYSIS OF GAMMA WAVES'], \
                              attention_analysis : ['YOUR ANALYSIS OF ATTENTION VALUES'],"

brain_agent_prompt = "Here is the EEG data sampled, it contains the values of different brainwave frequencies. \
                    Please tell me what patterns you see and what is the overall trend of my brainwaves"