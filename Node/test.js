var fs = require('fs');

// Get user input
var args = process.argv;

// Setup config
// --------------------------------------
var numRecords = 100000;
numRecords = parseInt(args[2] ? args[2] : numRecords, 10);

var numCalculations = 100;
numCalculations = parseInt(args[3] ? args[3] : numCalculations, 10);

var numIterations = 1;
numIterations = parseInt(args[4] ? args[4] : numIterations, 10);

console.log('Testing with ' + numRecords + ' records, ' + 
    numCalculations + ' calculations, ' + 
    numIterations + ' iterations');

// Run calculations
// --------------------------------------
var d1 = 0;
var d2 = 0;
var d3 = 0;
var j = 0;

console.log('Running calculations on data');
var start = new Date();

for(var i=numRecords; i >= 0; i--){
    d1 = i;
    d2 = i;
    // run calculation n times
    for(j=numCalculations; j >= 0; j--){
        d3 = d1 * d2 + (0.05 * d1) * (1.08 / d2) * (0.02 * (0.0485 * d2)) + ((d1 / d2) + (0.02 * 0.02 * 0.02 * d1)) - (d2 / 2);
    }
}

var finish = (new Date() - start);
console.log('Done in ' + finish + ' ms');

// Write to file
fs.appendFile(__dirname + '../data.csv', 
    'NodeJS,' + finish + ',' + numRecords + ',' + numCalculations + '\n', 
    function (err) { 
        console.log('Wrote to data.csv');
    });
