module TennisSim

using Random

include("types.jl")
include("scoring.jl")
include("simulation.jl")

export GameState, ScoringRules, SimConfig
export default_scoring_rules, reset_state!
export run_simulation, simulate_point, update_score!
export load_player_data, make_rules_dict

end
