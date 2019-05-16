
# Marker Conguration Service

## Installation && Running

Prerequisite: python3 with virtualenv. (eg. [Anaconda](https://www.anaconda.com/distribution/))

```bash
# setup virtual environment
virtualenv venv

# activate envirnoment
./venv/Script/activate  #  Window
. ./venv/bin/activate  # Linux

# Install
pip install -r requirements.txt

# Running
python ./app.py

```

Then, go to <http://localhost:5000/> to access the UI.
.

## Format

### Marker

Maker are defined as their `x y z` coordinates

```json
x: float
y: float
z: float

Example:
{ "x": 1.0, "y": 1.0, "z": 1.0 }
```

In processing markers will be stored as vecotrs and stored contiguously
.

### Maker Configuration

Maker configuration is a list of `makers` and a list of rspective `mount_point_id` and `length` used

```json
sockets_and_lengths
socket_id: [int]
stick_id: [int]

Example:
{   "markers": [
            {"x": 1.0, "y": 1.0, "z": 1.0 },
            {"x": 2.0, "y": 1.0, "z": 1.0 },
            {"x": 1.0, "y": 2.0, "z": 1.0 },
            {"x": 1.0, "y": 1.0, "z": 2.0 }
        ],
    "socket_ids": [ 0, 2, 3, 4 ],
    "stick_ids": [ 0, 0, 1, 0 ]
}
```

.

### Combination Input Set

Combination input set consist of `sockets`, `constraints` and `similarity_function`.

`sockets:` mount points is a list of mount point which consists of its coordinate in `x, y, z` and its mounting direction as `vx, vy, vz` forming unit vector

`contraints:` constraints are stored as a dictionary

`similarity_function:` simiarity funciton are is codes to specify which similarity function to be used with its respective parameters

```json
Mount Point:-
x: float
y: float
z: float
vx: float
vy: float
vz: float
* l2_norm([vx, vy, vz]) == 1

Contraints:-
n_markers: [ int ] (number of markers to be used)
stick_lengths: [ float ] (length of stick available for configuration)

Simiarity Function:
name: string
param names: param values

{
    "sockets": [
        {"x": 0.0, "y": 0.0, "z": 0.0,  "vx": 1.0, "vy": 0.0, "vz": 0.0},
        {"x": 0.0, "y": 0.0, "z": 0.0,  "vx": -1.0, "vy": 0.0, "vz": 0.0},
        {"x": 0.0, "y": 0.0, "z": 0.0,  "vx": 0.0, "vy": 0.0, "vz": 1.0},
        {"x": 0.0, "y": 10.0, "z": 0.0,  "vx": 1.0, "vy": 0.0, "vz": 0.0},
        {"x": 0.0, "y": 10.0, "z": 0.0,  "vx": -1.0, "vy": 0.0, "vz": 0.0},
        {"x": 0.0, "y": 10.0, "z": 0.0,  "vx": 0.0, "vy": 0.0, "vz": 1.0}

    ],
    "constraints": {
        "n_markers": [4, 5, 5],
        "stick_lengths": [ 10.0, 30.0, 50.0 ]
    },
    "similarity_function": {
        "name": "l2_point_norm",
        "avg_threshold": 10.0,
        "max_threshold": 20.0
    }
}
```

.

## Library Used

### Python

- [flask](flask.pocoo.org/)
- [numpy](https://www.numpy.org/)

### Javascript

- [Foundation sites](https://foundation.zurb.com/sites.html)
- [Three.js](http://threejs.org/)
