import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.integrate import quad

# Ensure the diagrams directory exists
if not os.path.exists("diagrams"):
    os.makedirs("diagrams")

def save_fig(name):
    plt.savefig(f"diagrams/{name}.png", dpi=300, bbox_inches="tight")
    plt.close()

# 1. Grid Transformation (w = z^2)
def plot_grid_transform_z2():
    x = np.linspace(0.1, 2, 10)
    y = np.linspace(0.1, 2, 10)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # z-plane
    for xi in x:
        ax1.plot([xi, xi], [0, 2], "b", lw=0.5)
    for yi in y:
        ax1.plot([0, 2], [yi, yi], "r", lw=0.5)
    ax1.set_title("z-plane (Original Grid)")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.grid(True, alpha=0.3)
    
    # w-plane (w = z^2)
    for xi in x:
        z = xi + 1j * np.linspace(0, 2, 100)
        w = z**2
        ax2.plot(w.real, w.imag, "b", lw=0.5)
    for yi in y:
        z = np.linspace(0, 2, 100) + 1j * yi
        w = z**2
        ax2.plot(w.real, w.imag, "r", lw=0.5)
    ax2.set_title("w-plane (w = z²)")
    ax2.set_xlabel("u")
    ax2.set_ylabel("v")
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    save_fig("grid_transform_z2")

# 2. Electrostatic Potential Lines (Mapping to Half-Plane)
def plot_electrostatic_mapping():
    x = np.linspace(-2, 2, 100)
    y = np.linspace(0.1, 2, 100)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    # Potential in half-plane (simplest case: Phi = v)
    Phi = Y
    
    plt.figure(figsize=(8, 6))
    cp = plt.contour(X, Y, Phi, levels=15, colors="blue", linestyles="dashed")
    plt.clabel(cp, inline=True, fontsize=8)
    
    # Streamlines (E-field lines)
    plt.streamplot(X, Y, np.zeros_like(X), -np.ones_like(Y), color="red")
    
    plt.title("Electrostatic Potential (Blue) and Field Lines (Red) in Half-Plane")
    plt.xlabel("u")
    plt.ylabel("v")
    plt.grid(True, alpha=0.2)
    save_fig("electrostatic_half_plane")

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
    plt.contour(Z.real, Z.imag, W.imag, levels=20, colors="blue")
    
    # Plot the cylinder
    circle = plt.Circle((0, 0), 1, color="gray", alpha=0.3)
    plt.gca().add_patch(circle)
    
    plt.title("Fluid Flow Streamlines around a Cylinder (via w = z + 1/z)")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis("equal")
    plt.grid(True, alpha=0.2)
    save_fig("fluid_flow_cylinder")

# 4. SC Step-by-Step Visualization
def plot_sc_step_by_step():
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    # 1. Half-plane
    axes[0].fill_between([-2, 2], 0, 2, color="blue", alpha=0.1)
    axes[0].axhline(0, color="black", lw=2)
    axes[0].set_title("1. Upper Half-Plane (z)")
    axes[0].axis("off")
    
    # 2. Integration / Bending
    t = np.linspace(-2, 2, 100)
    # This is a conceptual representation, not a precise integral plot
    axes[1].plot(np.cos(np.linspace(0, np.pi, 100)), np.sin(np.linspace(0, np.pi, 100)), "r--", lw=2)
    axes[1].set_title("2. Transformation (Bending)")
    axes[1].axis("off")
    
    # 3. Resulting Polygon
    poly = plt.Polygon([[-1, 0], [1, 0], [1, 1], [-1, 1]], closed=True, color="green", alpha=0.1, ec="green", lw=2)
    axes[2].add_patch(poly)
    axes[2].set_title("3. Final Polygon (w)")
    axes[2].set_xlim(-1.5, 1.5)
    axes[2].set_ylim(-0.5, 1.5)
    axes[2].axis("off")
    
    plt.tight_layout()
    save_fig("sc_process")

