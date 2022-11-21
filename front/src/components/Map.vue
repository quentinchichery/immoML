<template>
  <div>
    <h1>France</h1>
    <svg id="my_dataviz" width="400" height="300"></svg>
  </div>
</template>
 
<script>
import * as d3 from 'd3'
 
export default {
  name: 'France',
  mounted() {
    const svg = d3.select("#my_dataviz"),
        width = +svg.attr("width"),
        height = +svg.attr("height");
    
    // Map and projection
    const projection = d3.geoMercator()
        .center([2, 47])                // GPS of location to zoom on
        .scale(980)                       // This is like the zoom
        .translate([ width/2, height/2 ])
    
    // Load external data and boot
    d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson").then( function(data){
    
        // Filter data
        data.features = data.features.filter(d => {console.log(d.properties.name); return d.properties.name=="France"})
    
        // Draw the map
        svg.append("g")
            .selectAll("path")
            .data(data.features)
            .join("path")
              .attr("fill", "grey")
              .attr("d", d3.geoPath()
                  .projection(projection)
              )
            .style("stroke", "none")
    })
  }
}
</script>
 



<style>

</style>
