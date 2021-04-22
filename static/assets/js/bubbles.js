(function(){
	var width = 700,
		height = 700;

	var svg = d3.select("#chart")
		.append("svg")
		.attr("height", height)
		.attr("width", width)
		.append("g")
		.attr("transform", "translate(0,0)")

	//simulations - collection of forces - how circles interact
	//get them to middle
	//don't collide
	var simulation = d3.forceSimulation()
		.force("x", d3.forceX(width/2).strength(0.05))
		.force("y", d3.forceY(height/2).strength(0.05))
		.force("collide", d3.forceCollide(function (d){
			return radiusScale(d.Radius);
		}))
		

	var radiusScale = d3.scaleSqrt().domain([0,100]).range([30,100])

	d3.queue()
		.defer(d3.csv, "data.csv")
		.await(ready)

	function ready(error, datapoints) {

		var circles = svg.selectAll(".names")
			.data(datapoints)
			.enter().append("circle")
			.attr("class", "names")
			.attr("r", function(d){
				return radiusScale(d.Radius);
			}) 
			.attr("fill",function(d){
				return d.Color;
			})

		var texts = svg.selectAll(null)
		    .data(datapoints)
		    .enter()
		    .append('text')
		    .attr("text-anchor", "middle")
		    .text(d => d.Field)
		    .attr('fill', 'black')
		    .attr('font-size', 12)

		simulation.nodes(datapoints)
			.on('tick', ticked)
		function ticked() {
			circles
				.attr("cx", function(d){
					return d.x
				})
				.attr("cy", function(d) {
					return d.y
				})
			texts
				.attr("y", function(d){
					return d.y
				})
				.attr("x", function(d){
					return d.x
				})

		}
	}

})();