# New Diagram 1: Bergman Kernel Visualization (Conceptual)
def plot_bergman_kernel_concept():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Original Domain (e.g., a square)
    square = plt.Polygon([[-1, -1], [1, -1], [1, 1], [-1, 1]], closed=True, fc='lightblue', ec='blue', alpha=0.6)
    ax1.add_patch(square)
    ax1.plot(0, 0, 'ro', markersize=8, label='Point a')
    ax1.text(0.1, 0.1, 'D', fontsize=14)
    ax1.set_title('Original Domain D')
    ax1.set_aspect('equal', adjustable='box')
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.axis('off')

    # Mapped Domain (e.g., a disk) and kernel function
    circle = plt.Circle((0, 0), 1, fc='lightgreen', ec='green', alpha=0.6)
    ax2.add_patch(circle)
    ax2.plot(0, 0, 'ro', markersize=8, label='Point f(a)' if ax2.get_legend_handles_labels()[1] else '')
    ax2.text(0.1, 0.1, 'B(0,R)' , fontsize=14)
    
    # Representing the kernel function as a peak at f(a)
    x_surf = np.linspace(-1, 1, 50)
    y_surf = np.linspace(-1, 1, 50)
    X_surf, Y_surf = np.meshgrid(x_surf, y_surf)
    Z_surf = np.exp(-(X_surf**2 + Y_surf**2) * 5) # Simple Gaussian peak for visualization
    ax2.contour(X_surf, Y_surf, Z_surf, levels=5, colors='purple', alpha=0.5)

    ax2.set_title('Mapped Domain and Bergman Kernel (Conceptual)')
    ax2.set_aspect('equal', adjustable='box')
    ax2.set_xlim(-1.5, 1.5)
    ax2.set_ylim(-1.5, 1.5)
    ax2.axis('off')

    plt.tight_layout()
    save_fig('bergman_kernel_concept')

