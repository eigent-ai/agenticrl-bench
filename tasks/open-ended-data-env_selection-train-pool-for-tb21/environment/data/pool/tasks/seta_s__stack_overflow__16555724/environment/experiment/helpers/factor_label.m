function label = factor_label(n)
  f = factor(n);
  uf = unique(f);
  parts = '';
  for i = 1:length(uf)
    if i > 1
      parts = [parts ' '];
    end
    parts = [parts num2str(uf(i))];
  end
  label = ['factors: ' parts];
end
