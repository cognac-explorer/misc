using Plots

# Parameters
Lx, Ly = 10.0, 10.0    # Domain size
Nx, Ny = 100, 100      # Grid points
T = 7.0                # Total time
Nt = 500               # Time steps
dx = Lx / (Nx-1)
dy = Ly / (Ny-1)
dt = T / Nt

# Define wave speeds
c1 = 0.5                # Wave speed in the first region
c2 = 1.0                # Wave speed in the second region

# Create the wave speed matrix
c = ones(Nx, Ny) * c1
c[Int(Ny/2):end, :] .= c2  # Bottom half has different speed

# Courant number matrix
s = (c * dt) ./ dx

# Initialize wave field
u = zeros(Nx, Ny, Nt)
x = LinRange(0, Lx, Nx)
y = LinRange(0, Ly, Ny)

# Initial condition: A pulse at the center
# u[:, :, 1] .= exp.(-100 * ((x .- Lx/2)'.^2 .+ (y .- Ly/2).^2))
# u[:, 1, 1] .= exp.(-100 * ((x .- Lx/2)'.^2 .+ (1 .- Ly/2).^2))

# Initial condition: Impulse on the surface
impulse_location_x = round(Int, Ny*0.9)
impulse_location_y = round(Int, Nx/2)   # Near the top surface

# Apply a small impulse at the selected location
u[impulse_location_x, impulse_location_y, 1] = 1.0

# Time-stepping loop
for n in 2:Nt-1
    for i in 2:Nx-1
        for j in 2:Ny-1
            u[i,j,n+1] = 2u[i,j,n] - u[i,j,n-1] + s[i,j]^2 * (
                u[i+1,j,n] + u[i-1,j,n] + u[i,j+1,n] + u[i,j-1,n] - 4u[i,j,n])
        end
    end
    
    # Reflective boundary conditions
    u[1,:,n+1] .= u[2,:,n+1]
    # u[end,:,n+1] .= u[end-1,:,n+1]
    # u[:,1,n+1] .= u[:,2,n+1]
    # u[:,end,n+1] .= u[:,end-1,n+1]
end

# Plotting the wave propagation
anim = @animate for n in 1:10:Nt
    heatmap(x, y, u[:, :, n], color=:viridis, c=:blues, clim=(-1, 1),
            xlabel="X", ylabel="Y", title="Time = $(round(n*dt, digits=2))")
    # contour!(x, y, c, levels=3, color=:reds, linewidth=2, alpha=0.3)  # Transparent velocity model overlay
end

gif(anim, "wave_propagation_2d.gif", fps=15)
