var url = 'http://localhost:5000/gtlddb/registries';

var values_count = [];
//var values_domains = []
var labels = [];
Plotly.d3.json(url, function (figure) {
    console.log(figure);
    var data = figure.data;

    
    for (var i = 0; i < data.length; i++) {
        values_count.push(data[i]['count']);
        labels.push(data[i]['registries']);

    }
    console.log(values_count);
    console.log(labels);
    var trace = [{
        
        values: values_count,
        type: 'pie',
        labels: labels,
        domain: { x: [0, 1] },
        textinfo: 'REGISTRIES COUNT',
        hoverinfo: 'labels+values_share',
        hole: .4
        

    
    }];



    var layout = {
        title: 'REGISTRIES COUNT',
        annotations: [
            {
                font: {
                    size: 20
                },
                showarrow: false,
                text: 'REG',
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
    

Plotly.newPlot('slide', trace, layout);

})
