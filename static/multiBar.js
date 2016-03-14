    var long_short_data = [
        {
            key: "Zipcode",
            values: [
                {
                    "label" : "Group A" ,
                    "value" : -1.8746444827653
                } ,
                {
                    "label" : "Group B" ,
                    "value" : -8.0961543492239
                } ,
                {
                    "label" : "Group C" ,
                    "value" : -0.57072943117674
                } ,
                {
                    "label" : "Group D" ,
                    "value" : -2.4174010336624
                } ,
                {
                    "label" : "Group E" ,
                    "value" : -0.72009071426284
                } ,
                {
                    "label" : "Group F" ,
                    "value" : -2.77154485523777
                } ,
                {
                    "label" : "Group G" ,
                    "value" : -9.90152097798131
                } ,
                {
                    "label" : "Group H" ,
                    "value" : 14.91445417330854
                } ,
                {
                    "label" : "Group I" ,
                    "value" : -3.055746319141851
                }
            ]
        },
    ];

    var llong_short_data = $("#result").data

    var chart;
    nv.addGraph(function() {
        chart = nv.models.multiBarHorizontalChart()
            .x(function(d) { return d.label })
            .y(function(d) { return d.value })
            //.yErr(function(d) { return [-Math.abs(d.value * Math.random() * 0.3), Math.abs(d.value * Math.random() * 0.3)] })
            .barColor(d3.scale.category20().range())
            .duration(250)
            .margin({left: 100})
            .stacked(true);

        chart.yAxis.tickFormat(d3.format(',.2f'));

        chart.yAxis.axisLabel('Count or Price / $100,000');
        chart.xAxis.axisLabel('Amenity Type').axisLabelDistance(20);

        d3.select('#chart1 svg')
            .datum(long_short_data)
            .call(chart);

        nv.utils.windowResize(chart.update);

        chart.dispatch.on('stateChange', function(e) { nv.log('New State:', JSON.stringify(e)); });
        chart.state.dispatch.on('change', function(state){
            nv.log('state', JSON.stringify(state));
        });
        return chart;
    });


