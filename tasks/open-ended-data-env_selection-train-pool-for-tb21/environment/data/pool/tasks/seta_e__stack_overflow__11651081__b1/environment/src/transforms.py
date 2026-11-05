def create_normalizers(filtered_datasets):
    normalizers = {}
    names = sorted(filtered_datasets.keys())

    for name in names:
        data = filtered_datasets[name]
        min_val = min(data)
        max_val = max(data)

        def normalizer(values):
            normalized = [(v - min_val) / (max_val - min_val) for v in values]
            return {
                'normalized': normalized,
                'range': {'min': min_val, 'max': max_val}
            }

        normalizers[name] = normalizer

    return normalizers
