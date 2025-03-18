extends RigidBody3D

@export var rngLimits = 2

var rng = RandomNumberGenerator.new()
var beginForce = rng.randf_range(-rngLimits, rngLimits)

func _ready():
    beginForce = rng.randf_range(-2.0, 2.0)
    
    print(beginForce)
    self.add_constant_force(Vector3(beginForce, 0, 0))





