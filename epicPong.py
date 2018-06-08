"""
Created by Marc Aoun
With Reza Mousavi
Using Python 3
Encode utf-8
"""

#test.py
import turtle
from time import time, sleep
from math import sqrt
from random import randint, choice
from pygame import mixer
from utils import listAllFilesIn, intersection, jump
import config


class MyTurtle(turtle.Turtle):
    '''This class is really not necessary. It's only there to learn inheritence'''

    def square(self, length):
        for i in range(4):
            self.forward(length)
            self.left(90)

    def jump(self, x, y):
        self.penup()
        self.goto(x, y)
        self.pendown()


class Sprite(MyTurtle):
    allSprites = []

    def __init__(self, x, y, heading, shape, velocity):
        super().__init__()
        self.jump(x, y)
        self.setheading(heading)
        self.shape(shape)
        self.penup()
        self.velocity = velocity
        self.is_destroyed = False

        # when any object is created from any subclass of Sprite (e.g. Player, Enemy,...)
        # they get appended to this list
        Sprite.allSprites.append(self)

    def is_at_boundary(self):
        limit = config.SCREEN_SIZE/2 - 10
        boundaries_hit = []

        if self.xcor() > limit:
            self.setx(limit)
            boundaries_hit.append("right")
        if self.xcor() < -limit:
            self.setx(-limit)
            boundaries_hit.append("left")
        if self.ycor() > limit:
            self.sety(limit)
            boundaries_hit.append("top")
        if self.ycor() < -limit:
            self.sety(-limit)
            boundaries_hit.append("bottom")

        return boundaries_hit

    def bounce_off_boundaries(self):
        for boundary_hit in self.is_at_boundary():
            if boundary_hit in ['left', 'right']:
                self.setheading(180 - self.heading())
            if boundary_hit in ['top', 'bottom']:
                self.setheading(-self.heading())

    def move(self):
        self.forward(self.velocity)
        self.bounce_off_boundaries()

    def destroy(self):
        self.hideturtle()
        self.is_destroyed = True
        if self in Sprite.allSprites:
            Sprite.allSprites.remove(self)

    def update(self):
        pass


class SolidSprite(Sprite):
    allSprites = []

    def __init__(self, x, y, heading, shape, velocity):
        super().__init__(x, y, heading, shape, velocity)
        SolidSprite.allSprites.append(self)
        self.explosion_sound = None
        self.health = 0
        self.explosion_color = "white"

    def check_collisions(self):
        for sprite in SolidSprite.allSprites:
            if sprite != self:
                distX = self.xcor() - sprite.xcor()
                distY = self.ycor() - sprite.ycor()
                dist = sqrt(distX**2 + distY**2)
                if dist <= 15:
                    return True

    def explode(self):
        if self.explosion_sound:
            mixer.Sound(self.explosion_sound).play()
        for i in range(100):
            ExplosiveParticle(self.xcor(), self.ycor(), choice(config.PLAYER_EXPLOSION_COLORS))

    def destroy(self):
        super().destroy()
        if self in SolidSprite.allSprites:
            SolidSprite.allSprites.remove(self)

    def update(self):
        self.move()
        self.check_collisions()


class Player(SolidSprite):
    def __init__(self):
        super().__init__(
            x=config.PLAYER_INIT_POSX,
            y=config.PLAYER_INIT_POSY,
            heading=config.PLAYER_INIT_HEADING,
            shape=config.PLAYER_INIT_SHAPE,
            velocity=config.PLAYER_INIT_VELOCITY
        )
        self.left_limit = 145
        self.right_limit = 145
        self.points= config.PLAYER_INIT_POINTS
        self.health = config.PLAYER_HEALTH_POINTS
        self.explosion_sound = config.PLAYER_EXPLOSION_SOUND

    def move_left(self):
        self.goto(self.xcor()-20,self.ycor())

    def move_right(self):
        self.goto(self.xcor()+20,self.ycor())

    def fire(self):
        if len(BarEnemy.my_bar_enemy) == 1:
            if not self.is_destroyed and len(Ball.balls) == 0:
                shooting_range = list(range(-60,-20)) + list(range(20,60))
                Ball(
                    x=self.xcor(),
                    y=self.ycor(),
                    heading=90 + choice(shooting_range),
                    velocity=self.velocity
                )
        elif len(BarEnemy.my_bar_enemy) == 0:
            if self.health >0:
                Missile(
                    x = self.xcor(),
                    y = self.ycor(),
                    heading = 90,
                    velocity = config.MISSILE_ADDED_VELOCITY
                )

    def destroy(self):
        super().destroy()
        self.explode()

    def update(self):
        super().update()
        if len(BarEnemy.my_bar_enemy) ==0:
            self.shape(config.PLAYER_END_SHAPE)
            self.left_limit = 60
            self.right_limit = 60
        if self.health <= 0:
            self.destroy()


