/**
 * Created by wanggen on 15/3/25.
 */

$.getJSON('/getusersummary', function(data){

    data = data.reverse();

    var dates   = _.map(data, function(row){ return row['date'].substr(6,2) });
    var incrs   = _.map(data, function(row){ return row['incr'] });
    var totals  = _.map(data, function(row){ return row['total'] });
    var type = dates.length <= 10 ? 'column' : 'spline';
    $('#container').highcharts({
        chart: {
            type: type
        },
        title: {
            text: '用户流量 '+'<strong>'+data[0]['date'].substr(0,6)+'</strong>'
        },
        xAxis: {
            categories: dates
        },
        yAxis: {
            min: 0,
            title: {
                text: '人数'
            },
            stackLabels: {
                enabled: true,
                style: {
                    fontWeight: 'bold',
                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                }
            }
        },
        legend: {
            align: 'right',
            x: -70,
            verticalAlign: 'top',
            y: 20,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColorSolid) || 'white',
            borderColor: '#CCC',
            borderWidth: 1,
            shadow: false
        },
        tooltip: {
            formatter: function() {
                return '<b>'+ this.x +'</b><br>'+
                    this.series.name +': '+ this.y +'<br>'+
                    'Total: '+ this.point.stackTotal;
            }
        },
        plotOptions: {
            column: {
                stacking: 'normal',
                dataLabels: {
                    enabled: true,
                    color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
                }
            }
        },
        series: [{
            name: '每日增长',
            data: incrs
        }, {
            name: '总数量',
            data: totals
        }]
    });


});