Plotly.d3.csv("static/data/csv/registrars.csv", function(err, rows){

  function unpack(rows, key) {
  return rows.map(function(row) { return row[key]; });
  }

  var headerNames = Plotly.d3.keys(rows[0]);

  var headerValues = [];
  var cellValues = [];
  for (i = 0; i < headerNames.length; i++) {
    headerValue = [headerNames[i]];
    headerValues[i] = headerValue;
    cellValue = unpack(rows, headerNames[i]);
    cellValues[i] = cellValue;
  }

  // clean date
  for (i = 0; i < cellValues[1].length; i++) {
  var dateValue = cellValues[1][i].split(' ')[0]
  cellValues[1][i] = dateValue
  }


var data = [{
  type: 'table',
  columnwidth: [200,500,600,600,400,400,600,600,600],
  columnorder: [0,1,2,3,4,5,6,7,8,9],
  header: {
    values: headerValues,
    align: "center",
    line: {width: 1, color: 'rgb(50, 50, 50)'},
    fill: {color: ['rgb(234, 144, 119)']},
    font: {family: "Arial", size: 11, color: "black"}
  },
  cells: {
    values: cellValues,
    align: ["center", "center"],
    line: {color: "black", width: 1},
    fill: {color: ['rgba(239, 187, 172, 0.65)','rgb(247, 177, 158)', 'rgba(249, 202, 189, 0.65)']},
    font: {family: "Arial", size: 10, color: ["black"]}
  }
}]

var layout = {
  title: "Registrar Tabular Data"
}

Plotly.plot('table', data, layout);
});