class Ball(SolidSprite):
    balls = []
    def __init__(self, x, y, heading, velocity):
        super().__init__(
            x,
            y,
            heading,
            shape=config.BALL_IMAGE,
            velocity=velocity + config.BALL_ADDED_VELOCITY
        )
        self.sound_fire = mixer.Sound(config.BALL_SOUND_SHOOT)
        self.sound_fire.set_volume(0.2)
        self.sound_fire.play()
        Ball.balls.append(self)


    def destroy(self):
        super().destroy()
        if self in Ball.balls:
            Ball.balls.remove(self)

    def bounce_off_boundaries(self):
        for boundary_hit in self.is_at_boundary():
            if boundary_hit in ['left', 'right']:
                self.setheading(180 - self.heading())
            if boundary_hit in ['top', 'bottom']:
                if boundary_hit == 'top':
                    player.points +=1
                    self.destroy()
                if boundary_hit == "bottom":
                    player.health -= 10
                    self.destroy()

    def bounce_off_enemy(self):
        if (self.ycor() >= enemy.ycor()  and (self.xcor() < enemy.xcor()+ enemy.left_limit and self.xcor() > enemy.xcor() -enemy.right_limit)):
            self.setheading(-self.heading()) 
            self.shape(config.BALL_IMAGE_DOWN)

    def bounce_off_player(self):
        if (self.ycor() <= player.ycor()  and (self.xcor() < player.xcor()+ player.left_limit and self.xcor() > player.xcor() -player.right_limit)):
            self.setheading(-self.heading())
            self.shape(config.BALL_IMAGE_UP)

    def update_velocity(self):
        if player.points == 0:
            self.velocity = 20
        if player.points == 1:
            self.velocity = 25
        if player.points == 2:
            self.velocity = 30
        if player.points == 3:
            self.velocity = 45

    def move(self):
        self.update_velocity()
        self.forward(self.velocity)
        self.bounce_off_enemy()
        self.bounce_off_player()
        self.bounce_off_boundaries()


class Missile(SolidSprite):
    def __init__(self, x, y, heading, velocity):
        super().__init__(
            x,
            y,
            heading = 90,
            shape=config.MISSILE_SHAPE,
            velocity=velocity + config.MISSILE_ADDED_VELOCITY
        )
        self.sound_fire = mixer.Sound(config.MISSILE_SOUND_SHOOT)
        self.sound_fire.set_volume(0.5)
        self.sound_fire.play()
        #self.inflicts = [config.MISSILE_DAMAGE]
        #self.is_hurt_by = [config.ALIEN_TOUCH]


    def touch_boss(self):
        if (self.ycor() >= my_boss.ycor()  and (self.xcor() < my_boss.xcor()+ my_boss.left_limit and self.xcor() > my_boss.xcor() -my_boss.right_limit)):
            self.destroy()
            my_boss.health -= 10

    def move(self):
        self.forward(self.velocity)
        self.touch_boss()
        if self.is_at_boundary():
            self.destroy()


class Net(SolidSprite):
    def __init__(self, x, y, heading, velocity):
        super().__init__(
            x,
            y,
            heading = 270,
            shape=config.NET_SHAPE,
            velocity=config.NET_VELOCITY
        )
        self.sound_fire = mixer.Sound(config.NET_LAUNCH_SOUND)
        self.sound_fire.set_volume(0.5)
        self.sound_fire.play()
        #self.inflicts = [config.MISSILE_DAMAGE]
        #self.is_hurt_by = [config.ALIEN_TOUCH]


    def touch_player(self):
        if (self.ycor() <= player.ycor()  and (self.xcor() < player.xcor()+ player.left_limit and self.xcor() > player.xcor() -player.right_limit)):
            self.destroy()
            player.health -= 10

    def move(self):
        self.forward(self.velocity)
        self.touch_player()
        if self.is_at_boundary():
            self.destroy()


