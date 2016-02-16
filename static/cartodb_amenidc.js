function main() {
cartodb.createVis('map', 
'https://jarnold111.cartodb.com/api/v2/viz/08b0a752-d2a7-11e5-9ca8-0ecd1babdde5/viz.json', {
    shareable: false,
    title: false,
    description: true,
    search: false,
    tiles_loader: false,
    center_lat: 38.904722,
    center_lon: -77.016389,
    zoom: 12
})
.done(function(vis, layers) {
  // layer 0 is the base layer, layer 1 is cartodb layer
  // setInteraction is disabled by default
  layers[1].setInteraction(true);
  layers[1].on('featureOver', function(e, latlng, pos, data) {
    cartodb.log.log(e, latlng, pos, data);
  });
  // you can get the native map to work with it
  var map = vis.getNativeMap();
  // now, perform any operations you need
  // map.setZoom(3);
  // map.panTo([50.5, 30.5]);
})
.error(function(err) {
  console.log(err);
});
}
window.onload = main;

