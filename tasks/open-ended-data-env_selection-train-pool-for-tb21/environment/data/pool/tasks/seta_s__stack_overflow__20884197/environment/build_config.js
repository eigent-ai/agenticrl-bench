const fs = require('fs');
const path = require('path');

const levelsDir = path.join(__dirname, '..', 'levels');
const outputPath = path.join(__dirname, '..', 'game_config.json');

const files = fs.readdirSync(levelsDir).filter(f => f.endsWith('.json'));

function loadManualLevels() {
    const config = {
        boxes: {},
        stars: {},
        player_positions: {},
        victory_conditions: {}
    };

    for (const file of files) {
        const match = file.match(/level(\d+)\//);
        if (!match) continue;
        const levelKey = 'level' + match[1];
        const data = JSON.parse(fs.readFileSync(path.join(levelsDir, file), 'utf8'));

        config.boxes[levelKey] = data.boxes || [];
        config.stars[levelKey] = data.stars || [];
        config.player_positions[levelKey] = data.player_position || null;
        config.victory_conditions[levelKey] = data.victory_condition || null;
    }

    return config;
}

function loadGeneratedLevels() {
    const generatedConfig = { game_data: {} };

    const genFiles = files.filter(f => {
        const m = f.match(/level(\d+)\//);
        return m && parseInt(m[1]) >= 4;
    });

    for (const file of genFiles) {
        const match = file.match(/level(\d+)\//);
        const levelKey = 'level' + match[1];
        const data = JSON.parse(fs.readFileSync(path.join(levelsDir, file), 'utf8'));

        generatedConfig.game_data[levelKey] = {
            boxes: data.boxes || [],
            stars: data.stars || [],
            player_position: data.player_position || null,
            victory_condition: data.victory_condition || null
        };
    }

    return generatedConfig;
}

function mergeLevels(manual, generated) {
    const result = { game_data: {} };
    Object.assign(result.game_data, manual.game_data);
    Object.assign(result.game_data, generated);
    return result;
}

const manualData = loadManualLevels();
const generatedData = loadGeneratedLevels();

const merged = mergeLevels(manualData, generatedData);

fs.writeFileSync(outputPath, JSON.stringify(merged, null, 2));
console.log('Built game_config.json');