class BarEnemy(SolidSprite):
    my_bar_enemy = []
    def __init__(self):
        super().__init__(
            x=config.PLAYER_INIT_POSX,
            y=config.PLAYER_INIT_POSY *-1 -30,
            heading=config.PLAYER_INIT_HEADING,
            shape=config.BAR_ENEMY_SHAPE,
            velocity=config.PLAYER_INIT_VELOCITY
        )
        self.left_limit = 130
        self.right_limit = 130
        BarEnemy.my_bar_enemy.append(self)

    def move(self):
        if len(Ball.balls) == 0:
            return False
        ballpos = Ball.balls[0].xcor()
        if ballpos > self.xcor():
            self.setheading(0)
            if randint(1,100) > 20:
                self.forward(10)
            self.bounce_off_boundaries()
        if ballpos < self.xcor():
            self.setheading(180)
            if randint(1,100) > 20:
                self.forward(10)
            self.bounce_off_boundaries()

        self.update_status()

    def destroy(self):
        super().destroy()
        BarEnemy.my_bar_enemy.remove(self)
        global my_boss
        my_boss = BossEnemy()


    def update_status(self):
        if player.points >= 3:
            self.destroy()
            pass


class BossEnemy(SolidSprite):
    boss_list = []
    def __init__(self):
        super().__init__(
            x=config.BOSS_INIT_POSX,
            y=config.BOSS_INIT_POSY,
            heading=config.BOSS_INIT_HEADING,
            shape=config.BOSS_INIT_SHAPE,
            velocity=config.BOSS_INIT_VELOCITY
        )
        self.explosion_sound = config.BOSS_EXPLOSION_SOUND 
        self.left_limit = 90
        self.right_limit = 90
        self.down_limit = 50
        self.up_limit = 50
        self.health = config.BOSS_INIT_HEALTH
        self.health_step = config.BOSS_INIT_HEALTH/4
        BossEnemy.boss_list.append(self)


    def destroy(self):
        super().destroy()
        self.explode()

    def update_status(self):
        if self.health <= 0:
            self.destroy()


    def spit(self):
        Net(
            x = self.xcor(),
            y = self.ycor(),
            heading = -90,
            velocity = config.NET_VELOCITY
        )

    def pattern1(self):
        self.velocity = 5
        self.forward(10)
        self.bounce_off_boundaries()
        self.shape(config.BOSS_INIT_SHAPE)
        if randint(1,120) < 15:
            self.spit()
    
    def pattern2(self):
        self.velocity = 10
        self.forward(10)
        self.bounce_off_boundaries()
        self.shape(config.BOSS_LEVEL2)
        if randint(1,120) < 20:
            self.spit()

    def pattern3(self):
        self.velocity = 15
        self.forward(10)
        self.bounce_off_boundaries()
        self.shape(config.BOSS_LEVEL3)
        if randint(1,120) < 25:
            self.spit()

    def pattern4(self):
        self.velocity = 20
        self.forward(10)
        self.bounce_off_boundaries()
        self.shape(config.BOSS_LEVEL4)
        if randint(1,120) < 30:
            self.spit()

    def move(self):
        if self.health > config.BOSS_INIT_HEALTH - self.health_step:
            self.jump(self.xcor(), 150)
            self.pattern1()
        elif self.health > config.BOSS_INIT_HEALTH - self.health_step*2:
            self.jump(self.xcor(),90)
            self.pattern2()
        elif self.health > config.BOSS_INIT_HEALTH - self.health_step * 3:
            self.jump(self.xcor(), 50)
            self.pattern3()
        else:
            self.jump(self.xcor(), 0)
            self.pattern4()
        self.update_status()


