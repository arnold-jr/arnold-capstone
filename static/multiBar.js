$(function() {
var submit_form = function(e) {
  $.getJSON($SCRIPT_ROOT + '/_run_address', {
    a: $('input[name="a"]').val()
  }, function(data) {
    $('input[name=a]').focus().select();
    $('#get_address_result').text(data.result);
  
    histWrapper(data.result_df);
    bulletWrapper(data.result_saleprice);

  });
  return false;
};
$('a#calculate').bind('click', submit_form);
$('input[type=text]').bind('keydown', function(e) {
  if (e.keyCode == 13) {
    submit_form(e);
  }
});
$('input[name=a]').focus();


var bulletWrapper = function(new_data) {
  var chart;
  d3.select("#chart").selectAll("svg > *").remove()
  nv.addGraph(function() {
      chart = nv.models.bulletChart()
          .margin({left: 150});

      d3.select('#chart svg')
          .datum(new_data)
          .call(chart);

      nv.utils.windowResize(chart.update);

      chart.dispatch.on('stateChange', function(e) { 
          nv.log('New State:', JSON.stringify(e)); });
      chart.state.dispatch.on('change', function(state){
          nv.log('state', JSON.stringify(state));
      });
      return chart;
  });
};

var histWrapper = function(new_data) {
  var chart;
  d3.select("#chart1").selectAll("svg > *").remove()
  nv.addGraph(function() {
      chart = nv.models.multiBarHorizontalChart()
          .x(function(d) { return d.label })
          .y(function(d) { return d.value })
          .barColor(d3.scale.category20().range())
          .duration(500)
          .margin({left: 150})
          .stacked(false)
          .showControls(false);

      chart.yAxis.tickFormat(d3.format(',.2f'));

      chart.yAxis.axisLabel('Count or Price / $10,000');

      d3.select('#chart1 svg')
          .datum(new_data)
          .call(chart);

      nv.utils.windowResize(chart.update);

      chart.dispatch.on('stateChange', function(e) { 
          nv.log('New State:', JSON.stringify(e)); });
      chart.state.dispatch.on('change', function(state){
          nv.log('state', JSON.stringify(state));
      });
      return chart;
  });

};

function exampleData() {
  return {
    "title":"Revenue",      //Label the bullet chart
    "subtitle":"US$, in ten thousands",     //sub-label for bullet chart
    "ranges":[150,225,300],  //Minimum, mean and maximum values.
    "measures":[220]        //Value representing current measurement (the thick blue line in the example)
  };
}

});
