function result = compute_metric(value, scale, unit)
  computed = value * scale;
  result = sprintf('%.4f %s', computed, unit);
end
