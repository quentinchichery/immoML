<template>
  <div id="map">
    <Paris />
    <img src="scatterArrondissements.jpg" width="900">
  </div>
</template>

<script>
import Paris from './components/Paris.vue'

export default {
  name: 'App',
  methods: {
    
  },
  components: {
    Paris
  }
}
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
