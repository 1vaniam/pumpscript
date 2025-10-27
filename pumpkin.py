import minescript as mine  # type: ignore
import time
import random
import rotate
import threading
from minescript_plus import Util

start_x = mine.player_position()

random_time = [18.7, 18]
hold_time = random.choice(random_time)

loops = 63
target_yaw = 90.0
target_pitch = -57.0
next_loop = 5.0
tolerance = 12.0
stuck_limit = 8.0
last_position = start_x
lastmove_time = time.time()

safe_tp = False
sudden_threshold = 5.0

chat_options = ["hello", "ayo", "hi po", "wut", "bat ako natp", "huh"]
look_random = random.uniform(0.5, 1.0)
message = random.choice(chat_options)

mine.echo(f"Start position recorded at: {start_x}")


def safe_sleep(duration):
    global running
    start = time.time()
    while running and (time.time() - start) < duration:
        time.sleep(0.05)

def stuck():
    global last_position, lastmove_time, running

    while running:
        pos_now = mine.player_position()

        if abs(pos_now[0] - last_position[0]) > 0.2 or abs(pos_now[2] - last_position[2]) > 0.2:
            last_position = pos_now
            lastmove_time = time.time()

        if time.time() - lastmove_time > stuck_limit:
            mine.echo("bro is stuck, stopping")
            mine.player_press_attack(False)
        
            mine.player_press_forward(False)
            time.sleep(0.1)

            mine.player_press_right(False)
            time.sleep(0.1)

            mine.player_press_left(False)
            time.sleep(0.1)

            mine.player_press_attack(False)
        

            mine.chat(message)
            running = False
            for _ in range(1):
                rotate.look_at_random_block()
                time.sleep(look_random)
            mine.execute("\suspend")

            break
        safe_sleep(1)


def tp_detect():

    global running

    while running:
        x = mine.player_position()

        if abs(x[0] - start_x[0]) > tolerance:
            mine.player_press_attack(False)
            mine.echo("gumalaw ka boi")

            mine.player_press_forward(False)
            time.sleep(0.1)

            mine.player_press_right(False)
            time.sleep(0.1)

            mine.player_press_left(False)
            time.sleep(0.1)

            mine.player_press_attack(False)
        

            mine.chat(message)
            running = False
            for _ in range(1):
                rotate.look_at_random_block()
                time.sleep(look_random)
            mine.execute("\suspend")

            break

        safe_sleep(1)

def sudden_move():

    global running, safe_tp
    prev = mine.player_position()

    while running:
        safe_sleep(0.2)
        now = mine.player_position()
        dx = abs(now[0] - prev[0])
        dy = abs(now[1] - prev[1])
        dz = abs(now[2] - prev[2])

        if safe_tp == True:
            prev = now
            continue

        if dx > sudden_threshold or dy > sudden_threshold or dz > sudden_threshold:
            mine.echo(f"bro got tped")

            mine.player_press_attack(False)
            mine.echo("gumalaw ka boi")

            mine.player_press_forward(False)
            safe_sleep(0.1)

            mine.player_press_right(False)
            safe_sleep(0.1)

            mine.player_press_left(False)
            safe_sleep(0.1)

            mine.player_press_attack(False)

            mine.chat("whut")
            safe_sleep(1.5)
            mine.chat("kanina pa to ah")
            safe_sleep(0.5)

            for _ in range(2):
                rotate.look_at_random_block()
                safe_sleep(look_random)

            mine.execute("/home pump")
            running = False
            mine.execute("\suspend")
            break

        prev = now
            

def farm_loop():
    global running, safe_tp

    while running:
        mine.player_set_orientation(target_yaw, target_pitch)
        mine.player_press_forward(True)
        mine.player_press_attack(True)

        for i in range(loops):
            if not running:
                break

            mine.player_press_right(True)
            safe_sleep(hold_time)
            safe_sleep(0.1)
            mine.player_press_right(False)

            mine.player_press_left(True)
            safe_sleep(hold_time)
            safe_sleep(0.2)
            mine.player_press_left(False)

            
            mine.player_press_forward(True)
            mine.echo(f"LOOOOOOOOOOOOOOOP numba: {i + 1}")

            if (i + 1) % 3 == 0:
                mine.execute("/sellall PUMPKIN")
                mine.echo(f"sold pumpkin: {i + 1} times")

        safe_tp = True

        mine.player_press_forward(False)
        mine.echo("FINISHED LOOPING")
        mine.execute("/home pump")

        safe_sleep(5.0)
        safe_tp = False
        
        safe_sleep(next_loop)

running = True

tp_thread = threading.Thread(target=tp_detect, daemon=True)
stuck_thread = threading.Thread(target=stuck, daemon=True)
sudden_thread = threading.Thread(target=sudden_move, daemon=True)

tp_thread.start()
stuck_thread.start()
sudden_thread.start()


farm_loop()

mine.echo("Script finished")
