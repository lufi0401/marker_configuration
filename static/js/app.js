$(document).foundation()

var refresh_tasks, show_task_details, current_task, scene_init;

// Inits
$(document).ready(function () {
    console.log("loaded");
    $("div#task_details_window").hide();
    refresh_tasks();
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
            $(tr).click(function() {
                show_task_details($($(this).children()[0]).text());
            });
            tbody.append(tr);
        }

        $(loader).hide();
    })
}

$("a#refresh.button").click(refresh_tasks);

$("input:file#upload").change(() =>{
    let file = $("input:file#upload").prop("files")[0];
    let fileReader = new FileReader();
    fileReader.onerror = () => { alert("Failed to read selected file.") };
    fileReader.onload = () => {
        let result = fileReader.result;
        console.log(result)
        if (!result.startsWith("data:application/json")) {
            alert("Selected file is not json");
            return;
        }
        let file_data;
        try {
            file_data = atob(result.substr(result.match("base64").index + 7));
        } catch (err) {
            alert("Failed to read selected file: "+err.message);
            return;
        }
        $.ajax({
            url: "/input_set/upload",
            type: "POST",
            data: file_data,
            contentType: "application/json",
            success: (data) => {
            if (!data.status) {
                alert("Failed to upload: "+data.message);
                return;
            }
            refresh_tasks();
            show_task_details(data.input_set_id);
            }
        })

    };
    fileReader.readAsDataURL(file);
})
// "data:application/json;base64,ew0KICAgICAgICAic29ja2V0cyI6IFsNCiAgICAgICAgICAgIHsieCI6IDAuMCwgInkiOiAwLjAsICJ6IjogMC4wLCAgInZ4IjogMS4wLCAidnkiOiAwLjAsICJ2eiI6IDAuMH0sDQogICAgICAgICAgICB7IngiOiAwLjAsICJ5IjogMC4wLCAieiI6IDAuMCwgICJ2eCI6IC0xLjAsICJ2eSI6IDAuMCwgInZ6IjogMC4wfSwNCiAgICAgICAgICAgIHsieCI6IDAuMCwgInkiOiAwLjAsICJ6IjogMC4wLCAgInZ4IjogMC4wLCAidnkiOiAwLjAsICJ2eiI6IDEuMH0sDQogICAgICAgICAgICB7IngiOiAwLjAsICJ5IjogMTAuMCwgInoiOiAwLjAsICAidngiOiAxLjAsICJ2eSI6IDAuMCwgInZ6IjogMC4wfSwNCiAgICAgICAgICAgIHsieCI6IDAuMCwgInkiOiAxMC4wLCAieiI6IDAuMCwgICJ2eCI6IC0xLjAsICJ2eSI6IDAuMCwgInZ6IjogMC4wfSwNCiAgICAgICAgICAgIHsieCI6IDAuMCwgInkiOiAxMC4wLCAieiI6IDAuMCwgICJ2eCI6IDAuMCwgInZ5IjogMC4wLCAidnoiOiAxLjB9DQoNCiAgICAgICAgXSwNCiAgICAgICAgImNvbnN0cmFpbnRzIjogew0KICAgICAgICAgICAgIm5fbWFya2VycyI6IFs0LCA1LCA1XSwNCiAgICAgICAgICAgICJzdGlja19sZW5ndGhzIjogWyAxMC4wLCAzMC4wLCA1MC4wIF0NCiAgICAgICAgfSwNCiAgICAgICAgInNpbWlsYXJpdHlfZnVuY3Rpb24iOiB7DQogICAgICAgICAgICAibmFtZSI6ICJsMl9wb2ludF9ub3JtIiwNCiAgICAgICAgICAgICJhdmdfdGhyZXNob2xkIjogMTAuMCwNCiAgICAgICAgICAgICJtYXhfdGhyZXNob2xkIjogMjAuMA0KICAgICAgICB9IA0KICAgIH0=

// Tasks details related
var task_refreshing = null;

function update_progress(data) {
    let loader = $('div#progress_update div.loader');
    loader.hide();
    if (task_refreshing == null)
        task_refreshing = setInterval(() => {
            let input_id = current_task.input_id;
            loader.show()
            $.getJSON("/input_set/" + input_id, update_progress)
        }, 3000);
    if (!data.status) return;
    current_task = data.info;

    let start_button = $("a#start");
    let stop_button = $("a#stop");
    if (current_task.running) {
        $(start_button).addClass("disabled").hide();
        $(stop_button).removeClass("disabled").show();
    } else {
        $(stop_button).addClass("disabled").hide();
        $(start_button).removeClass("disabled").show();
    }

    $("div#progress_update p").text(current_task.progress);
}

function show_task_details(input_id) {
    $.getJSON("/input_set/" + input_id, function (data) {
        if (!data.status) return;
        $("div#task_details_window").show();
        $("b#task_id").text(input_id)
        update_progress(data);
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
        // setup sockets
        setTimeout(three_setup_sockets, 0);

        // update contraints and similarity_function
        $("pre#cons_sims").text(
            JSON.stringify(current_task.input_json.constraints, null, 2) + "\n\n" +
            JSON.stringify(current_task.input_json.similarity_function, null, 2)
        );

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

    })

    three_init();

}

