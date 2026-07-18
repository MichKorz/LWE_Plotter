import argparse
import os
import matplotlib.pyplot as plt
import LightwaveExplorer as lwe
import numpy as np
from scipy.ndimage import gaussian_filter1d
from colors import colors

def main():
    parser = argparse.ArgumentParser(description="Plot Lightwave Explorer simulations.")
    
    # Accepts multiple simulation files directly
    parser.add_argument('-i', '--inputs', nargs='+', required=True, help="Simulation files to plot (e.g., sim1.zip sim2.zip)")
    parser.add_argument('-c', '--colors', nargs='+', help="Colors for the plots (e.g., red blue)")
    parser.add_argument('-u', '--unit', choices=['freq', 'wlen'], default='freq', help="Base unit: freq (THz) or wlen (nm)")
    parser.add_argument('-s', '--smoothness', type=float, default=5.0, help="Sigma for Gaussian smoothing")
    parser.add_argument('-o', '--output', type=str, default="plot_output.png", help="Output image filename")

    args = parser.parse_args()

    # Handle color assignment
    color_args = args.colors if args.colors else []
    if len(color_args) < len(args.inputs):
        color_args.extend(['blue'] * (len(args.inputs) - len(color_args)))

    plt.figure(figsize=(12, 4))

    for idx, (sim_file, col_name) in enumerate(zip(args.inputs, color_args)):
        if not os.path.exists(sim_file):
            print(f"Error: File '{sim_file}' not found.")
            continue

        # Load data
        results = lwe.load(sim_file, False)
        y_data = results.spectrumTotal
        
        # Apply smoothing
        if args.smoothness > 0:
            y_data = gaussian_filter1d(y_data, sigma=args.smoothness)
            
        # Retrieve color from Palette
        try:
            color_pair = getattr(colors, col_name)
            plot_color = color_pair.base
        except AttributeError:
            print(f"Warning: Color '{col_name}' not found in Palette. Defaulting to blue.")
            plot_color = colors.blue.base
            
        # Process units
        if args.unit == 'wlen':
            c = 299792458
            freq = results.frequencyVectorSpectrum
            
            # Filter out zero/negative frequencies to avoid division by zero
            valid_idx = freq > 0
            x_data = (c / freq[valid_idx]) * 1e9 # Convert to nm
            y_data = y_data[valid_idx]
            
            xlabel = "Wavelength (nm)"
        else:
            x_data = results.frequencyVectorSpectrum / 1e12 # Convert to THz
            xlabel = "Frequency (THz)"

        # Plot
        plt.plot(x_data, y_data, color=plot_color, label=os.path.basename(sim_file), linewidth=1, linestyle='-')

    # Formatting
    plt.xlabel(xlabel)
    plt.ylabel("Intensity (J/THz)" if args.unit == 'freq' else "Intensity")
    
    if args.unit == 'freq':
        plt.xlim(0, 850)

    plt.title("Simulation Results")
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.3)
    
    plt.tight_layout()
    #plt.savefig(args.output, dpi=600)
    plt.show()

if __name__ == "__main__":
    main()