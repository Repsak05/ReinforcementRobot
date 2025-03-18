extends Node3D

@export var speed = 5

func _process(delta):

	if Input.is_action_pressed("q"):
		self.position.x -= speed * delta

	if Input.is_action_pressed("e"):
		self.position.x += speed * delta