$("a#start").click(() => {
    let input_id = current_task.input_id;
    let start_button = $("a#start");
    $(start_button).addClass("disabled");
    $.post("/input_set/" + input_id + "/start", (data) => {
        if (!data.status) {
            $(start_button).removeClass("disabled");
            alert("Start failed: " + data.message);
            return;
        } else {
            $(start_button).hide();
            alert("Task started.");
        }
        refresh_tasks();
    });
})

$("a#stop").click(() => {
    let input_id = current_task.input_id;
    let stop_button = $("a#stop");
    $(stop_button).addClass("disabled");
    $.post("/input_set/" + input_id + "/stop", (data) => {
        if (!data.status) {
            $(stop_button).removeClass("disabled");
            alert("Stop failed: " + data.message);
            return;
        } else {
            $(stop_button).hide()
            alert("Task Interrupted.");
        }
        refresh_tasks();
    })
})


// visualizer related
var set_scene = null;

function three_init() {
    if (set_scene != null) return;

    set_scene = {};

    set_scene.container = $('#three_container');

    set_scene.renderer = new THREE.WebGLRenderer({ antialias: true });
    $(set_scene.container).empty();
    $(set_scene.container).append(set_scene.renderer.domElement);
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

    set_scene.axes = new THREE.AxesHelper(10);
    set_scene.axes.position.set( -10, -5, -10 );
    set_scene.scene.add(set_scene.axes);

    animate();
};

function animate() {
    requestAnimationFrame(animate);
    if (set_scene.container.width() != set_scene.w) {
        set_scene.w = set_scene.container.width();
        set_scene.renderer.setSize(set_scene.w, set_scene.h);
        set_scene.camera.aspect = set_scene.w / set_scene.h;
        set_scene.camera.updateProjectionMatrix();
    }
    set_scene.controls.update();
    set_scene.renderer.render(set_scene.scene, set_scene.camera);
};

function three_setup_sockets() {
    if (set_scene.sockets != null)
        set_scene.scene.remove(set_scene.sockets);

    let sockets = current_task.input_json.sockets;

    let material = new THREE.MeshPhongMaterial({ color: 0xf94545 });
    let geometry = new THREE.CylinderGeometry(.5,0,.5);

    let new_sockets = new THREE.Group();
    set_scene.sockets = new_sockets
    set_scene.scene.add(new_sockets);

    let from_vec = new THREE.Vector3(0, 1, 0);
    for (let i in sockets) {
        let soc = sockets[i]

        let to_vec = new THREE.Vector3(soc["vx"], soc["vy"], soc["vz"])

        let quat = new THREE.Quaternion();
        quat.setFromUnitVectors(from_vec, to_vec);

        let disk = new THREE.Mesh(geometry, material);
        new_sockets.add(disk);
        disk.position.set(soc["x"], soc["y"], soc["z"])
        // disk.setRotationFromQuaternion(quat);
        disk.applyQuaternion(quat);
    }
}

function three_update_unique_set() {
    let tbody = $("tbody#unique_set");
    tbody.empty();

    if (set_scene.unique_set != null)
        set_scene.scene.remove(set_scene.unique_set);

    if (current_task.result_json == null || current_task.result_json.length <= 0)
        return;

    let unique_set_id = $('input#cur_unique_set').val();
    let positions = current_task.result_json[unique_set_id].markers;
    let socket_ids = current_task.result_json[unique_set_id].socket_ids;
    let sockets = current_task.input_json.sockets;

    let geometry = new THREE.SphereGeometry(1);
    let material = new THREE.MeshPhongMaterial({ color: 0xefefef });
    var line_material = new THREE.LineBasicMaterial({ color: 0xdddd00 });

    let new_unique_set = new THREE.Group();
    let axes_pos = { x: 1e9, y: 1e9, z: 1e9 };
    for (let i in positions) {
        let pos = positions[i];

        axes_pos.x = axes_pos.x < pos["x"] ? axes_pos.x : pos["x"];
        axes_pos.y = axes_pos.y < pos["y"] ? axes_pos.y : pos["y"];
        axes_pos.z = axes_pos.z < pos["z"] ? axes_pos.z : pos["z"];

        let ball = new THREE.Mesh(geometry, material);
        ball.position.set(pos["x"], pos["y"], pos["z"]);
        new_unique_set.add(ball);

        let skt_pos = sockets[socket_ids[i]];
        let line_geometry = new THREE.Geometry();
        line_geometry.vertices.push(
            new THREE.Vector3(pos["x"], pos["y"], pos["z"]),
            new THREE.Vector3(skt_pos["x"], skt_pos["y"], skt_pos["z"]),
        )
        var line = new THREE.Line( line_geometry, line_material );
        new_unique_set.add(line);

        let tr = $('<tr/>');
        $(tr).append("<td>" + positions[i].x + "</td>");
        $(tr).append("<td>" + positions[i].y + "</td>");
        $(tr).append("<td>" + positions[i].z + "</td>");
        tbody.append(tr);
    }

    set_scene.unique_set = new_unique_set;
    set_scene.scene.add(set_scene.unique_set);
    set_scene.axes.position.set(axes_pos.x-5, -5, axes_pos.z-5);

};
