import librosa
import numpy as np
import matplotlib.pyplot as plt
from librosa import display

def save_audio_spectrogram(input_wav_file="audio.wav", output_image_file="audio_spec.jpg", dpi=500):
    """
    Converts a .wav file to a mel-spectrogram and saves it as a .jpg file.
    
    Parameters:
        input_wav_file (str): The path to the input .wav file. Defaults to 'audio.wav'.
        output_image_file (str): The path to save the output .jpg file. Defaults to 'audio_spec.jpg'.
        dpi (int): Resolution of the output image. Defaults to 500.
    """
    try:
        # Load audio file using librosa
        audio, sr = librosa.load(input_wav_file, sr=16000)  # 16kHz sample rate

        # Create mel-spectrogram
        mel_spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=128)
        mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)

        # Plot the mel-spectrogram
        plt.figure()  # Create a figure
        display.specshow(mel_spectrogram_db, sr=sr, x_axis='time', y_axis='mel')
        
        # Center the image
        plt.axis('off')  # Remove axes for cleaner images
        
        # Save the figure as .jpg
        plt.savefig(output_image_file, bbox_inches='tight', pad_inches=0, dpi=dpi)
        plt.close()
        
        print(f"Spectrogram saved as: {output_image_file}")

    except Exception as e:
        print(f"Error processing file '{input_wav_file}': {e}")

# Example usage
if __name__ == "__main__":
    save_audio_spectrogram()

