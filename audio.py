import subprocess

def record_single_audio(filename="audio.wav", duration=3):
    """
    Records a single audio file and saves it to the specified filename.
    
    Parameters:
        filename (str): The name of the file to save the audio. Defaults to 'audio.wav'.
        duration (int): The duration of the recording in seconds. Defaults to 3 seconds.
    """
    
    # Recording audio using arecord
    command = ["arecord", "-D", "plughw:2,0", "-f", "S16_LE", "-r", "16000", "-c", "1", filename, "-d", str(duration)]
    subprocess.run(command)

    print(f"Recording finished. Audio saved as {filename}.")

# Example usage:
if __name__ == "__main__":
    record_single_audio()
