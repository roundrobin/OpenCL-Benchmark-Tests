require "date"

records = 4000000
num_calculations = 100

begin
  records = ARGV[0].to_i
rescue
  puts "There is a problem accessing the first command line argument"
end

begin
  num_calculations = ARGV[1].to_i
rescue
  puts "There is a problem accessing the second command line argument"
end


puts "Testing with #{records} records"
puts "Testing with #{num_calculations} calculations"


# Setup dummy data
# ---------------------------------------
speeds = []
start = Time.now
data1 = []
data2 = []

records.times do |index|
  data1 << Random.new.rand * 200000
  data2 << Random.new.rand * 200000
end

speeds << Time.now - start
puts (Time.now - start)

# Run performance tests
# ---------------------------------------
puts '>>> Actual speed tests' 
start = Time.now
records.times do |i|
    num_calculations.times do |j|
        #Do a dummy calculation n times
        dummy = data1[i] * data2[i] + (0.05 * data1[i]) * (1.08 / data2[i]) * (0.02 * (0.0485 * data1[i])) + ((data1[i] / data2[i]) + (0.02 * 0.02 * 0.02 * data1[i])) - (data2[i] / 2)
    end
end

speeds << Time.now - start
finish = speeds[-1]
puts "<<< Done: #{finish}"


mm, ss = finish.divmod(60)
hh, mm = mm.divmod(60)    
dd, hh = hh.divmod(24)    

final_speed_result = "#{hh}:#{mm}:#{ss}"


File.open("../test.csv", 'a') do |file|
    file.write "\nRuby test,#{final_speed_result},#{records},#{num_calculations}"
end



