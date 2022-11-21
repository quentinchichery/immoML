<template>
  <div id="Departements" >
    <h1>Departements</h1>
  </div>
</template>
 
<script>
import * as d3 from 'd3'
 
export default {
  name: 'Departements',
  mounted() {
const width = 550, height = 550;
const path = d3.geoPath();
const projection = d3.geoConicConformal()
  .center([2.454071, 46.279229])
  .scale(2600)
  .translate([width / 2, height / 2]);
path.projection(projection);

const svg = d3.select('#Departements').append("svg")
  .attr("id", "svg")
  .attr("width", width)
  .attr("height", height);

const deps = svg.append("g");
d3.json('departments.json').then(function(geojson) {
    deps.selectAll("path")
      .data(geojson.features)
      .enter()
      .append("path")
      .attr("d", path);
  });



}
}
</script>
 



<style>
.map-tooltip {
  position: absolute;
  text-align: center;
  z-index: 1000;
  color: black;
  width: 275px;
  height: 37px;
  padding: 2px;
  font: 12px sans-serif;
  background: grey;
  border: 0px;
  border-radius: 8px;
  pointer-events: none;
  }
</style>
