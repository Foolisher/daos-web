/**
 * Created by wanggen on 15/3/25.
 */

$.getJSON('/getdealsummary', function(data){

    data = data.reverse();

    var dates       = _.map(data, function(row){ return row['sum_for'].substr(6,2) });
    var deals       = _.map(data, function(row){ return row['deal'] });
    var deal_items  = _.map(data, function(row){ return row['deal_item'] });
    var deal_orders = _.map(data, function(row){ return row['deal_order'] });
    var type = dates.length <= 10 ? 'column' : 'spline';

    $('#container').highcharts({
        chart: {
            type: type
        },
        title: {
            text: '交易数据'
        },
        subtitle: {
            text: '<strong>'+data[0]['sum_for'].substr(0,6)+'</strong>'
        },
        xAxis: {
            //categories: dates
        },
        yAxis: {
            min: 0,
            title: {
                text: ''
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
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
        series:
            [
                {
                    name: '交易金额',
                    data: deals
                },
                {
                    name: '商品销量',
                    data: deal_items
                },
                {
                    name: '订单量',
                    data: deal_orders
                }
            ]
    });

});


