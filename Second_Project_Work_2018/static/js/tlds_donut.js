var url = 'http://localhost:5000/gtlddb/tlds';

var values_share = [];
//var values_domains = []
var labels = [];
Plotly.d3.json(url, function (figure) {
    console.log(figure);
    var data = figure.data;

    
    for (var i = 0; i < data.length; i++) {
        values_share.push(data[i]['share']);
        labels.push(data[i]['tlds']);

    }
    console.log(values_share);
    console.log(labels);
    var trace = [{
        
        values: values_share,
        type: 'pie',
        labels: labels,
        domain: { x: [0, 1] },
        textinfo: 'TLDS SHARE %',
        hoverinfo: 'labels+values_share',
        hole: .4
        

    
    }];



    var layout = {
        title: 'TLDS PERCENT SHARE',
        annotations: [
            {
                font: {
                    size: 20
                },
                showarrow: false,
                text: 'TLDS',
                x: 0.5,
                y: 0.5
            }
            // {
            //     font: {
            //         size: 20
            //     },
            //     showarrow: false,
            //     text: 'TD',
            //     x: 0.82,
            //     y: 0.5
            // }
        ],
        
    };
    

Plotly.newPlot('donut', trace, layout);

})
