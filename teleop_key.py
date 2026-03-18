#!/usr/bin/env python3
import time, math, pygame, carla, numpy as np
#HOST, PORT = "127.0.0.1", 2000

HOST, PORT = "localhost", 2000
# speed limit < 20km/h
SPEED_LIMIT_KMH = 20.0
SPEED_LIMIT_MS  = SPEED_LIMIT_KMH / 3.6
GOV_MARGIN_MS   = 1.2   
GOV_TH_MIN      = 0.05  
GOV_TH_CUT      = 0.35  
GOV_KP_BRAKE    = 0.18  
GOV_BIAS_BRAKE  = 0.04  

# control tuning
THR_SLEW_UP     = 1.2  
THR_SLEW_DOWN   = 1.5  
BRK_SLEW_UP     = 3.5   
BRK_SLEW_DOWN   = 3.0  

STEER_RATE      = 2.8  
STEER_RETURN    = 4.0  

SOFTSTART_THR   = 0.28 
SOFTSTART_V_MAX = 4.0 

NONLIN_WEIGHT   = 0.55  
CAM_W, CAM_H    = 960, 540
CAM_FOV         = 100.0
CAM_PITCH       = -8.0
CAM_X, CAM_Y, CAM_Z = 1.2, 0.0, 1.3


def find_vehicle(world, timeout=10.0, interval=0.2):
    deadline = time.time() + timeout
    last_cnt = -1
    while time.time() < deadline:
        try:
            world.wait_for_tick(timeout=1.0)
        except Exception:
            pass
        actors = world.get_actors().filter("vehicle.*")
        if last_cnt != len(actors):

            print(f"[carla] vehicles detected: {len(actors)}")
            last_cnt = len(actors)
        for v in actors:
            if v.attributes.get("role_name", "") == "ego_vehicle":
                return v
        time.sleep(interval)
    return None


def spawn_front_camera(world, vehicle):
    bp = world.get_blueprint_library().find("sensor.camera.rgb")
    bp.set_attribute("image_size_x", str(CAM_W))
    bp.set_attribute("image_size_y", str(CAM_H))
    bp.set_attribute("fov", str(CAM_FOV))
    tf = carla.Transform(
        carla.Location(x=CAM_X, y=CAM_Y, z=CAM_Z),
        carla.Rotation(pitch=CAM_PITCH),
    )
    return world.spawn_actor(bp, tf, attach_to=vehicle)

