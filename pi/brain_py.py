import ctypes

lib = ctypes.CDLL("./brain.so")
lib.readBrainData.restype = ctypes.c_char_p

class Brain:

    def __init__(self):
        lib.initBrain()

    def read(self):
        string_ptr = lib.readBrainData()
        brain_data = ctypes.string_at(string_ptr).decode("utf-8")
        brain_array = brain_data.split(",")
        brain_array = [int(x) for x in brain_array]

        return  {
                "signal_strength": brain_array[0],
                "attention": brain_array[1],
                "meditation": brain_array[2],
                "delta": brain_array[3],
                "theta": brain_array[4],
                "low_alpha": brain_array[5],
                "high_alpha": brain_array[6],
                "low_beta": brain_array[7],
                "high_beta": brain_array[8],
                "low_gamma": brain_array[9],
                "high_gamma": brain_array[10]
                }

    def __del__(self):
        lib.closeBrain()












