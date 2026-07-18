import matplotlib.pyplot as plt
import LightwaveExplorer as lwe
import os
from scipy.ndimage import gaussian_filter1d
from colors import colors

# --- 1. File Configuration ---
script_dir = os.path.dirname(os.path.abspath(__file__))

sub_dir = "Experiment"
energy = "10nJ"

smoothness = 5
waveguide_number = 1
title = f"{energy}, Waveguide #{waveguide_number} (Smoothed, $\sigma$={smoothness})"

waveguide = f"NTT_Group_{waveguide_number}"
filename_1 = waveguide + ".zip"
filename_2 = waveguide + "_Reversed" + ".zip"

color = colors.blue



path_1 = os.path.join(script_dir, "../" + sub_dir + "/Simulations/" + energy, filename_1)
path_2 = os.path.join(script_dir, "../" + sub_dir + "/Simulations/" + energy, filename_2)

# --- 2. Load Data ---
results_1 = lwe.load(path_1, False)
results_2 = lwe.load(path_2, False)

# --- 3. Smoothing Configuration ---
# Apply the filter to the Y-axis data (Spectrum)
y1_smooth = gaussian_filter1d(results_1.spectrumTotal, sigma=smoothness)
y2_smooth = gaussian_filter1d(results_2.spectrumTotal, sigma=smoothness)

# --- 4. Plotting ---

# Plot 1: Blue
plt.plot(results_1.frequencyVectorSpectrum / 1e12, 
         y1_smooth, # Use the smoothed variable
         color=color.base, 
         label='Forward',
         linewidth=1,
         linestyle='-')

# Plot 2: Green
plt.plot(results_2.frequencyVectorSpectrum / 1e12, 
         y2_smooth, # Use the smoothed variable
         color=color.alternative, 
         label='Backward',
         linewidth=1,
         linestyle='--')

# --- 5. Formatting ---
#plt.yscale('log')
plt.xlim(0, 850)

plt.xlabel("Frequency (THz)")
plt.ylabel("Intensity (J/THz)")
plt.title(title)
plt.legend() 
plt.grid(True, which="both", ls="-", alpha=0.3)

plt.gcf().set_size_inches(1800/150, 600/150); plt.savefig(f"{energy}-Waveguide#{waveguide_number}.png", dpi=600)
plt.show()