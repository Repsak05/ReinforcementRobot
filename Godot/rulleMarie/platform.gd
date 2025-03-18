extends StaticBody3D

@export var rotateSpeed = 1.5

func _process(delta):
    
    if Input.is_action_pressed("a") && self.rotation.z < 1:
        self.rotation += Vector3(0, 0, rotateSpeed) * delta
    
    if Input.is_action_pressed("d") && self.rotation.z > -1:
        self.rotation += Vector3(0, 0, -rotateSpeed) * delta


    