class Star(Sprite):
    def __init__(self):
        super().__init__(
            x=randint(-config.SCREEN_SIZE/2, config.SCREEN_SIZE/2),
            y=randint(-config.SCREEN_SIZE/2, config.SCREEN_SIZE/2),
            heading=270,
            shape="circle",
            velocity=0
        )
        self.shapesize(0.1)

    def move(self):
        self.forward(self.velocity)
        if 'bottom' in self.is_at_boundary():
            self.sety(config.SCREEN_SIZE/2 - 20)

    def update(self):
        self.move()
        self.color(choice(config.BACKGROUND_STAR_COLORS))


class ExplosiveParticle(Sprite):
    def __init__(self, x, y, color):
        super().__init__(
            x,
            y,
            heading=randint(0, 360),
            shape="circle",
            velocity=10
        )
        self.color(color)
        self.shapesize(0.1)
        self.x0 = self.xcor()
        self.y0 = self.ycor()

    def move(self):
        self.forward(self.velocity)

    def update(self):
        self.move()
        if self.distance(self.x0, self.y0) > config.SCREEN_SIZE/4:
            self.destroy()


class MyScreen():
    def __init__(self):
        # SINCE THE __init__ function was too mong I broke it down to 4 functions
        # that I call here. So no difference overall. Just more organized
        self.init_screen()
        self.init_border()
        self.init_writer()
        self.init_music()

    def init_screen(self):
        self.screen = turtle.Screen()
        self.screen.setup(
            width=config.SCREEN_SIZE+config.MARGIN,
            height=config.SCREEN_SIZE+config.MARGIN+10,
            startx=630,
            starty=0
        )
        self.screen.tracer(0)
        self.screen.bgcolor(config.BACKGROUND_COLOR)
        self.screen.title(config.GAME_TITLE)
        for imageFile in listAllFilesIn(config.IMAGES_DIRECTORY, "gif"):
            self.screen.addshape(imageFile)

    def init_border(self):
        self.border = MyTurtle()
        self.border.color(config.BORDER_COLOR)
        self.border.pensize(3)
        self.border.hideturtle()
        self.border.jump(-config.SCREEN_SIZE/2, -config.SCREEN_SIZE/2)
        self.border.square(config.SCREEN_SIZE)

    def init_writer(self):
        # I CHANGED THE NAME info TO wirter
        self.writer = MyTurtle()
        self.writer.color(config.TEXT_COLOR)
        self.writer.hideturtle()

    def init_music(self):
        mixer.init()
        self.music = mixer.music
        self.music.load(config.GAME_MUSIC)
        self.music.set_volume(config.GAME_MUSIC_VOLUME)
        self.music.play(-1)

    def bind_events(self, events):
        self.screen.listen()
        for key in events:
            self.screen.onkeypress(events[key], key)
        # for (key, value) in events.items():
        #     self.screen.onkeypress(value, key)

    def update_info(self, trtl):
        if len(BossEnemy.boss_list) == 0:
            info_str = "X:{:+04} Sprites: {} Solids: {} PlayerPoints: {} Health: {}".format(
                int(trtl.xcor()),
                len(Sprite.allSprites),
                len(SolidSprite.allSprites),
                trtl.points,
                trtl.health
            )
        else:
            info_str = "X:{:+04} Sprites: {} Solids: {} PlayerPoints: {} Health: {} BossLife: {}".format(
                int(trtl.xcor()),
                len(Sprite.allSprites),
                len(SolidSprite.allSprites),
                trtl.points,
                trtl.health,
                my_boss.health
            )
        self.writer.clear()
        self.writer.jump(-config.SCREEN_SIZE/2, config.SCREEN_SIZE/2)
        self.writer.write(info_str, font=config.TEXT_FONT)



#################
# INSTATIATIONS #
#################
my_screen = MyScreen()
player = Player()
enemy = BarEnemy()
# we don't need to save enemies in a list anymore sicne they are stored in Sprite.allSprites
for i in range(150):
    Star()

my_screen.bind_events({
    "Left": player.move_left,
    "Right": player.move_right,
    "space": player.fire,
})


#############
# MAIN LOOP #
#############
while True:
    t0 = time()

    for sprite in Sprite.allSprites:
        sprite.update()

    my_screen.update_info(player)
    my_screen.screen.update()
    t1 = time()

    exe_time = t1 - t0
    if 1/config.FPS - exe_time > 0:
        sleep(1/config.FPS - exe_time)
