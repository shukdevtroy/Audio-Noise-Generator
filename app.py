import os
import numpy as np
from pydub import AudioSegment
import tkinter as tk
from tkinter import messagebox, filedialog

def generate_gaussian_noise(duration, sample_rate=44100, std_dev=0.1):
    """Generate Gaussian noise."""
    samples = np.random.normal(0, std_dev, size=(duration * sample_rate,))
    audio_segment = AudioSegment(
        samples.tobytes(),
        frame_rate=sample_rate,
        sample_width=2,  # 16-bit audio
        channels=1
    )
    return audio_segment

def generate_impulse_noise(duration, sample_rate=44100, impulse_rate=0.05):
    """Generate impulse noise."""
    samples = np.zeros(int(duration * sample_rate))
    num_impulses = int(sample_rate * duration * impulse_rate)
    impulse_indices = np.random.randint(0, len(samples), num_impulses)
    samples[impulse_indices] = np.random.uniform(-1, 1, size=num_impulses)
    
    audio_segment = AudioSegment(
        samples.tobytes(),
        frame_rate=sample_rate,
        sample_width=2,  # 16-bit audio
        channels=1
    )
    return audio_segment

def add_noise(audio_file, noise_type='gaussian', noise_level=0.1):
    """Add noise to a clean audio file."""
    audio = AudioSegment.from_file(audio_file)
    duration = len(audio)

    if noise_type == 'gaussian':
        noise = generate_gaussian_noise(duration // 1000)
    elif noise_type == 'impulse':
        noise = generate_impulse_noise(duration // 1000)
    else:
        raise ValueError("Invalid noise type.")

    noise = noise - (20 * np.log10(1 / noise_level))
    noisy_audio = audio.overlay(noise)

    return noisy_audio

def save_noisy_audio(noisy_audio, output_file):
    """Save the noisy audio to a file."""
    noisy_audio.export(output_file, format='wav')

def create_noisy_audio(noise_type):
    """Create a noisy audio file based on the selected noise type."""
    file_paths = audio_file_paths.get().split(';')  # Split the file paths
    if not file_paths[0]:  # Check if any file is selected
        messagebox.showwarning("Warning", "Please select an audio file first.")
        return

    for audio_file in file_paths:
        # Create directory for noisy audio files
        base_name = os.path.splitext(audio_file)[0]
        output_dir = f"{base_name} noise files"
        os.makedirs(output_dir, exist_ok=True)

        output_audio_file = os.path.join(output_dir, f"noisy_audio_{noise_type}_{os.path.basename(audio_file)}")
        noisy_audio = add_noise(audio_file, noise_type=noise_type, noise_level=0.1)
        save_noisy_audio(noisy_audio, output_audio_file)
    
    messagebox.showinfo("Success", "Noisy audio files saved successfully.")

def browse_file():
    """Open a file dialog to select multiple audio files."""    
    filenames = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.wav;*.mp3")])
    if filenames:
        audio_file_paths.set(';'.join(filenames))  # Store paths as a single string separated by semicolons

def create_gui():
    """Create the GUI for the noise generator."""
    global audio_file_paths
    root = tk.Tk()
    root.title("Audio Noise Generator")

    audio_file_paths = tk.StringVar()  # Initialize after root window is created

    tk.Label(root, text="Select Audio Files:").pack(pady=10)
    tk.Entry(root, textvariable=audio_file_paths, width=50).pack(pady=5)
    tk.Button(root, text="Browse", command=browse_file).pack(pady=5)

    tk.Label(root, text="Select Noise Type to Add:").pack(pady=10)

    noise_types = ['gaussian', 'impulse']
    for noise in noise_types:
        button = tk.Button(root, text=noise.capitalize() + " Noise", command=lambda n=noise: create_noisy_audio(n))
        button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
