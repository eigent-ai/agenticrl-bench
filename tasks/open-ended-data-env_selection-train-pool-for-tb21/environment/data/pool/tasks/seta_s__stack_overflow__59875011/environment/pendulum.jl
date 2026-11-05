using OrdinaryDiffEq

function pendulum!(du, u, p, t)
    g, L = p
    du[1] = u[2]
    du[2] = -(g / L) * sin(u[1])
end

p = [9.81, 1.0]
u0 = (0.3, 0.0)
tspan = (0.0, 10.0)

prob = ODEProblem(pendulum!, u0, tspan, p)
sol  = solve(prob, Tsit5(), reltol=1e-8, abstol=1e-8)

println("Final angle (rad): ", sol.u[end][1])
println("Final angular velocity (rad/s): ", sol.u[end][2])
