// --------------------------------------
// Viz Setup
// --------------------------------------
var margin = {top: 10, right: 140, bottom: 60, left: 90},
    width = 960 - margin.left - margin.right,
    height = 580 - margin.top - margin.bottom;

// Setup scales
// --------------------------------------
var xScale = d3.scale.linear()
    .range([0, width])
    .domain([0, 100000000]);

var yScale = d3.scale.linear()
    .range([height, 0]);

// extent will update based on data
var color = d3.scale.category20c();

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
    .attr("transform", "translate(0," + height + ")");

var yAxisGroup = axesGroup.append("g")
    .attr("class", "y axis");

var lowerElements = svg.append('g').attr({ 'class': 'lowerElements' });
var chart = svg.append('g').attr({ 'class': 'chart' });


// Setup axes
// --------------------------------------
var xAxis = d3.svg.axis()
    .scale(xScale)
    .ticks(5)
    .tickFormat(function(d){
        return d3.format(',')(d);
    })
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(yScale)
    .tickSize(-width)
    .tickFormat(function(d){
        return d3.format(',04d')(d/1000);
    })
    .orient("left");

// Draw labels on axes
yAxisGroup.call(yAxis)
    .append("text")
        .attr({
            "class": "axisLabel",
            "transform": "translate(" + [
                -90, (height - (margin.top + margin.bottom)) / 2
            ] + ") rotate(-90)",
            "y": 6,
            "dy": ".71em"
        })
        .style({
            "text-anchor": "middle"
        })
        .text("Time (seconds)");

xAxisGroup.call(xAxis)
    .append("text")
        .attr({
            "class": "axisLabel",
            "transform": "translate(" + [width / 2, 26] + ")",
            "y": 6,
            "dy": ".71em"
        })
        .style("text-anchor", "begin")
        .text("Num records");

// Draw a line for the 'acceptable' time
// --------------------------------------
// Draw a line representing projected info
var acceptableLine = lowerElements.append('line')
    .attr({
        'class': 'acceptableLine',
        x1: 0,
        x2: width,
        y1: 0,
        y2: 0
    });

var unacceptable = lowerElements.append('rect')
    .attr({
        'class': 'unacceptable',
        x: 0,
        width: width,
        y: 0,
        height: 0
    });


var data;
// --------------------------------------
// Draw chart
// --------------------------------------
d3.csv('data_example_averages.csv', function(d){
    data = d;
    drawChart();
});

var drawChart = function(){
    // Update data
    _.each(data, function(d){
        d.x = +d.records;
        d.y = +d.time;
    });

    // Get data by name
    data = _.groupBy(data, function(d){ return d.name; });
    var flatData = _.flatten(_.values(data));

    // update scales
    xScale.domain(d3.extent(flatData, function(d){ return d.x; }));
    yScale.domain(d3.extent(flatData, function(d) { return d.y; }));
    yScale.domain([0, yScale.domain()[1]]);

    // Update y axis
    yAxisGroup.transition().call(yAxis);
    xAxisGroup.transition().call(xAxis);

    // lines lines
    var line = d3.svg.line()
        .interpolate('basis')
        .x(function(d) { return xScale(d.x); })
        .y(function(d) { return yScale(d.y); });


    // add line
    _.each(data, function(value, key){
        var methodGroup = chart.append('g')
            .attr({
                'class': key.replace(' ', '-').toLowerCase()
            });
        
        methodGroup.append("path")
            .datum(value)
            .attr("class", "line result")
            .attr("d", line)
            .style({ 
                stroke: function(d){ return color(d[0].name); }
            });

        methodGroup.append("text")
            .datum(value)
            .attr({
                x: function(d){ return width + 10; },
                y: function(d){ return yScale(d[0].y) + 3; }
            })
            .text(key);

        methodGroup.selectAll('circle')
            .data(value)
            .enter()
            .append('svg:circle')
                .attr({
                    cx: function(d){ return xScale(d.x); },
                    cy: function(d){ return yScale(d.y); },
                    r: 4
                }).style({
                    fill: function(d){ return color(d.name); }
                });
    });

    //update acceptable line
    acceptableLine.transition().attr({
        y1: yScale( 4000 ),
        y2: yScale( 4000 )
    });
    unacceptable.transition().attr({
        y: 0,
        height: yScale( 4000 )
    });

};
