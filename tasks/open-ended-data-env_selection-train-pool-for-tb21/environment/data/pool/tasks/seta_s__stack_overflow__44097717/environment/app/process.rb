#!/usr/bin/env ruby
require_relative 'lib/data_processor'
require 'json'

x_file   = ARGV[0] || 'data/x_data.json'
y_file   = ARGV[1] || 'data/y_data.json'
out_file = ARGV[2] || 'output/aligned_data.csv'

x_data = JSON.parse(File.read(x_file))
y_data = JSON.parse(File.read(y_file))

timestamps, x_values, y_values = values_for_regression(x_data, y_data)

File.open(out_file, 'w') do |f|
  f.puts "timestamp,x_value,y_value"
  timestamps.each_with_index do |ts, i|
    f.puts "#{ts},#{x_values[i]},#{y_values[i]}"
  end
end

puts "Wrote #{timestamps.length} aligned data points to #{out_file}"
