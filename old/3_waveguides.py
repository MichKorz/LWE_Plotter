import matplotlib.pyplot as plt
import LightwaveExplorer as lwe
import os
from scipy.ndimage import gaussian_filter1d # Import the smoothing function
from colors import colors

# --- 1. File Configuration ---
script_dir = os.path.dirname(os.path.abspath(__file__))

sub_dir = "Publication"
energy = "25nJ"

postfix = "_Reversed"

smoothness = 5
title = f"{energy}, Increasing poling period (Smoothed, $\sigma$={smoothness})"

filename_1 = "NTT_Group_1" + postfix + ".zip"
filename_2 = "NTT_Group_2" + postfix + ".zip"
filename_3 = "NTT_Group_3" + postfix + ".zip"

path_1 = os.path.join(script_dir, "../" + sub_dir + "/Simulations/" + energy, filename_1)
path_2 = os.path.join(script_dir, "../" + sub_dir + "/Simulations/" + energy, filename_2)
path_3 = os.path.join(script_dir, "../" + sub_dir + "/Simulations/" + energy, filename_3)

# --- 2. Load Data ---
results_1 = lwe.load(path_1, False)
results_2 = lwe.load(path_2, False)
results_3 = lwe.load(path_3, False)

# --- 3. Smoothing Configuration ---
# Sigma controls the smoothness. 
# 2 is subtle, 5 is very smooth, 10 might blur too much.


# Apply the filter to the Y-axis data (Spectrum)
y1_smooth = gaussian_filter1d(results_1.spectrumTotal, sigma=smoothness)
y2_smooth = gaussian_filter1d(results_2.spectrumTotal, sigma=smoothness)
y3_smooth = gaussian_filter1d(results_3.spectrumTotal, sigma=smoothness)

# --- 4. Plotting ---
plt.figure(figsize=(10, 6))

# Plot 1: Blue
plt.plot(results_1.frequencyVectorSpectrum / 1e12, 
         y1_smooth, # Use the smoothed variable
         color=colors.blue.base, 
         label='Waveguide #1',
         linewidth=1,
         linestyle='-')

# Plot 2: Green
plt.plot(results_2.frequencyVectorSpectrum / 1e12, 
         y2_smooth, # Use the smoothed variable
         color=colors.green.base, 
         label='Waveguide #2',
         linewidth=1,
         linestyle='-')

# Plot 3: Red
plt.plot(results_3.frequencyVectorSpectrum / 1e12, 
         y3_smooth, # Use the smoothed variable
         color=colors.red.base, 
         label='Waveguide #3',
         linewidth=1,
         linestyle='-')


# --- 5. Harmonic Markers (Detachable Block) ---
# ========================================================
SHOW_HARMONICS = True
FUNDAMENTAL_THZ = 73  # Base frequency (e.g., 2200nm ~ 136 THz)
MAX_HARMONICS = 11      # How many harmonics to label (H1, H2...)

if SHOW_HARMONICS:
    ax = plt.gca() # Get current axis
    
    # Calculate positions: [1*f, 2*f, 3*f, ...]
    harmonic_positions = [FUNDAMENTAL_THZ * i for i in range(1, MAX_HARMONICS + 1)]
    
    for i, pos in enumerate(harmonic_positions):
        label = f"H{i+1}"
        
        # Check if the marker is within current visible limits to avoid clutter
        if 0 <= pos <= 850: 
            ax.text(
                x=pos, 
                y=0.02,             # 2% up from the bottom axis (Blended Transform)
                s=label, 
                transform=ax.get_xaxis_transform(),
                ha='center', va='bottom',
                fontsize=10, fontweight='bold', color='black',
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1)
            )
            
            # Optional: Add small tick mark
            ax.vlines(pos, 0, 0.015, transform=ax.get_xaxis_transform(), color='black', alpha=0.5, linewidth=1)
# ========================================================


# --- 6. Formatting ---
plt.yscale('log')
plt.xlim(0, 850)

plt.xlabel("Frequency (THz)")
plt.ylabel("Intensity (Log Scale)")
plt.title(title)
plt.legend() 
plt.grid(True, which="both", ls="-", alpha=0.3)

plt.gcf().set_size_inches(1800/150, 600/150); plt.savefig(f"{energy}-AllBackward.png", dpi=600)
plt.show()