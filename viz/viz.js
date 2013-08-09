// --------------------------------------
// Viz Setup
// --------------------------------------
var margin = {top: 20, right: 20, bottom: 30, left: 80},
    width = 840 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// Setup scales
// --------------------------------------
var xScale = d3.scale.linear()
    .range([0, width])
    .domain([0, 100000000]);

var yScale = d3.scale.linear()
    .range([height, 0])
    .domain([0, 121807]);

// extent will update based on data
var color = d3.scale.category20c();

// Setup axes
// --------------------------------------
var xAxis = d3.svg.axis()
    .scale(xScale)
    .ticks(5)
    .tickFormat(function(d){
        return d;
    })
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(yScale)
    .tickSize(-width - (margin.left + margin.right))
    .tickFormat(function(d){
        return d3.format(',04d')(d/1000);
    })
    .orient("left");

// Setup SVG
// --------------------------------------
var svg = d3.select('svg')
    .attr({
        width: width + margin.left + margin.right,
        height: height + margin.top + margin.bottom
    })
    .append("g")
        .attr({
            transform: "translate(" + margin.left + "," + margin.top + ")"
        });

// Setup groups
// --------------------------------------
// Draw initial axes
var axesGroup = svg.append('g').attr({ 'class': 'axes' });

var xAxisGroup = axesGroup.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

var yAxisGroup = axesGroup.append("g")
    .attr("class", "y axis");

yAxisGroup.call(yAxis)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("Time (seconds)");

// --------------------------------------
// Data Paths
// --------------------------------------
// Udpate y scale
d3.csv('data_example_averages.csv', function(data){
    var newData = {};

    _.each(data, function(d){
        newData[d.name] = newData[d.name] || [];
        d.x = +d.records;
        d.y = +d.time;
        newData[d.name].push(d);
    });

    // update scales
    xScale.domain(d3.extent(data, function(d) { return d.x; }));
    yScale.domain(d3.extent(data, function(d) { return d.y; }));
    yScale.domain([0, yScale.domain()[1]]);

    // lines lines
    var line = d3.svg.line()
        .x(function(d) { return xScale(d.x); })
        .y(function(d) { return yScale(d.y); });

    // add line
    _.each(newData, function(value, key){
        var methodGroup = svg.append('g')
            .attr({
                'class': key.replace(' ', '-').toLowerCase()
            });
        
        methodGroup.append("path")
            .datum(value)
            .attr("class", "line")
            .attr("d", line);

        methodGroup.selectAll('circle')
            .data(value)
            .enter()
            .append('svg:circle')
                .attr({
                    cx: function(d){ return xScale(d.x); },
                    cy: function(d){ return yScale(d.y); },
                    r: 4
                });
    });

});
