#!/usr/bin/env ruby

if ARGV.length < 1
  puts "Usage: ruby process_image.rb <input_image>"
  exit 1
end

input_path = ARGV[0]
unless File.exist?(input_path)
  puts "Error: Input file does not exist: #{input_path}"
  exit 1
end

output_dir = '/var/www/app/output'
basename = File.basename(input_path, File.extname(input_path))

puts "Processing image: #{input_path}"

# Check if RMagick is available
begin
  require 'rmagick'
rescue LoadError => e
  puts "Error: rmagick gem is not installed! #{e.message}"
  exit 1
end

# Check if EXIFR is available
begin
  require 'exifr/jpeg'
rescue LoadError => e
  puts "Error: exifr gem is not installed! #{e.message}"
  exit 1
end

begin
  # 1. Generate thumbnail using RMagick
  img = Magick::Image.read(input_path).first
  thumb = img.resize_to_fit(150, 150)
  thumbnail_path = "#{output_dir}/#{basename}_thumbnail.png"
  thumb.write(thumbnail_path)
  puts "Thumbnail created: #{thumbnail_path}"
  puts "Thumbnail dimensions: #{thumb.columns}x#{thumb.rows}"

  # 2. Convert to WebP format
  img2 = Magick::Image.read(input_path).first
  img2.format = 'WEBP'
  webp_path = "#{output_dir}/#{basename}.webp"
  img2.write(webp_path)
  puts "WebP conversion created: #{webp_path}"

  # 3. Extract EXIF data if present (for JPEG files)
  puts "\nEXIF Data:"
  if input_path.downcase.end_with?('.jpg', '.jpeg')
    begin
      exif = EXIFR::JPEG.new(input_path)
      if exif.exif?
        puts "  Make: #{exif.make}" if exif.make
        puts "  Model: #{exif.model}" if exif.model
        puts "  DateTime: #{exif.date_time}" if exif.date_time
        found = [exif.make, exif.model, exif.date_time].compact
        puts "  No standard EXIF metadata found" if found.empty?
      else
        puts "  No EXIF data available"
      end
    rescue => e
      puts "  Could not read EXIF data: #{e.message}"
    end
  else
    puts "  No EXIF data available or unsupported format"
  end

  puts "\nImage processing completed successfully!"
  exit 0

rescue => e
  puts "Error during image processing: #{e.message}"
  exit 1
end
