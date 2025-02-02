MODEL_NAME = "o3-mini-2025-01-31"

jarvis_instructions = "YOU ARE A TOP LEVEL LLM AGENT RESPONSIBLE FOR THE FOLLOWING TASK : \
                        - GIVEN A COLLECTION OF IMAGES AND EEG DATA SAMPLES (BRAINWAVE SIGNAL AMPLITUDES) YOU MUST DETECT THE FOLLOWING \
                          1. THE MOMENT THE USER HAS LOST THEIR ATTENTIVENESS AND MOMEMNTS LEADING UP TO IT \
                          2. WHAT IN THE ENVIRONMENT/SURROUNDING HAS CAUSED THE USER TO LOSE THEIR ATTENTIVENESS \
                        YOU MUST THEN PROVIDE A DETAILED REPORT THAT EXPLAINS WHAT HAPPENED, IF THE USER HAS LOST THEIR ATTENTION IN THE GIVEN PERIOD AND MOST IMPORTANTLY YOU MUST PROVIDE A SUGGESTION ON WHAT THE USER SHOULD DO WITH THEIR ENVIRONMENT OR ELSEWISE IN ORDER TO REGAIN THEIR ATTENTION"

jarvis_prompt = "HERE IS THE COLLECTED EEG DATA AND ACCOMPANYING IMAGES THAT SHOW THE USERS SURROUNDING WHILE THE EEG DATA HAS BEEN GATHERED \
                 ANALYZE THEM AND DETERMINE WHAT, IF ANYTHING, HAS DISTRACTED THE USER IN THIS TIME FRAME : "


vision_agent_summary = {"name" : "process_images"}
eeg_agent_summary =  {
    "name": "process_eeg_data",
    "description": (
      "The EEG data is passed to an LLM agent that will process and analyze this data"
      "The LLM agent will then respond with a descriptive analysis of the brainwaves."
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