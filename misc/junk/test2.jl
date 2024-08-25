using Plots

# Parameters
const nx, ny = 50         # Grid size
const dx, dy = 1.0, 1.0   # Grid spacing
const dt = 0.01           # Time step
const alpha = 0.01        # Thermal diffusivity
const nt = 100            # Number of time steps for the animation

# Initialize the temperature grid
T = zeros(nx, ny)        # Temperature grid
T_new = copy(T)          # Grid for updated temperatures

# Initial condition: Heat source in the center
T[nx ÷ 2, ny ÷ 2] = 100.0

# Function to update temperature
function update_temperature!(T, T_new, alpha, dt, dx, dy)
    for i in 2:(nx-1)
        for j in 2:(ny-1)
            T_new[i, j] = T[i, j] + alpha * dt * (
                (T[i+1, j] - 2*T[i, j] + T[i-1, j]) / dx^2 +
                (T[i, j+1] - 2*T[i, j] + T[i, j-1]) / dy^2
            )
        end
    end
end

# Create an animation
anim = @animate for t in 1:nt
    update_temperature!(T, T_new, alpha, dt, dx, dy)
    T, T_new = T_new, T    # Swap references
    heatmap(T, title="2D Heat Distribution at Time Step $t", xlabel="X", ylabel="Y", color=:inferno, clims=(0, 100))
end

# Save the animation
gif(anim, "heat_diffusion.gif", fps=20)
