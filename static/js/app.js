$(document).foundation()

var refresh_tasks, show_task_details;

$(document).ready(function () {
    console.log("on load");
    refresh_tasks();
});

function refresh_tasks() {
    $.getJSON("input_set/list", function(data) {
        console.log(data);
        // return if empty
        if (!data.status) return; 

        // empty table
        let tbody = $("tbody#tasks_body");
        tbody.empty();

        for (let i=0; i<data.tasks.length; i++) {
            let tr = $('<tr/>');
            $(tr).append("<td>" + data.tasks[i].input_id + "</td>");
            $(tr).append("<td>" + data.tasks[i].task_id + "</td>");
            $(tr).append("<td>" + data.tasks[i].running + "</td>");
            $(tr).append("<td>" + data.tasks[i].progress + "</td>");
            $(tr).click(show_task_details);
            tbody.append(tr);
        }
        // $("tbody#tasks_body tr").click(show_task_details);
    })
}

$("a#refresh.button").click(refresh_tasks);

function refresh_task_details() {

}

function show_task_details() {
    let input_id = $(this).children()[0];
    $("div#task_details_window").show();
    $.getJSON("")
    console.log();
}


