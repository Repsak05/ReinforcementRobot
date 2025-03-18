extends Node

@onready var platform = $Bodys/platform
@onready var ball = $Bodys/ball

func _process(delta):
	
	platform.rotation = Vector3(0, 0,   pow(ball.transform.origin.x, 5)) * delta
	
	pass
