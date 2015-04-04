/**
 * Created by wanggen on 15/3/27.
 */

$table = $("#board");
$note = $(".alert-danger");
$sql = $('#sql');
$time = $('#time');
$sql.val($.cookie('sql_his'));
$note.hide();

$(".btn-sql-query").click(function () {
    var time=0;
    var sql = $sql.val();
    console.log(sql);
    $.cookie('sql_his', sql, {expires: 7});
    if(_.isEmpty(sql)) return;
    $table.find("thead tr").html('');
    $table.find("tbody").html('');
    $note.hide().find('p').html('');
    $(this).addClass('disabled');
    var check = setInterval(function(){ $time.text((time+=100)/1000+" s")}, 100);
    $.ajax({
        type: "POST",
        url: "/sql",
        data: sql,
        success: function(data){
            if (data.data !== undefined) {
                data = data.data;
                var header = '', k;
                for (k in data[0]) header += '<th>' + k + '</th>'
                $table.find("thead tr").html(header);
                _.each(data, function(row){
                    var tds = '<tr>', k;
                    for (k in row) tds += '<td>' + row[k] + '</td>';
                    tds += '</tr>';
                    $table.find("tbody").append(tds)
                })
            }else{
                $note.find('p').html(data.error); for(i in [1,2,3]) $note.fadeToggle("fast")
            }
        },
        error: function(msg){
            $note.find('p').html(msg.error); for(i in [1,2,3]) $note.fadeToggle("fast")
        },
        complete: function(){
            $(".btn-sql-query").removeClass('disabled');
            clearInterval(check);  for(i in [1,2,3,4]) $time.fadeToggle()
        },
        dataType: 'json'
    });

});