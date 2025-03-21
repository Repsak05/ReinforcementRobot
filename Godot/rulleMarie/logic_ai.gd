extends Node

@onready var platform = $Bodys/platform
@onready var ball = $Bodys/ball
@onready var setPoint = $setPoint

func _process(delta):
	
	platform.rotation = Vector3(0, 0,5 * pow(ball.transform.origin.x - setPoint.transform.origin.x, 3) + ball.transform.origin.x - setPoint.transform.origin.x) * delta
	
	pass
