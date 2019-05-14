$(document).foundation()

var refresh_tasks, show_task_details;

$(document).ready(function () {
    console.log("on load");
    refresh_tasks();
    $("div#task_details_window").hide();
});

function refresh_tasks() {
    let loader = $("div#refresh.loader").show();
    $.getJSON("/input_set/list", function(data) {
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
        
        $(loader).hide();
    })
}

$("a#refresh.button").click(refresh_tasks);

function refresh_task_details(input_id) {
    $.getJSON("/input_set/"+input_id, function (data) {
        if (!data.status) return;
        data = data.info
        console.log(data);
        $("#panel1 pre").text(
            JSON.stringify(data.input_json.sockets).replace(/\{/g, "\n  {")
        );
        $("#panel2 pre").text(
            JSON.stringify(data.input_json.constraints, null, 2) + "\n\n" +
            JSON.stringify(data.input_json.similarity_function, null, 2)
        );
    })
}

function show_task_details() {
    let input_id = $($(this).children()[0]).text();
    $("div#task_details_window").show();
    refresh_task_details(input_id)
    
}


