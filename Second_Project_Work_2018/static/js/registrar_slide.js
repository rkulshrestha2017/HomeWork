var url = 'http://localhost:5000/gtlddb/totalregistrar';
var xField = 'DATE';
var yField = 'TOTAL REGISTRARS IN MILLION';

var selectorOptions = {
    buttons: [{
        step: 'month',
        stepmode: 'backward',
        count: 1,
        label: '1m'
    }, {
        step: 'month',
        stepmode: 'backward',
        count: 6,
        label: '6m'
    }, {
        step: 'year',
        stepmode: 'todate',
        count: 1,
        label: 'YTD'
    }, {
        step: 'year',
        stepmode: 'backward',
        count: 1,
        label: '1y'
    }, {
        step: 'all',
    }],
};

Plotly.d3.json(url, function (err, rawData) {
    if (err) throw err;

    var data = prepData(rawData);
    var layout = {
        title: 'TOTAL REGISTRARS IN MILLION vs DATE',
        
        xaxis: {
            title: "DATE" ,
            rangeselector: selectorOptions,
            rangeslider: {}
        },
        yaxis: {
            title: "TOTAL REGISTRARS IN MILLION",
            fixedrange: true
        }
    };
   

    Plotly.plot('slide', data, layout);
});

function prepData(rawData) {
    var x = [];
    var y = [];

    let data = rawData.data
    for (var i = 0; i < data.length; i++) {
        x.push(data[i]['date']);
        y.push(data[i]['total_registrar']);
    }

    // rawData.forEach(function(datum, i) {

    //     x.push(new Date(datum['date']));
    //     y.push(datum['total_registrar']);
    // });

    return [{
        mode: 'lines',
        x: x,
        y: y,
        marker: {
            color: 'rgb(55, 83, 109)'},
            type:'line',
        
    }];
}