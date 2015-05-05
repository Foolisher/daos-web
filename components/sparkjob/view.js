/**
 * Created by wanggen on 15/4/13.
 */

var $result_table = $('.table-job-result');

var data;

var num_pattern = /^([-]){0,1}([0-9]){1,}([.]){0,1}([0-9]){0,}$/;

var job_id = $("#job_id").data('id');

var $chart_container = $('#container');

$.getJSON('/sparkjob/result/'+job_id, function (rows) {
    $result_table.find("thead tr").html('');
    $result_table.find("tbody").html('');

    if(rows.length>0){
        data = rows
        $(".job-id-name").html(rows[0]['job_id']);

        var header = '<th>#</th>', k, n=1;
        var row_1=JSON.parse(rows[0]['result']);
        for (k in row_1) header += '<th>' + k + '</th>'
        $result_table.find("thead tr").html(header);

        _.each(rows, function(row){
            var tds = '<tr><td>'+(n++)+'</td>', k;
            var data_row=JSON.parse(row['result']);
            for (k in data_row) tds += '<td>' + data_row[k] + '</td>';
            tds += '</tr>';
            $result_table.find("tbody").append(tds)
        });

        $result_table.tablesort();
        $result_table.find('tbody tr td:contains("Exception: ")').css('background-color','#e51c23').css('color','white')

        renderChart()

    }
});


function renderChart() {
    var columns = {}, series, date, dates=[];
    if(data.length>0){
        _.each(data.reverse(), function(row){
            var resultSet = JSON.parse(row.result);
            for(p in resultSet){
                num_pattern.test(resultSet[p]) && (columns[p]=(columns[p] || {'name':p, data:[]})).data.push(resultSet[p]);
            }
            console.log(row)
            date = date || row.order_key.substr(0, 10);
            dates.push(row.order_key)
        });
        series = _.map(columns,function(e){ return e });
    }
    if(!series || series.length<1){
       $(".h2-report").hide(); $chart_container.hide();
    }
    $chart_container.highcharts({
        chart: {
            type: data.length <= 10 ? 'column' : 'spline'
        },
        title: {
            text: job_id
        },
        subtitle: {
            //text: '<strong>'+date+'</strong>'
        },
        xAxis: {
            tickInterval: 1000000,
            categories: dates
        },
        yAxis: {
            min: 0,
            title: {
                text: ''
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px; color: red;">#{point.key}</span><table>',
            pointFormat:  '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: series
    });
}


