// create layer selector
/*function createSelector(layer) {
    var $options = $('#layer_selector li');
    var col_name = ""
    $options.click(function(e) {
      // get the area of the selected layer
      var $li = $(e.target);
      col_name = $li.attr('data');
      // deselect all and select the clicked one
      $options.removeClass('selected');
      $li.addClass('selected');
    });
    
}*/
// Create layer selector
function createSelector(layer,num) {
 for (var i = 0; i < layer.getSubLayerCount(); i++) {
  if (i === num) {
    layer.getSubLayer(i).show();
  } else {
    layer.getSubLayer(i).hide();
  }
 }
}
function main() {
cartodb.createVis('map', carto, {
  shareable: false,
  title: false,
  description: true,
  search: true,
  tiles_loader: false,
  center_lat: 38.904722,
  center_lon: -77.016389,
  zoom: 12
})
.done(function(vis, layers) {
  // layer 0 is the base layer, layer 1 is cartodb layer
  //var subLayer = layers[1].getSubLayer(0);
  //createSelector(subLayer);
  var $options = $('#layer_selector li');
  $options.on('click', function(e) {
    var $li = $(e.target)
    var num = +$(e.target).attr('data');
    createSelector(layers[1],num);
    $options.removeClass('selected');
    $li.addClass('selected');
  });
})
.error(function(err) {
  console.log(err);
});
}
window.onload = main;
