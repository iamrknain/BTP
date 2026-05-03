import numpy as np
import matplotlib.pyplot as plt
import os

# Ensure the diagrams directory exists
if not os.path.exists('diagrams'):
    os.makedirs('diagrams')

def save_fig(name):
    plt.savefig(f'diagrams/{name}.png', dpi=300, bbox_inches='tight')
    plt.close()

# 1. Grid Transformation (w = z^2)
def plot_grid_transform_z2():
    x = np.linspace(0.1, 2, 10)
    y = np.linspace(0.1, 2, 10)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # z-plane
    for xi in x:
        ax1.plot([xi, xi], [0, 2], 'b', lw=0.5)
    for yi in y:
        ax1.plot([0, 2], [yi, yi], 'r', lw=0.5)
    ax1.set_title('z-plane (Original Grid)')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.grid(True, alpha=0.3)
    
    # w-plane (w = z^2)
    for xi in x:
        z = xi + 1j * np.linspace(0, 2, 100)
        w = z**2
        ax2.plot(w.real, w.imag, 'b', lw=0.5)
    for yi in y:
        z = np.linspace(0, 2, 100) + 1j * yi
        w = z**2
        ax2.plot(w.real, w.imag, 'r', lw=0.5)
    ax2.set_title('w-plane (w = z²)')
    ax2.set_xlabel('u')
    ax2.set_ylabel('v')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    save_fig('grid_transform_z2')

# 2. Electrostatic Potential Lines (Mapping to Half-Plane)
def plot_electrostatic_mapping():
    x = np.linspace(-2, 2, 100)
    y = np.linspace(0.1, 2, 100)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    # Potential in half-plane (simplest case: Phi = v)
    Phi = Y
    
    plt.figure(figsize=(8, 6))
    cp = plt.contour(X, Y, Phi, levels=15, colors='blue', linestyles='dashed')
    plt.clabel(cp, inline=True, fontsize=8)
    
    # Streamlines (E-field lines)
    plt.streamplot(X, Y, np.zeros_like(X), -np.ones_like(Y), color='red')
    
    plt.title('Electrostatic Potential (Blue) and Field Lines (Red) in Half-Plane')
    plt.xlabel('u')
    plt.ylabel('v')
    plt.grid(True, alpha=0.2)
    save_fig('electrostatic_half_plane')

# 3. Fluid Flow around a Cylinder (Mapping Concept)
def plot_fluid_flow_cylinder():
    # Complex potential for flow around a cylinder: F(z) = z + 1/z
    r = np.linspace(1, 3, 50)
    theta = np.linspace(0, 2*np.pi, 100)
    R, THETA = np.meshgrid(r, theta)
    Z = R * np.exp(1j * THETA)
    W = Z + 1/Z
    
    plt.figure(figsize=(8, 8))
    # Plot streamlines (Imaginary part of complex potential)
    plt.contour(Z.real, Z.imag, W.imag, levels=20, colors='blue')
    
    # Plot the cylinder
    circle = plt.Circle((0, 0), 1, color='gray', alpha=0.3)
    plt.gca().add_patch(circle)
    
    plt.title('Fluid Flow Streamlines around a Cylinder (via w = z + 1/z)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axis('equal')
    plt.grid(True, alpha=0.2)
    save_fig('fluid_flow_cylinder')

# 4. SC Step-by-Step Visualization
def plot_sc_step_by_step():
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    # 1. Half-plane
    axes[0].fill_between([-2, 2], 0, 2, color='blue', alpha=0.1)
    axes[0].axhline(0, color='black', lw=2)
    axes[0].set_title('1. Upper Half-Plane (z)')
    axes[0].axis('off')
    
    # 2. Integration / Bending
    t = np.linspace(-2, 2, 100)
    # Simple bend: w = integral (t - (-1))^-0.5 (t - 1)^-0.5 dt
    # This is roughly an arc
    axes[1].plot(np.cos(np.linspace(0, np.pi, 100)), np.sin(np.linspace(0, np.pi, 100)), 'r--', lw=2)
    axes[1].set_title('2. Transformation (Bending)')
    axes[1].axis('off')
    
    # 3. Resulting Polygon
    poly = plt.Polygon([[-1, 0], [1, 0], [1, 1], [-1, 1]], closed=True, color='green', alpha=0.1, ec='green', lw=2)
    axes[2].add_patch(poly)
    axes[2].set_title('3. Final Polygon (w)')
    axes[2].set_xlim(-1.5, 1.5)
    axes[2].set_ylim(-0.5, 1.5)
    axes[2].axis('off')
    
    plt.tight_layout()
    save_fig('sc_process')

if __name__ == "__main__":
    plot_grid_transform_z2()
    plot_electrostatic_mapping()
    plot_fluid_flow_cylinder()
    plot_sc_step_by_step()
    print("Enhanced diagrams generated successfully.")