def main():
    client = carla.Client(HOST, PORT); client.set_timeout(5.0)
    world  = client.get_world()

    veh = find_vehicle(world, timeout=15.0)
    if not veh:
        print("No vehicle found. Make sure ros2_native.py spawned the hero.")
        return

    #veh.set_autopilot(False)

    ctrl = carla.VehicleControl(throttle=0.0, brake=0.0, steer=0.0,
                                hand_brake=False, reverse=False)
    pygame.init()
    pygame.display.set_caption("CARLA Teleop + Front Camera (WASD)")
    screen = pygame.display.set_mode((CAM_W, CAM_H))
    clock = pygame.time.Clock()
    hud_font = pygame.font.SysFont("monospace", 18)

    cam_sensor = None
    latest = {"frame": None}
    try:
        cam_sensor = spawn_front_camera(world, veh)

        def _on_cam(image):
            arr = np.frombuffer(image.raw_data, dtype=np.uint8)
            arr = arr.reshape((image.height, image.width, 4))
            rgb = arr[:, :, :3][:, :, ::-1]  # BGRA -> RGB
            latest["frame"] = rgb.copy()

        cam_sensor.listen(_on_cam)
        print("[carla] front camera attached for teleop view")
    except Exception as e:
        print(f"[carla] front camera unavailable: {e}")
    
    th_cmd = 0.0
    br_cmd = 0.0
    st_cmd = 0.0

    def _speed_ms(v):  # m/s
        return math.sqrt(v.x*v.x + v.y*v.y + v.z*v.z)

    def _slew(curr, target, up, down, dt):
        rate = up if target > curr else down
        step = rate * dt
        if abs(target - curr) <= step:
            return target
        return curr + step * (1 if target > curr else -1)

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: 
                        return
                    if event.key == pygame.K_q: ctrl.reverse = True
                    if event.key == pygame.K_e: ctrl.reverse = False
                    if event.key == pygame.K_r: st_cmd = 0.0

            keys = pygame.key.get_pressed()

            dt = max(1e-3, clock.tick(60) / 1000.0)

            accel_pressed  = keys[pygame.K_w] or keys[pygame.K_UP]
            brake_pressed  = keys[pygame.K_s] or keys[pygame.K_DOWN]
            left_pressed   = keys[pygame.K_a] or keys[pygame.K_LEFT]
            right_pressed  = keys[pygame.K_d] or keys[pygame.K_RIGHT]
            ctrl.hand_brake = keys[pygame.K_SPACE]

            try:
                v_ms = _speed_ms(veh.get_velocity())
            except Exception:
                v_ms = 0.0

            want_thr = 0.0
            if accel_pressed and not brake_pressed:
                want_thr = 1.0
                if v_ms < SOFTSTART_V_MAX:
                    k = 1.0 - (v_ms / SOFTSTART_V_MAX)
                    want_thr = max(want_thr * (1.0 - 0.25*k), SOFTSTART_THR)

            want_brk = 1.0 if brake_pressed else 0.0

            th_cmd = _slew(th_cmd, want_thr, THR_SLEW_UP, THR_SLEW_DOWN, dt)
            br_cmd = _slew(br_cmd, want_brk, BRK_SLEW_UP, BRK_SLEW_DOWN, dt)

            if br_cmd > 0.05:
                th_cmd = max(0.0, th_cmd - 3.0*dt)

            if left_pressed and not right_pressed:
                target_st = -1.0
            elif right_pressed and not left_pressed:
                target_st = 1.0
            else:
                if abs(st_cmd) < STEER_RETURN*dt:
                    target_st = 0.0
                else:
                    target_st = st_cmd - STEER_RETURN*dt * (1 if st_cmd > 0 else -1)

            st_cmd = _slew(st_cmd, target_st, STEER_RATE, STEER_RATE, dt)

            if v_ms < 15.0:
                st_limit = 1.0 - 0.65*(v_ms/15.0)  
            elif v_ms < 25.0:
                st_limit = 0.35 - 0.10*((v_ms-15.0)/10.0) 
            else:
                st_limit = 0.25
            st_cmd = max(-st_limit, min(st_limit, st_cmd))

            steer_out = (1.0 - NONLIN_WEIGHT)*st_cmd + NONLIN_WEIGHT*(st_cmd**3)

            if v_ms >= (SPEED_LIMIT_MS - GOV_MARGIN_MS):
                approach = min(1.0, max(0.0, (v_ms - (SPEED_LIMIT_MS - GOV_MARGIN_MS)) / GOV_MARGIN_MS))
                th_cmd = max(GOV_TH_MIN, th_cmd * (GOV_TH_CUT + (1.0 - GOV_TH_CUT) * (1.0 - approach)))

            if v_ms > SPEED_LIMIT_MS:
                overshoot = v_ms - SPEED_LIMIT_MS
                th_cmd = 0.0
                br_cmd = max(br_cmd, min(1.0, GOV_KP_BRAKE * overshoot + GOV_BIAS_BRAKE))

            ctrl.throttle = max(0.0, min(1.0, th_cmd))
            ctrl.brake    = max(0.0, min(1.0, br_cmd))
            ctrl.steer    = max(-1.0, min(1.0, steer_out))
            veh.apply_control(ctrl)

            txt = f"v:{v_ms:4.1f} T:{ctrl.throttle:.2f} B:{ctrl.brake:.2f} S:{ctrl.steer:.2f} Rev:{int(ctrl.reverse)} HB:{int(ctrl.hand_brake)}"
            pygame.display.set_caption(txt)

            frame = latest["frame"]
            if frame is not None:
                surf = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                screen.blit(surf, (0, 0))
            else:
                screen.fill((20, 20, 20))
                wait = hud_font.render("Waiting for front camera frames...", True, (220, 220, 220))
                screen.blit(wait, (24, 20))

            hud = hud_font.render(txt, True, (255, 255, 255))
            hud_bg = pygame.Surface((CAM_W, 28), pygame.SRCALPHA)
            hud_bg.fill((0, 0, 0, 130))
            screen.blit(hud_bg, (0, CAM_H - 28))
            screen.blit(hud, (8, CAM_H - 24))
            pygame.display.flip()

            clock.tick(30)
    finally:
        if cam_sensor is not None:
            try:
                cam_sensor.stop()
            except Exception:
                pass
            try:
                cam_sensor.destroy()
            except Exception:
                pass
        pygame.quit()

if __name__ == "__main__":
    main()
