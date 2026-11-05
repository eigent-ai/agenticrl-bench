using OrdinaryDiffEq

function quantum!(du, u, p, t)
    omega, gamma = p
    du[1] = (-1im * omega - gamma) * u[1]
    du[2] = abs(u[1])^2
end

p = [2.0, 0.1]
u0 = [1.0, 0.0]
tspan = (0.0, 5.0)

prob = ODEProblem(quantum!, u0, tspan, p)
sol  = solve(prob, Tsit5(), reltol=1e-8, abstol=1e-8)

println("Amplitude squared |psi|^2 at t=5: ", abs(sol.u[end][1])^2)
println("Integrated probability density: ", real(sol.u[end][2]))
