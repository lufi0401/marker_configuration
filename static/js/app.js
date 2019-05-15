$(document).foundation()

var refresh_tasks, show_task_details, current_task, scene_init;

// Inits
$(document).ready(function () {
    console.log("on load");
    $(".loader").hide()
    refresh_tasks();
    $("div#task_details_window").hide();
});

// Task list related
function refresh_tasks() {
    let loader = $("div#refresh.loader").show();
    $.getJSON("/input_set/list", function(data) {
        // return if empty
        if (!data.status) return; 

        // empty table
        let tbody = $("tbody#tasks");
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

// Tasks details related
function refresh_task_progress() {
    let input_id = current_task.input_id;
    let loader = $('div#progress_update div.loader');
    loader.show()
    $.getJSON("/input_set/"+input_id, function (data) {
        loader.hide()
        setTimeout(refresh_task_progress, 5000);
        if (!data.status) return;
        current_task = data.info;

        $("div#progress_update p").text(current_task.progress);
    })
}

function show_task_details() {
    let input_id = $($(this).children()[0]).text();
    $("div#task_details_window").show();

    $.getJSON("/input_set/" + input_id, function (data) {
        if (!data.status) return;
        current_task = data.info;
        // update socket_table
        let sockets = current_task.input_json.sockets;
        let tbody = $("tbody#sockets");
        tbody.empty();
        for (let i in sockets) {
            let tr = $('<tr/>');
            $(tr).append("<td>" + sockets[i].x + "</td>");
            $(tr).append("<td>" + sockets[i].y + "</td>");
            $(tr).append("<td>" + sockets[i].z + "</td>");
            $(tr).append("<td>" + sockets[i].vx + "</td>");
            $(tr).append("<td>" + sockets[i].vy + "</td>");
            $(tr).append("<td>" + sockets[i].vz + "</td>");
            tbody.append(tr);
        }

        // update contraints and similarity_function
        $("pre#cons_sims").text(
            JSON.stringify(current_task.input_json.constraints, null, 2) + "\n\n" +
            JSON.stringify(current_task.input_json.similarity_function, null, 2)
        );

        $("div#progress_update p").text(current_task.progress);
        
        // setup unique_set
        let n_unique_set = 0;
        if (current_task.result_json != null)
            n_unique_set = current_task.result_json.length
        let selector = $("div#unique_set_select")
        $(selector).empty();
        $(selector).append('\
            <div class="slider" data-slider >\
                <span class="slider-handle" data-slider-handle role="slider" tabindex="1""></span>\
            </div>\
        ');
        $(selector).children().attr("data-end",n_unique_set);
        $(selector).children().children().attr('aria-controls',"cur_unique_set"); 
        $(selector).foundation();
        $(selector).children().on('changed.zf.slider', three_update_unique_set);

        setTimeout(refresh_task_progress, 5000);
    })

    three_init();

}

// visualizer related
var set_scene = null, three_resize;

function three_init() {
    if (set_scene != null) return;

    set_scene = {};

    set_scene.container = $('#three_container');
    
    set_scene.renderer = new THREE.WebGLRenderer();
    $(set_scene.container).empty();
    $(set_scene.container).append(set_scene.renderer.domElement);
    $(set_scene.container).resize(three_resize);
    set_scene.w = 1000.;
    set_scene.h = 500.;
    set_scene.renderer.setSize(set_scene.w, set_scene.h);


    set_scene.scene = new THREE.Scene();
    set_scene.scene.background = new THREE.Color(0x505050);

    set_scene.camera = new THREE.PerspectiveCamera(75, set_scene.w/set_scene.h, 0.1, 1000)
    set_scene.camera.position.set(50, 10, 0);
    set_scene.camera.lookAt(0, 0, 0)
    set_scene.controls = new THREE.OrbitControls(set_scene.camera, set_scene.container.get(0));
    set_scene.controls.saveState();

    let light = new THREE.HemisphereLight(0xffffff, 0x444444);
    set_scene.scene.add(light);

    let grid = new THREE.GridHelper(300, 20, 0xffffff, 0xdddddd);
    grid.position.y = -5;
    grid.material.opacity = 0.4;
    grid.material.transparent = true;
    set_scene.scene.add(grid);

    let axes = new THREE.AxesHelper(10);
    set_scene.scene.add(axes);

    animate();
};

function animate() {
    requestAnimationFrame(animate);
    if (set_scene.container.width() != set_scene.w)
        three_resize();
    set_scene.controls.update();
    set_scene.renderer.render(set_scene.scene, set_scene.camera);
};

function three_resize() {
    console.log("three_resize")
    set_scene.w = set_scene.container.width();
    set_scene.renderer.setSize(set_scene.w, set_scene.h);
    set_scene.camera.aspect = set_scene.w / set_scene.h;
    set_scene.camera.updateProjectionMatrix();
};

function three_update_unique_set() {
    let tbody = $("tbody#unique_set");
    tbody.empty();

    if (set_scene.unique_set != null)
        set_scene.scene.remove(set_scene.unique_set);

    if (current_task.result_json == null || current_task.result_json.length <= 0) 
        return;
    
    let unique_set_id = $('input#cur_unique_set').val();
    let positions = current_task.result_json[unique_set_id].markers
    let geometry = new THREE.SphereGeometry(1);
    let material = new THREE.MeshPhongMaterial({ color: 0xefefef });

    let new_unique_set = new THREE.Object3D();
    for (let i in positions) {
        let pos = positions[i];
        let ball = new THREE.Mesh(geometry, material);
        ball.position.set(pos["x"], pos["y"], pos["z"]);
        new_unique_set.add(ball);
    }

    set_scene.unique_set = new_unique_set;
    set_scene.scene.add(set_scene.unique_set);

    
    for (let i in positions) {
        let tr = $('<tr/>');
        $(tr).append("<td>" + positions[i].x + "</td>");
        $(tr).append("<td>" + positions[i].y + "</td>");
        $(tr).append("<td>" + positions[i].z + "</td>");
        tbody.append(tr);
    }
};
