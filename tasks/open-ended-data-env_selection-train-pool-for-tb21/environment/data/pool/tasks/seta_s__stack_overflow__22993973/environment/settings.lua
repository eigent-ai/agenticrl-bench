-- Server Configuration Defaults
-- Central configuration module for game server settings

local Settings = {}

Settings.server = {
    hostname = "My Game Server",
    maxplayers = 32,
    tickrate = 66,
    region = "us-east",
    password = "",
    sv_lan = 0
}

Settings.gameplay = {
    friendly_fire = false,
    respawn_time = 5.0,
    round_time = 300,
    warmup_time = 30,
    max_rounds = 15
}

Settings.logging = {
    enabled = true,
    level = "info",
    file = "/var/log/gameserver/server.log",
    max_size_mb = 50,
    rotate_count = 5
}

-- Apply a table of overrides to a settings category
function Settings.Apply(category, overrides)
    if not Settings[category] then
        print("[Settings] Unknown category: " .. tostring(category))
        return false
    end

    local count = 0
    for key, value in pairs(overrides) do
        if Settings[category][key] ~= nil then
            Settings[category][key] = value
            count = count + 1
        else
            print("[Settings] Unknown key in " .. category .. ": " .. key)
        end
    end

    print("[Settings] Applied " .. count .. " override(s) to " .. category)
    return true
end
end
end

-- Get a flat copy of all settings for serialization
function Settings.Export()
    local flat = {}
    for cat_name, cat_values in pairs(Settings) do
        if type(cat_values) == "table" then
            for k, v in pairs(cat_values) do
                flat[cat_name .. "." .. k] = v
            end
        end
    end
    return flat
end

return Settings
