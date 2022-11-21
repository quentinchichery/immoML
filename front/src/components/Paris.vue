<template>
  <div id="map_Paris" >
    <h1>Real Estate Prices in Paris ...</h1>
    <button @click='changeArrQuart'> Change to Arrondissement / Quartier </button>
  </div>
</template>
 
<script>
import * as d3 from 'd3'
import axios from 'axios';
 
export default {
  name: 'Paris',
  data() {
    return {
      geoname : 'arrondissements.json',
      geojson : {}
    }
  },
  methods: {
    getJsonfromGCP() {
      axios.post("https://europe-west1-ml-immo-paris.cloudfunctions.net/function-1", {geoname: this.geoname})
      .then(response => {
        this.geojson = response.data
        this.createMap()
      });
    },
    createMap() {
      d3.selectAll('svg').remove();
      const width = 550, height = 550;
      const path = d3.geoPath();
      const projection = d3.geoConicConformal()
        .center([2.3522219, 48.856614])
        .scale(170000)
        .translate([width / 2, height / 2]);
      path.projection(projection);

      const svg = d3.select('#map_Paris').append("svg")
        .attr("id", "svg")
        .attr("width", width)
        .attr("height", height);

      const deps = svg.append("g");

      let div = d3.select("body").append("div")   
        .attr("class", "map-tooltip")               
        .style("opacity", 0);

      // d3.json(geofile).then(function(geojson) {
        var min = d3.min(this.geojson.features, function(d) { return d.properties.price_m2; } )
        var max = d3.max(this.geojson.features, function(d) { return d.properties.price_m2; } )
        var colorScale = d3.scaleSequential()
          .interpolator( d3.interpolateOrRd)
          .domain([min,max])

          deps.selectAll("path")
            .data(this.geojson.features)
            .enter()
            .append("path")
            .attr("d", path)
            .style("fill", d => colorScale(d.properties.price_m2))
            
            .on("mouseover", function(event, d) {
            div.transition()        
                      .duration(200)      
                      .style("opacity", .9);
                  div.html("<b>Arrondissement : </b>" + d.properties.code_postal + "<br>"
                          + "<b>Moyenne Prix / m² : </b>" + d.properties.price_m2 + "<br>")
                      .style("left", (event.pageX + 30) + "px")     
                      .style("top", (event.pageY - 30) + "px");
              })
              .on("mouseout", function() {
                      div.style("opacity", 0);
                      div.html("")
                          .style("left", "-500px")
                          .style("top", "-500px");
          });

          var legend = svg.append('g')
          .attr('transform', 'translate(525, 150)')
          .attr('id', 'legend');

          legend.selectAll('.colorbar')
          .data(d3.range(9))
          .enter().append('svg:rect')
              .attr('y', d => 8*20 - (d * 20) + 'px')
              .attr('height', '20px')
              .attr('width', '20px')
              .attr('x', '0px')
              .style("fill", d => colorScale(
                min + d * (max-min)/9
                ))

          var legendScale = d3.scaleLinear()
          .domain([min, max])
          .range([0, 9 * 20]);

          svg.append("g")
          .attr('transform', 'translate(550, 150)')
          .call(d3.axisRight(legendScale).ticks(6));
      // });
    },
  changeArrQuart() {
      if (this.geoname === 'arrondissements.json') {
        this.geoname = 'quartiers.json'
        console.log(this.geoname)
      } else {
        this.geoname = 'arrondissements.json'
        console.log(this.geoname)
      }
    this.getJsonfromGCP()
    console.log('updated')
    }
  },
  mounted() {
    this.getJsonfromGCP()
    }
  }
</script>
 



<style>

#svg {
    display: block;
    margin: auto;
}



.map-tooltip {
    position: absolute;
    opacity:0.8;
    z-index:1000;
    text-align:left;
    border-radius:4px;
    -moz-border-radius:4px;
    -webkit-border-radius:4px;
    padding:8px;
    color:#fff;
    background-color:#000;
    font: 12px sans-serif;
    max-width: 300px;
    height: 60px;
}
</style>