# New Diagram 2: Boundary Length Minimization (Conceptual)
def plot_boundary_minimization_concept():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Original Domain (e.g., an ellipse)
    theta = np.linspace(0, 2*np.pi, 100)
    ax1.plot(2*np.cos(theta), np.sin(theta), 'b-', lw=2, label='Original Boundary')
    ax1.fill(2*np.cos(theta), np.sin(theta), 'lightblue', alpha=0.6)
    ax1.set_title('Original Domain D')
    ax1.set_aspect('equal', adjustable='box')
    ax1.set_xlim(-2.5, 2.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.axis('off')

    # Mapped Domain (e.g., a unit circle) and a non-minimal boundary
    ax2.plot(np.cos(theta), np.sin(theta), 'g-', lw=2, label='Minimal Boundary (Circle)')
    ax2.fill(np.cos(theta), np.sin(theta), 'lightgreen', alpha=0.6)
    
    # Example of a non-minimal boundary (e.g., a distorted circle)
    ax2.plot(1.2*np.cos(theta) + 0.1*np.cos(5*theta), 1.2*np.sin(theta) + 0.1*np.sin(5*theta), 'r--', lw=1, label='Non-Minimal Boundary')

    ax2.set_title('Boundary Minimization (Conceptual)')
    ax2.set_aspect('equal', adjustable='box')
    ax2.set_xlim(-1.5, 1.5)
    ax2.set_ylim(-1.5, 1.5)
    ax2.axis('off')
    ax2.legend()

    plt.tight_layout()
    save_fig('boundary_minimization_concept')

# New Diagram 3: Numerical Integration Path around Singularity (Conceptual)
def plot_integration_path_singularity():
    plt.figure(figsize=(8, 6))
    
    # Real axis
    plt.axhline(0, color='black', lw=1)
    plt.axvline(0, color='black', lw=1)
    
    # Singularity point
    plt.plot(0, 0, 'rx', markersize=10, mew=2, label='Singularity (x_k)')
    
    # Integration path (contour around singularity)
    t = np.linspace(0, 2*np.pi, 100)
    radius = 0.5
    path_x = radius * np.cos(t)
    path_y = radius * np.sin(t)
    plt.plot(path_x, path_y, 'b--', lw=1.5, label='Integration Path')
    plt.arrow(path_x[20], path_y[20], path_x[21]-path_x[20], path_y[21]-path_y[20], head_width=0.05, head_length=0.1, fc='b', ec='b')

    plt.text(0.6, 0.2, '$\Gamma$' , fontsize=14, color='b')
    plt.text(0.1, -0.2, '$x_k$' , fontsize=14, color='r')

    plt.title('Numerical Integration Path around a Singularity')
    plt.xlabel('Real Axis')
    plt.ylabel('Imaginary Axis')
    plt.grid(True, alpha=0.2)
    plt.axis('equal')
    plt.legend()
    save_fig('integration_path_singularity')

# New Diagram 4: Parameter Iteration Flow (Conceptual Flowchart)
def plot_parameter_iteration_flow():
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Define node styles
    box_style = dict(boxstyle='round,pad=0.5', fc='yellow', ec='black', lw=1, alpha=0.8)
    diamond_style = dict(boxstyle='round,pad=0.5', fc='lightcoral', ec='black', lw=1, alpha=0.8)
    arrow_style = dict(arrowstyle='->', lw=1.5)

    # Nodes
    start = ax.text(5, 9, 'Start: Initial Guess for Parameters', ha='center', va='center', bbox=box_style)
    calc_F = ax.text(5, 7.5, 'Calculate F(x) (Discrepancy Vector)', ha='center', va='center', bbox=box_style)
    calc_J = ax.text(5, 6, 'Calculate Jacobian J', ha='center', va='center', bbox=box_style)
    solve_eq = ax.text(5, 4.5, 'Solve J * delta_x = -F(x)' , ha='center', va='center', bbox=box_style)
    update_x = ax.text(5, 3, 'Update Parameters: x_new = x_old + delta_x', ha='center', va='center', bbox=box_style)
    converged = ax.text(5, 1.5, 'Converged?', ha='center', va='center', bbox=diamond_style)
    end = ax.text(5, 0.5, 'End: Optimal Parameters Found', ha='center', va='center', bbox=box_style)

    # Arrows
    ax.annotate('', xy=(5, 8.5), xytext=(5, 9.5), arrowprops=arrow_style)
    ax.annotate('', xy=(5, 8), xytext=(5, 9), arrowprops=arrow_style)
    ax.annotate('', xy=(5, 6.5), xytext=(5, 7.5), arrowprops=arrow_style)
    ax.annotate('', xy=(5, 5), xytext=(5, 6), arrowprops=arrow_style)
    ax.annotate('', xy=(5, 3.5), xytext=(5, 4.5), arrowprops=arrow_style)
    ax.annotate('', xy=(5, 2), xytext=(5, 3), arrowprops=arrow_style)
    
    ax.annotate('No', xy=(6.5, 1.5), xytext=(7.5, 1.5), arrowprops=arrow_style)
    ax.annotate('', xy=(7.5, 1.5), xytext=(7.5, 7.5), arrowprops=arrow_style)
    ax.annotate('', xy=(7.5, 7.5), xytext=(5.5, 7.5), arrowprops=arrow_style)

    ax.annotate('Yes', xy=(5, 1), xytext=(5, 1.5), arrowprops=arrow_style)

    plt.title('Conceptual Flowchart of Parameter Iteration (e.g., Newton\'s Method)')
    save_fig('parameter_iteration_flowchart')


if __name__ == "__main__":
    plot_grid_transform_z2()
    plot_electrostatic_mapping()
    plot_fluid_flow_cylinder()
    plot_sc_step_by_step()
    plot_bergman_kernel_concept()
    plot_boundary_minimization_concept()
    plot_integration_path_singularity()
    plot_parameter_iteration_flow()
    print("All diagrams generated successfully.")
