
# Marker Conguration Service


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

<br />

### Maker Configuration
Maker configuration is a list of `makers` and a list of rspective `mount_point_id` and `length` used
```json
mount_points_and_lengths
id: int
len: float

Example:
{   "markers": [
            {"x": 1.0, "y": 1.0, "z": 1.0 },
            {"x": 2.0, "y": 1.0, "z": 1.0 },
            {"x": 1.0, "y": 2.0, "z": 1.0 },
            {"x": 1.0, "y": 1.0, "z": 2.0 }
        ],
    "mount_points_and_lengths" [
        {"id": 0, "len": 30.0},
        {"id": 2, "len": 30.0},
        {"id": 3, "len": 40.0},
        {"id": 4, "len": 30.0},
    ]
}
```

<br />

### Combination Input Set
Combination input set consist of `mount_points`, `constraints` and `similarity_function`.

`mount_points:` mount points is a list of mount point which consists of its coordinate in `x, y, z` and its mounting direction as `vx, vy, vz` forming unit vector

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

Example
{
    "mount_points": [
        {"x": 1.0, "y": 1.0, "z": 1.0,  "vx": 1.0, "vy": 0.0, "vz": 0.0},
        {"x": 1.0, "y": 1.0, "z": 1.0,  "vx": 0.0, "vy": 1.0, "vz": 0.0},
        {"x": 1.0, "y": 2.0, "z": 1.0,  "vx": 0.5774, "vy": 0.5774, "vz": 0.5774},
        {"x": 1.0, "y": 1.0, "z": 2.0,  "vx": 0.0, "vy": 0.0, "vz": 1.0}
    ],
    "constraints": {
        "n_markers": [4, 5],
        "stick_lengths": [ 30.0, 40.0 ]
    },
    "similarity_function": {
        "name": "l2_point_norm",
        "threshold": 10
    } 
}


```
