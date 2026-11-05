function createNormalizers(filteredDatasets) {
    var normalizers = {};
    var names = Object.keys(filteredDatasets).sort();

    for (var i = 0; i < names.length; i++) {
        var name = names[i];
        var data = filteredDatasets[name];
        var min = Math.min.apply(null, data);
        var max = Math.max.apply(null, data);

        normalizers[name] = function(values) {
            return {
                normalized: values.map(function(v) { return (v - min) / (max - min); }),
                range: { min: min, max: max }
            };
        };
    }

    return normalizers;
}

module.exports = { createNormalizers };
