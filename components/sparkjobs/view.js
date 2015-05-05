/**
 * Created by wanggen on 15/4/1.
 */

$("#btn-add-job").click(function () {
    $("#panel-add-job").slideToggle('normal');
    $(this).toggleClass('show-form').toggleClass('hide-form');
});


$("form button[type='submit']").click(function(e){
    e.preventDefault();
    var hour = parseInt($("#hour").val()), ttl = parseInt($("#ttl").val());
    if($("#job_id").val()==''){alert("job id can't be empty"); return;}
    if(!(hour>=0 && hour<=23)){ alert("hour must between 0~23"); return;}
    if(!(ttl>=0 && ttl<=365)){ alert("expires days must between 0~365"); return;}
    if($("#sql").val()==''){alert("job sql can't be empty"); return;}
    $("form").submit()
});

$(".btn-del-job").click(function () {
    var $btn_del_job = $(this);
    modal({
        body: '<h5>确认删除该任务?删除后无法恢复</h5>',
        confirm: function(){
            $.ajax({
                url: '/sparkjob/remove',
                type: 'PUT',
                data: {job_id: $btn_del_job.parent().parent().children(":first").text()},
                success: function () {
                    var tr = $btn_del_job.parent().parent();
                    tr.next().remove(); tr.remove();
                },
                error: function (data) { alert("job 删除失败:" + data) }
            })
        }
    });
});

$(".btn-job-start").click(function (e) {
    var job_id = $(this).parent().parent().children(":first").text();
    modal({
      body: '<h5>是否确认重新执行该任务</h5>',
      confirm: function(){
          $.ajax({
              url: '/sparkjob/start/'+job_id,
              type: 'GET',
              success: function(data){

              },
              error: function (data) {
                  alert("执行job错误:"+data)
              }
          })
      }
    });
});


$(".btn-job-stop").click(function (e) {
    var job_id = $(this).parent().parent().children(":first").text()
    $.ajax({
        url: '/sparkjob/stop/'+job_id,
        type: 'GET',
        success: function(data){

        },
        error: function (data) {
            alert("执行job错误:"+data)
        }
    })
});


$result_table=$(".table-job-result");
$(".btn-view-result").click(function () {
    var job_id = $(this).parent().parent().children(":first").text();

    $.getJSON('/sparkjob/result/'+job_id, function (rows) {
        $result_table.find("thead tr").html('');
        $result_table.find("tbody").html('');
        if(rows.length>0){

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
        }
    })
});


$("#table-job").find("tbody tr th").click(function () { $(this).parent().next().toggle(); });

$("#search").keyup(function () {
    var word=$(this).val();
    _.each($(".row-job"), function (node) {
        node = $(node);
        if(node.find(":first-child").html().indexOf(word)==-1)
            node.hide();
        else node.show();
    });
});
