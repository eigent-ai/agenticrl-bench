-- Player Skin Registration Module
-- Handles loading and registering custom player models for the server

local PlayerSkins = {}
PlayerSkins.registered = {}
PlayerSkins.default_model = "models/player/group01/male_01.mdl"

-- Resource helper to register downloadable content
local function resource_AddFile(path)
    if not PlayerSkins.registered[path] then
        PlayerSkins.registered[path] = true
    end
end

-- Register a complete player model with all required resources
function PlayerSkins.RegisterModel(name, modelpath, hands)
    if not name or not modelpath then
        print("[PlayerSkins] ERROR: Missing name or model path")
        return false
    end

    local entry = {
        name = name,
        model = modelpath,
        hands = hands or "models/weapons/c_arms_citizen.mdl",
        registered_at = os.time()
    }

    resource_AddFile(modelpath)
    if hands then
        resource_AddFile(hands)
    end

    PlayerSkins.registered[name] = entry
    print("[PlayerSkins] Registered model: " .. name)
    return true
end

-- Initialize default player models
function PlayerSkins.LoadDefaults()
    local defaults = {
        { "Citizen Male", "models/player/group01/male_01.mdl" },
        { "Citizen Female", "models/player/group01/female_01.mdl" },
        { "Combine Soldier", "models/player/combine_soldier.mdl" },
        { "Metrocop", "models/player/police.mdl" },
    }

    for i = 1, #defaults do
        local skin = defaults[i]
        PlayerSkins.RegisterModel(skin[1], skin[2])
    end

    print("[PlayerSkins] Loaded " .. #defaults .. " default models")
end

-- Get a player's assigned model or return the default
function PlayerSkins.GetModel(player_id)
    if PlayerSkins.registered[player_id] then
        return PlayerSkins.registered[player_id].model
    end
    return PlayerSkins.default_model
end

PlayerSkins.LoadDefaults()

return PlayerSkins
end
