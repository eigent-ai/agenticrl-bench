mutable struct GameState
    point_score::Vector{Int64}
    game_score::Vector{Int64}
    set_score::Vector{Int64}
    server::Int64
    in_tiebreak::Bool
    match_over::Bool
    winner::Int64
    momentum::Vector{Float64}
    fatigue::Vector{Float64}
    serve_accuracy::Vector{Float64}
    return_depth::Vector{Float64}
    first_serve_pct::Vector{Float64}
    break_points::Vector{Int64}
    winners_count::Vector{Int64}
end

function GameState()
    GameState(
        [0, 0],
        [0, 0],
        [0, 0],
        1,
        false,
        false,
        0,
        [0.5, 0.5],
        [0.0, 0.0],
        [0.85, 0.85],
        [0.7, 0.7],
        [0.65, 0.65],
        [0, 0],
        [0, 0]
    )
end

function reset_state!(state::GameState)
    state.point_score .= 0
    state.game_score .= 0
    state.set_score .= 0
    state.server = 1
    state.in_tiebreak = false
    state.match_over = false
    state.winner = 0
    state.momentum .= 0.5
    state.fatigue .= 0.0
    state.serve_accuracy .= 0.85
    state.return_depth .= 0.7
    state.first_serve_pct .= 0.65
    state.break_points .= 0
    state.winners_count .= 0
    return state
end

struct ScoringRules
    games_to_win_set::Int64
    sets_to_win_match::Int64
    tiebreak_min_points::Int64
end

function default_scoring_rules()
    ScoringRules(6, 2, 7)
end

struct SimConfig
    player_skills::Vector{Float64}
    num_matches::Int64
    scoring_rules::Any
    seed::Int64
end
