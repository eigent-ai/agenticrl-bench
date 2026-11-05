using OrdinaryDiffEq

function oscillator!(du, u, t, p)
    gamma  = p[1]
    omega0 = p[2]
    du[1] = u[2]
    du[2] = -2 * gamma * u[2] - omega0^2 * u[1]
end

p = [0.5, 2.0]
u0 = [1.0, 0.0]
tspan = (0.0, 5.0)

prob = ODEProblem(oscillator!, u0, tspan, p)
sol  = solve(prob, Tsit5(), reltol=1e-8, abstol=1e-8)

println("Position at t=5: ", sol.u[end][1])
println("Velocity at t=5: ", sol.u[end][2])
