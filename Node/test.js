// Get user input
var args = process.argv;

// Setup config
// --------------------------------------
var num_records = 100;
num_records = args[2] ? args[2] : num_records;

console.log(num_records);
