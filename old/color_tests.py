import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import colorsys
import numpy as np

def get_variant_color(color_name, mode='muted', factor=0.6):
    """
    Generates a readable partner color.
    
    Args:
        color_name (str): Input color (e.g., "red", "blue")
        mode (str): 
            'muted'  -> Lowers saturation (Greys it out). Best for distinct but related lines.
            'darker' -> Lowers lightness. Good for high contrast.
            'pastel' -> (Your previous request) Increases lightness.
        factor (float): Strength of the effect (0 to 1).
    """
    rgb = mcolors.to_rgb(color_name)
    h, l, s = colorsys.rgb_to_hls(*rgb)
    
    if mode == 'muted':
        # Reduce saturation, keep lightness the same
        new_s = s * (1 - factor) 
        new_l = l
    elif mode == 'darker':
        # Reduce lightness significantly
        new_l = l * (1 - factor)
        new_s = s
    elif mode == 'pastel':
        # Increase lightness
        new_l = l + (1 - l) * factor
        new_s = s * 0.5 # Optional: also desaturate slightly
        
    new_rgb = colorsys.hls_to_rgb(h, new_l, new_s)
    return mcolors.to_hex(new_rgb)

# ==========================================
# DEMO: Compare the strategies
# ==========================================
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.sin(x) + 0.5

base_color = "dodgerblue" # A nice standard blue

# Generate variants
muted_color = get_variant_color(base_color, mode='muted', factor=0.6)
darker_color = get_variant_color(base_color, mode='darker', factor=0.4)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4))

# Strategy 1: Vibrant vs Muted (Recommended for Color)
ax1.set_title("Strategy 1: Vibrant vs Muted")
ax1.plot(x, y1, color=base_color, linewidth=1, label="Forward (Base)")
ax1.plot(x, y2, color=muted_color, linewidth=1, label="Backward (Muted)")
ax1.legend()
ax1.grid(True, alpha=0.3)

# Strategy 2: Base vs Darker
ax2.set_title("Strategy 2: Base vs Darker")
ax2.plot(x, y1, color=base_color, linewidth=1, label="Forward (Base)")
ax2.plot(x, y2, color=darker_color, linewidth=1, linestyle='--', label="Backward (Darker)")
ax2.legend()
ax2.grid(True, alpha=0.3)

# Strategy 3: Solid vs Dashed (Standard)
ax3.set_title("Strategy 3: Line Style (Best Grouping)")
ax3.plot(x, y1, color=base_color, linewidth=1, linestyle='-', label="Forward")
ax3.plot(x, y2, color=base_color, linewidth=1, linestyle='--', label="Backward")
ax3.legend()
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()