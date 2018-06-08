# epicPong configs


SCREEN_SIZE = 600
MARGIN = 40
FPS = 30

GAME_TITLE = "EPIC PONG"
GAME_MUSIC = "sounds/background_music.mp3"
GAME_MUSIC_VOLUME = 0.1
BACKGROUND_COLOR = "black"
BACKGROUND_STAR_COLORS = (BACKGROUND_COLOR, "white", "yellow", "orange","snow1", "yellow3", "SkyBlue", "tomato")
BACKGROUND_STAR_NUMBER = 50
BACKGROUND_IMAGE = "images/background.gif"
BORDER_COLOR = "red"
BORDER_WIDTH = 3
TEXT_FONT = ("Arial", 10, "bold")
# TEXT_FONT_BIG = ("Courier New", 20, "bold")
TEXT_COLOR = "blue"
IMAGES_DIRECTORY = "images/"

PLAYER_INIT_POSX = 0
PLAYER_INIT_POSY = -275
PLAYER_INIT_HEADING = 0
PLAYER_INIT_VELOCITY = 0
PLAYER_INIT_SHAPE = "images/init_racket.gif"
PLAYER_END_SHAPE = "images/player.gif"
PLAYER_TURN_ANGLE = 0
PLAYER_INIT_POINTS = 0
PLAYER_HEALTH_POINTS = 100
PLAYER_EXPLOSION_COLORS = ["red", "blue", "green","purple", "gold", "yellow"]
PLAYER_EXPLOSION_SOUND = "sounds/rocket_destroy.wav"


BAR_ENEMY_SHAPE = "images/bar_enemy.gif"


BALL = "images/BALL.gif"
BALL_IMAGE = "images/ball_image.gif"
BALL_IMAGE_UP = "images/ball_image_up.gif"
BALL_IMAGE_DOWN = "images/ball_image_down.gif"
BALL_ADDED_VELOCITY = 20
BALL_SOUND_SHOOT = "sounds/launch.wav"

MISSILE_SHAPE = "images/missile.gif"
MISSILE_ADDED_VELOCITY = 20
MISSILE_SOUND_SHOOT = "sounds/missile_shoot.wav"

BOSS_INIT_POSX = 0
BOSS_INIT_POSY = 150
BOSS_INIT_HEADING = 0
BOSS_INIT_SHAPE = "images/level1_boss.gif"
BOSS_LEVEL2 = "images/level2_boss.gif"
BOSS_LEVEL3 = "images/colorfull_very_big_boss.gif"
BOSS_LEVEL4 = "images/final_boss.gif"
BOSS_INIT_VELOCITY = 10
BOSS_EXPLOSION_SOUND = "sounds/enemy_destroy.wav"
BOSS_INIT_HEALTH = 400

NET_SHAPE = "images/boss_net.gif"
NET_VELOCITY = 10
NET_LAUNCH_SOUND = "sounds/net_launch.wav" 

# PLAYER_ACCELERATE_KEY = "Up"
# PLAYER_DECELERATE_KEY = "Down"
# PLAYER_TURN_LEFT_KEY = "Left"
# PLAYER_TURN_RIGHT_KEY = "Right"
# PLAYER_SHOOT_MISSILE_KEY = "space"
