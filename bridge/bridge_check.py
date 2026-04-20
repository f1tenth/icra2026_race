#!/usr/bin/env python3
# bridge_check.py
# Created by Samir Shehadeh and Claude for 27th Roboracer Autonomous Racing Competition.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Polygon
from pathlib import Path

# ============================================================
# User-provided car geometry
# ============================================================
WB = 0.36  # wheelbase [m], axle-center to axle-center
R = 0.05  # wheel radius [m]
FLOOR_H = 0.02  # chassis floor height above local ground [m]
BUMPER_H = 0.025  # lowest point of front bumper above local ground [m]
BUMPER_LEN = 0.10  # bumper extends ahead of front axle [m]

# Drawing-only body height
BODY_TOP_H = 0.06  # above local ground on flat, for visualization

# Bridge geometry
ANGLE_DEG = 7.2
ANGLE = np.deg2rad(ANGLE_DEG)
M = np.tan(ANGLE)
BRIDGE_H = 0.5  # bridge height [m]
RAMP_RUN = BRIDGE_H / M        # horizontal run of each ramp [m]
RAMP_SLANT = BRIDGE_H / np.sin(ANGLE)  # slant length along ramp face [m]
TOP_LEN = 2.5  # flat top length [m]
CLEARANCE_MIN = 0.30  # clearance threshold to mark [m]

# Bridge x-locations
X_UP_START = 0.0
X_UP_END = X_UP_START + RAMP_RUN
Y_TOP = BRIDGE_H
X_TOP_END = X_UP_END + TOP_LEN
X_DOWN_END = X_TOP_END + RAMP_RUN

# ============================================================
# Vehicle local geometry
# Local frame origin = rear wheel center
# Local y=0 is axle-center height, so ground on flat is y=-R
# ============================================================
rear_wc_local = np.array([0.0, 0.0])
front_wc_local = np.array([WB, 0.0])

floor_y_local = FLOOR_H - R
body_top_y_local = BODY_TOP_H - R
bumper_tip_y_local = BUMPER_H - R

body_poly_local = np.array(
    [
        [0.0, floor_y_local],
        [WB, floor_y_local],
        [WB, body_top_y_local],
        [0.0, body_top_y_local],
    ]
)

bumper_poly_local = np.array(
    [
        [WB, floor_y_local],  # rear bottom: flush with floor
        [WB + BUMPER_LEN, bumper_tip_y_local],  # front bottom: bumper tip
        [WB + BUMPER_LEN, bumper_tip_y_local + 0.012],  # front top: tip + thickness
        [WB, floor_y_local + 0.015],  # rear top
    ]
)

# Important lower-surface points for annotation/checking
floor_mid_local = np.array([[WB / 2.0, floor_y_local]])
bumper_low_local = np.array([[WB + BUMPER_LEN, bumper_tip_y_local]])


# ============================================================
# Math helpers
# ============================================================
def rot(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s], [s, c]])


def transform(points, angle, translation):
    pts = np.atleast_2d(points)
    return pts @ rot(angle).T + np.asarray(translation)


def wheel_center_from_contact(contact_xy, road_angle, radius):
    """Offset contact point by road normal to get wheel center."""
    n = np.array([-np.sin(road_angle), np.cos(road_angle)])
    return np.asarray(contact_xy) + radius * n


def signed_height_to_line(point, line_point, line_angle):
    """Signed distance in the line's upward normal direction."""
    t = np.array([np.cos(line_angle), np.sin(line_angle)])
    n = np.array([-t[1], t[0]])
    return float(np.dot(np.asarray(point) - np.asarray(line_point), n))


# ============================================================
# Bridge profiles
# ============================================================
def bridge_sharp(x):
    x = np.asarray(x)
    y = np.empty_like(x, dtype=float)

    m1 = x <= X_UP_START
    m2 = (x > X_UP_START) & (x <= X_UP_END)
    m3 = (x > X_UP_END) & (x <= X_TOP_END)
    m4 = (x > X_TOP_END) & (x <= X_DOWN_END)
    m5 = x > X_DOWN_END

    y[m1] = 0.0
    y[m2] = M * (x[m2] - X_UP_START)
    y[m3] = Y_TOP
    y[m4] = Y_TOP - M * (x[m4] - X_TOP_END)
    y[m5] = 0.0
    return y


# ============================================================
# Pose solvers for the four requested situations
# ============================================================
def pose_starting_up(front_contact_x):
    """
    Situation 1: car starting to go up the ramp.
    Rear wheel on flat, front wheel on up-ramp.
    """
    front_contact = np.array([front_contact_x, M * (front_contact_x - X_UP_START)])
    cf = wheel_center_from_contact(front_contact, ANGLE, R)

    # Rear wheel center lies on flat ground at y = R
    dy = cf[1] - R
    dx = np.sqrt(max(WB**2 - dy**2, 0.0))
    cr = np.array([cf[0] - dx, R])

    angle = np.arctan2(cf[1] - cr[1], cf[0] - cr[0])
    return {"angle": angle, "t": cr}


def pose_top_crest(front_contact_x):
    """
    Situation 2: car at the top, transition from 15° up to flat.
    Rear wheel on up-ramp, front wheel on flat top.
    """
    cf = np.array([front_contact_x, Y_TOP + R])

    def f(xr):
        rear_contact = np.array([xr, M * (xr - X_UP_START)])
        cr = wheel_center_from_contact(rear_contact, ANGLE, R)
        return np.linalg.norm(cf - cr) - WB

    xs = np.linspace(X_UP_END - 1.0, X_UP_END + 0.2, 7000)
    vals = np.array([f(xx) for xx in xs])
    idx = np.where(np.sign(vals[:-1]) != np.sign(vals[1:]))[0]
    if len(idx) == 0:
        raise RuntimeError("No solution found for top crest pose")
    a, b = xs[idx[0]], xs[idx[0] + 1]
    for _ in range(80):
        mid = 0.5 * (a + b)
        if f(a) * f(mid) <= 0:
            b = mid
        else:
            a = mid
    xr = 0.5 * (a + b)
    rear_contact = np.array([xr, M * (xr - X_UP_START)])
    cr = wheel_center_from_contact(rear_contact, ANGLE, R)
    angle = np.arctan2(cf[1] - cr[1], cf[0] - cr[0])
    return {"angle": angle, "t": cr}


def pose_flat_to_down(rear_center_x):
    """
    Situation 3: car at start of descent, transition from flat top to 15° down.
    Rear wheel still on flat top, front wheel already on down-ramp.
    """
    cr = np.array([rear_center_x, Y_TOP + R])

    def f(xf):
        front_contact = np.array([xf, Y_TOP - M * (xf - X_TOP_END)])
        cf = wheel_center_from_contact(front_contact, -ANGLE, R)
        return np.linalg.norm(cf - cr) - WB

    xs = np.linspace(X_TOP_END - 0.1, X_DOWN_END + 0.5, 7000)
    vals = np.array([f(xx) for xx in xs])
    idx = np.where(np.sign(vals[:-1]) != np.sign(vals[1:]))[0]
    if len(idx) == 0:
        raise RuntimeError("No solution found for flat-to-down pose")
    a, b = xs[idx[0]], xs[idx[0] + 1]
    for _ in range(80):
        mid = 0.5 * (a + b)
        if f(a) * f(mid) <= 0:
            b = mid
        else:
            a = mid
    xf = 0.5 * (a + b)
    front_contact = np.array([xf, Y_TOP - M * (xf - X_TOP_END)])
    cf = wheel_center_from_contact(front_contact, -ANGLE, R)
    angle = np.arctan2(cf[1] - cr[1], cf[0] - cr[0])
    return {"angle": angle, "t": cr}


def pose_down_to_floor(front_contact_x):
    """
    Situation 4: car leaving the bridge, transition from 15° down back to floor.
    Rear wheel on down-ramp, front wheel on flat floor.
    """
    cf = np.array([front_contact_x, R])

    def f(xr):
        rear_contact = np.array([xr, Y_TOP - M * (xr - X_TOP_END)])
        cr = wheel_center_from_contact(rear_contact, -ANGLE, R)
        return np.linalg.norm(cf - cr) - WB

    xs = np.linspace(X_DOWN_END - 1.0, X_DOWN_END + 0.2, 7000)
    vals = np.array([f(xx) for xx in xs])
    idx = np.where(np.sign(vals[:-1]) != np.sign(vals[1:]))[0]
    if len(idx) == 0:
        raise RuntimeError("No solution found for down-to-floor pose")
    a, b = xs[idx[0]], xs[idx[0] + 1]
    for _ in range(80):
        mid = 0.5 * (a + b)
        if f(a) * f(mid) <= 0:
            b = mid
        else:
            a = mid
    xr = 0.5 * (a + b)
    rear_contact = np.array([xr, Y_TOP - M * (xr - X_TOP_END)])
    cr = wheel_center_from_contact(rear_contact, -ANGLE, R)
    angle = np.arctan2(cf[1] - cr[1], cf[0] - cr[0])
    return {"angle": angle, "t": cr}


def pose_flat_ground():
    """
    Situation 5: car on flat ground.
    """
    return {"angle": 0.0, "t": np.array([0.0, R])}


def pose_approach_ramp():
    """
    Approach pose: both wheels on flat ground, front wheel contact
    exactly at the ramp entry corner (x = X_UP_START).
    This is the critical moment for bumper-vs-ramp-face scrape.
    """
    cf = np.array([X_UP_START, R])  # front wheel center at entry corner
    cr = np.array([X_UP_START - WB, R])
    return {"angle": 0.0, "t": cr}


def pose_approach_exit():
    """
    Symmetric exit pose: both wheels on the down-ramp, front wheel contact
    exactly at the exit corner (x = X_DOWN_END).
    This is the critical moment for bumper-vs-flat-ground scrape on descent.
    """
    front_contact = np.array([X_DOWN_END, 0.0])
    cf = wheel_center_from_contact(front_contact, -ANGLE, R)
    # rear wheel center: WB behind along the -ANGLE direction
    cr = cf - WB * np.array([np.cos(-ANGLE), np.sin(-ANGLE)])
    return {"angle": -ANGLE, "t": cr}


# ============================================================
# Build poses (0=flat ref, 0b=entry approach, 1..4=transitions, 0c=exit approach)
# ============================================================
pose0b = pose_approach_ramp()
pose0c = pose_approach_exit()
pose1 = pose_starting_up(front_contact_x=0.12)
pose2 = pose_top_crest(front_contact_x=X_UP_END + 0.12)
pose3 = pose_flat_to_down(rear_center_x=X_TOP_END - 0.12)
pose4 = pose_down_to_floor(front_contact_x=X_DOWN_END + 0.03)
pose5 = pose_flat_ground()


# ============================================================
# Clearance checks against sharp local transitions
# ============================================================
def transformed_critical_points(pose):
    floor_mid = transform(floor_mid_local, pose["angle"], pose["t"])[0]
    bumper_low = transform(bumper_low_local, pose["angle"], pose["t"])[0]
    return floor_mid, bumper_low


checks = {}

# Situation 1: sharp corner at start
floor1, bumper1 = transformed_critical_points(pose1)
checks["start_up_floor"] = signed_height_to_line(floor1, [X_UP_START, 0.0], ANGLE)
checks["start_up_bumper"] = signed_height_to_line(bumper1, [X_UP_START, 0.0], ANGLE)

# Situation 2: up to top crest
floor2, bumper2 = transformed_critical_points(pose2)
checks["top_crest_floor_ramp"] = signed_height_to_line(floor2, [X_UP_START, 0.0], ANGLE)
checks["top_crest_floor_top"] = signed_height_to_line(floor2, [X_UP_END, Y_TOP], 0.0)
checks["top_crest_bumper_ramp"] = signed_height_to_line(bumper2, [X_UP_START, 0.0], ANGLE)
checks["top_crest_bumper_top"] = signed_height_to_line(bumper2, [X_UP_END, Y_TOP], 0.0)

# Situation 3: top to down crest
floor3, bumper3 = transformed_critical_points(pose3)
checks["down_crest_floor_top"] = signed_height_to_line(floor3, [X_TOP_END, Y_TOP], 0.0)
checks["down_crest_floor_down"] = signed_height_to_line(floor3, [X_TOP_END, Y_TOP], -ANGLE)
checks["down_crest_bumper_top"] = signed_height_to_line(bumper3, [X_TOP_END, Y_TOP], 0.0)
checks["down_crest_bumper_down"] = signed_height_to_line(bumper3, [X_TOP_END, Y_TOP], -ANGLE)

# Situation 4: down to floor exit
floor4, bumper4 = transformed_critical_points(pose4)
checks["exit_floor_down"] = signed_height_to_line(floor4, [X_TOP_END, Y_TOP], -ANGLE)
checks["exit_bumper_down"] = signed_height_to_line(bumper4, [X_TOP_END, Y_TOP], -ANGLE)


# ============================================================
# Scrape detection
# ============================================================
def _build_underside_local(n=300):
    """Dense sample of points along the car's entire underside in local frame."""
    # Floor bottom: rear axle to front axle
    xs_floor = np.linspace(0.0, WB, n // 2)
    floor_pts = np.column_stack([xs_floor, np.full(n // 2, floor_y_local)])
    # Bumper lower edge: from floor height at the front face down to bumper tip
    ts = np.linspace(0.0, 1.0, n // 2)
    bx = WB + ts * BUMPER_LEN
    by = floor_y_local + ts * (bumper_tip_y_local - floor_y_local)
    bumper_pts = np.column_stack([bx, by])
    return np.vstack([floor_pts, bumper_pts])


_UNDERSIDE_LOCAL = _build_underside_local()


# Sharp corners of the bridge that can poke up into the car belly
_BRIDGE_CORNERS = [
    (X_UP_START, 0.0),
    (X_UP_END, Y_TOP),
    (X_TOP_END, Y_TOP),
    (X_DOWN_END, 0.0),
]


def _underside_y_local(lx):
    """Car underside y in local frame at local x. Returns None if outside footprint."""
    if 0.0 <= lx <= WB:
        return floor_y_local
    if WB < lx <= WB + BUMPER_LEN:
        t = (lx - WB) / BUMPER_LEN
        return floor_y_local + t * (bumper_tip_y_local - floor_y_local)
    return None


def find_scrape_points(pose):
    """
    Return (car_pts, bridge_pts, depth) where the car underside penetrates the
    bridge surface, or None if no contact.

    Two checks:
    1. Surface check: sample car underside vs bridge_sharp height (catches ramp-face hits).
    2. Corner check: each sharp bridge corner tested against car underside in local frame
       (catches convex-crest belly scrapes that the surface sample misses).
    """
    a = pose["angle"]
    t = pose["t"]
    ca, sa = np.cos(a), np.sin(a)
    R_inv = np.array([[ca, sa], [-sa, ca]])

    # --- 1. surface check ---
    car_pts = transform(_UNDERSIDE_LOCAL, a, t)
    bridge_y = bridge_sharp(car_pts[:, 0])
    depth_s = bridge_y - car_pts[:, 1]
    mask = depth_s > 1e-4

    # --- 2. corner check ---
    extra_car, extra_bridge, extra_depth = [], [], []
    for xc, yc in _BRIDGE_CORNERS:
        local = R_inv @ (np.array([xc, yc]) - t)
        lx, ly = local
        us_y = _underside_y_local(lx)
        if us_y is None:
            continue
        d = ly - us_y  # positive = corner pokes above underside = into car
        if d > 1e-4:
            world_us = transform(np.array([[lx, us_y]]), a, t)[0]
            extra_car.append(world_us)
            extra_bridge.append(np.array([xc, yc]))
            extra_depth.append(d)

    # --- combine ---
    if not np.any(mask) and not extra_car:
        return None

    all_car, all_bridge, all_depth = [], [], []
    if np.any(mask):
        all_car.append(car_pts[mask])
        all_bridge.append(np.column_stack([car_pts[mask, 0], bridge_y[mask]]))
        all_depth.append(depth_s[mask])
    if extra_car:
        all_car.append(np.array(extra_car))
        all_bridge.append(np.array(extra_bridge))
        all_depth.append(np.array(extra_depth))

    return np.vstack(all_car), np.vstack(all_bridge), np.concatenate(all_depth)


# ============================================================
# Plot helper
# ============================================================
def draw_car(ax, pose, color="black", label=None, annotate=False):
    body = transform(body_poly_local, pose["angle"], pose["t"])
    bumper = transform(bumper_poly_local, pose["angle"], pose["t"])
    rear_wc = transform(rear_wc_local, pose["angle"], pose["t"])[0]
    front_wc = transform(front_wc_local, pose["angle"], pose["t"])[0]

    kw = dict(edgecolor=color, fill=False, linewidth=1.8, zorder=4)
    ax.add_patch(Polygon(body, **kw))
    ax.add_patch(Polygon(bumper, **kw))
    ax.add_patch(Circle(rear_wc, R, **kw))
    ax.add_patch(Circle(front_wc, R, **kw))

    # Label above car body
    if label:
        ax.text(
            body[:, 0].mean(),
            body[:, 1].max() + 0.025,
            label,
            color=color,
            fontsize=7.5,
            ha="center",
            va="bottom",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=color, alpha=0.85),
            zorder=6,
        )

    # Scrape zone visualization
    scrape = find_scrape_points(pose)
    if scrape is not None:
        car_pts, bridge_pts, depth = scrape
        ax.plot(car_pts[:, 0], car_pts[:, 1], color="red", linewidth=4, zorder=7, solid_capstyle="round")
        ax.fill_between(car_pts[:, 0], car_pts[:, 1], bridge_pts[:, 1], color="red", alpha=0.30, zorder=6)
        idx_max = np.argmax(depth)
        ax.annotate(
            f"SCRAPE\n{depth[idx_max]*1000:.1f} mm",
            xy=bridge_pts[idx_max],
            xytext=(bridge_pts[idx_max, 0] + 0.05, bridge_pts[idx_max, 1] + 0.12),
            arrowprops=dict(arrowstyle="->", color="red"),
            fontsize=7.5,
            color="red",
            fontweight="bold",
            zorder=8,
        )

    if annotate:
        floor_mid = transform(floor_mid_local, pose["angle"], pose["t"])[0]
        bumper_low = transform(bumper_low_local, pose["angle"], pose["t"])[0]
        ax.plot(floor_mid[0], floor_mid[1], marker="s", markersize=5, color=color, zorder=5)
        ax.plot(bumper_low[0], bumper_low[1], marker="o", markersize=5, color=color, zorder=5)


# ============================================================
# Single combined plot: one bridge, all 5 cars
# ============================================================
out_dir = Path(".")

MARGIN = 0.55
FULL_XLIM = (X_UP_START - MARGIN, X_DOWN_END + MARGIN)
FULL_YLIM = (-0.12, BRIDGE_H + 0.44)


# Pose 0 = flat ground reference, parked just before the ramp
flat_ref_pose = {"angle": 0.0, "t": np.array([X_UP_START - 0.42, R])}
all_poses = [flat_ref_pose, pose0b, pose1, pose2, pose3, pose4, pose0c]
car_labels = [
    "0) flat ground\n(reference)",
    "0b) entry approach\nbumper vs ramp",
    "1) front on ramp\nrear on floor",
    "2) top crest\nrear↗ front→",
    "3) flat→down crest\nrear→ front↘",
    "4) leaving bridge\nrear↘ front→",
    "0c) exit approach\nbumper vs floor",
]
COLORS = ["#2ca02c", "#e377c2", "#1f77b4", "#ff7f0e", "#9467bd", "#8c564b", "#d62728"]

fig, ax = plt.subplots(figsize=(24, 7))

# ---- draw bridge once ----
x = np.linspace(FULL_XLIM[0], FULL_XLIM[1], 4000)
ys = bridge_sharp(x)
ax.fill_between(x, ys, -0.12, color="#cdd8ea", alpha=0.7, zorder=0)
ax.plot(x, ys, color="steelblue", linewidth=2.5, label="bridge", zorder=1)
ax.axhline(0, color="steelblue", linewidth=1, linestyle=":", alpha=0.4, zorder=0)

# ---- 30 cm clearance band ----
# On each ramp, find x where the bridge surface is exactly CLEARANCE_MIN high.
#   up-ramp:   y = M*(x - X_UP_START)  →  x_30_start = X_UP_START + CLEARANCE_MIN / M
#   down-ramp: y = BRIDGE_H - M*(x - X_TOP_END)  →  x_30_end = X_TOP_END + (BRIDGE_H - CLEARANCE_MIN) / M
x_30_start = X_UP_START + CLEARANCE_MIN / M
x_30_end   = X_TOP_END  + (BRIDGE_H - CLEARANCE_MIN) / M
len_30 = x_30_end - x_30_start

# green shaded band: ground (y=0) to clearance threshold, only where bridge ≥ CLEARANCE_MIN
x_band = np.linspace(x_30_start, x_30_end, 500)
ax.fill_between(x_band, 0, CLEARANCE_MIN,
                color="#2ca02c", alpha=0.18, zorder=1, label=f"≥{CLEARANCE_MIN*100:.0f} cm clearance")
# dashed threshold line under the bridge
ax.hlines(CLEARANCE_MIN, x_30_start, x_30_end,
          colors="#2ca02c", linewidths=1.4, linestyles="--", zorder=3)
# vertical markers at the transition points
for xv in (x_30_start, x_30_end):
    ax.vlines(xv, 0, CLEARANCE_MIN, colors="#2ca02c", linewidths=1.0, linestyles=":", zorder=3)
    ax.plot(xv, CLEARANCE_MIN, marker="o", markersize=5, color="#2ca02c", zorder=4)

# span arrow just below ground level
_cl_arr_y = -0.07
ax.annotate("", xy=(x_30_end, _cl_arr_y), xytext=(x_30_start, _cl_arr_y),
            arrowprops=dict(arrowstyle="<->", color="#2ca02c", lw=1.2))
ax.text((x_30_start + x_30_end) / 2, _cl_arr_y - 0.035,
        f"{len_30:.3f} m  (≥{CLEARANCE_MIN*100:.0f} cm clearance)",
        ha="center", va="top", fontsize=8, color="#2ca02c", fontweight="bold")

# vertical arrow showing the 30 cm height at the entry transition
ax.annotate("", xy=(x_30_start, CLEARANCE_MIN), xytext=(x_30_start, 0.0),
            arrowprops=dict(arrowstyle="<->", color="#2ca02c", lw=1.0))
ax.text(x_30_start - 0.04, CLEARANCE_MIN / 2,
        f"{CLEARANCE_MIN*100:.0f} cm", ha="right", va="center", fontsize=7.5, color="#2ca02c")

# dimension arrows
ann_y = BRIDGE_H + 0.20
arrow_kw = dict(arrowstyle="<->", color="dimgray", lw=1.0)
for xa, xb, lbl in [
    (X_UP_START, X_UP_END, f"run  {RAMP_RUN:.3f} m"),
    (X_UP_END, X_TOP_END, f"top  {TOP_LEN:.2f} m"),
    (X_TOP_END, X_DOWN_END, f"run  {RAMP_RUN:.3f} m"),
]:
    ax.annotate("", xy=(xb, ann_y), xytext=(xa, ann_y), arrowprops=arrow_kw)
    ax.text((xa + xb) / 2, ann_y + 0.04, lbl, ha="center", va="bottom", fontsize=8, color="dimgray")
ax.annotate("", xy=(FULL_XLIM[0] + 0.12, BRIDGE_H), xytext=(FULL_XLIM[0] + 0.12, 0.0), arrowprops=arrow_kw)
ax.text(FULL_XLIM[0] + 0.15, BRIDGE_H / 2, f"h={BRIDGE_H:.2f} m", va="center", fontsize=8, color="dimgray")

# slant length arrows — offset below/above each ramp face by a small perpendicular distance
_slant_off = 0.10
_perp_up   = np.array([ np.sin(ANGLE), -np.cos(ANGLE)]) * _slant_off   # below up-ramp
_perp_down = np.array([-np.sin(ANGLE),  np.cos(ANGLE)]) * _slant_off   # below down-ramp
for (px, py), (qx, qy), perp, side in [
    ((X_UP_START,  0.0),   (X_UP_END,   Y_TOP), _perp_up,   "up"),
    ((X_TOP_END,   Y_TOP), (X_DOWN_END, 0.0),   _perp_down, "down"),
]:
    p0 = np.array([px, py]) + perp
    p1 = np.array([qx, qy]) + perp
    ax.annotate("", xy=(p1[0], p1[1]), xytext=(p0[0], p0[1]), arrowprops=arrow_kw)
    mid = (p0 + p1) / 2 + perp * 0.9
    ax.text(mid[0], mid[1], f"slant  {RAMP_SLANT:.3f} m", ha="center", va="center",
            fontsize=8, color="dimgray",
            rotation=np.rad2deg(ANGLE if side == "up" else -ANGLE))

# angle arcs at the four ramp corners
_arc_r = 0.18
for xc, yc, theta1, theta2 in [
    (X_UP_START,  0.0,   0,            ANGLE_DEG),        # entry base: 0°→angle
    (X_UP_END,    Y_TOP, 180,          180 + ANGLE_DEG),  # top-crest up: ramp meets flat
    (X_TOP_END,   Y_TOP, 180 - ANGLE_DEG, 180),           # top-crest down
    (X_DOWN_END,  0.0,   180 - ANGLE_DEG, 180),           # exit base
]:
    ax.add_patch(Arc((xc, yc), 2 * _arc_r, 2 * _arc_r,
                     angle=0, theta1=theta1, theta2=theta2,
                     color="dimgray", lw=1.0, zorder=2))
# angle labels next to entry and exit arcs only (least cluttered spots)
ax.text(X_UP_START   + _arc_r + 0.04, 0.05, f"{ANGLE_DEG:.2f}°", fontsize=7.5, color="dimgray")
ax.text(X_DOWN_END   - _arc_r - 0.12, 0.05, f"{ANGLE_DEG:.2f}°", fontsize=7.5, color="dimgray")

# sharp-corner markers
for xc, yc, lbl in [
    (X_UP_START, 0.0, "entry\ncorner"),
    (X_UP_END, Y_TOP, "top\ncrest↑"),
    (X_TOP_END, Y_TOP, "top\ncrest↓"),
    (X_DOWN_END, 0.0, "exit\ncorner"),
]:
    ax.plot(xc, yc, marker="^", markersize=8, color="steelblue", zorder=3)
    ax.text(xc, yc - 0.06, lbl, ha="center", va="top", fontsize=7, color="steelblue", style="italic")

# ---- draw all 5 cars ----
for pose, color, lbl in zip(all_poses, COLORS, car_labels):
    draw_car(ax, pose, color=color, label=lbl, annotate=False)

# ---- clearance summary box ----
summary = (
    f"Clearances at sharp corners (+ = clear, − = scrape)\n"
    f"Entry  : bumper {checks['start_up_bumper']*1000:+.1f} mm  |  floor {checks['start_up_floor']*1000:+.1f} mm\n"
    f"Top ↑  : bumper/ramp {checks['top_crest_bumper_ramp']*1000:+.1f} mm  bumper/top {checks['top_crest_bumper_top']*1000:+.1f} mm  "
    f"floor/ramp {checks['top_crest_floor_ramp']*1000:+.1f} mm  floor/top {checks['top_crest_floor_top']*1000:+.1f} mm\n"
    f"Top ↓  : bumper/top {checks['down_crest_bumper_top']*1000:+.1f} mm  bumper/down {checks['down_crest_bumper_down']*1000:+.1f} mm  "
    f"floor/top {checks['down_crest_floor_top']*1000:+.1f} mm  floor/down {checks['down_crest_floor_down']*1000:+.1f} mm\n"
    f"Exit   : bumper {checks['exit_bumper_down']*1000:+.1f} mm  |  floor {checks['exit_floor_down']*1000:+.1f} mm"
)
has_neg = "-" in summary
ax.text(
    0.01,
    0.98,
    summary,
    transform=ax.transAxes,
    ha="left",
    va="top",
    fontsize=7.5,
    family="monospace",
    bbox=dict(boxstyle="round,pad=0.4", fc="#ffe8e8" if has_neg else "#e8f5e9", ec="gray", alpha=0.90),
    zorder=9,
)

ax.set_xlim(*FULL_XLIM)
ax.set_ylim(*FULL_YLIM)
ax.set_aspect("equal", adjustable="datalim")
ax.grid(True, alpha=0.22)
ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")
ax.set_title(
    f"RC Car bridge traversal — {ANGLE_DEG:.2f}° ramps · {BRIDGE_H:.2f} m height · "
    f"{TOP_LEN:.2f} m flat top · ramp run {RAMP_RUN:.3f} m · slant {RAMP_SLANT:.3f} m · "
    f"span {X_DOWN_END - X_UP_START:.3f} m",
    fontsize=11,
)
ax.legend(fontsize=8, loc="upper right")

plt.tight_layout()
out_combined = out_dir / "bridge_combined_overview.png"
plt.savefig(out_combined, dpi=180, bbox_inches="tight")
plt.show()
print(f"Saved: {out_combined}")

print("\nBridge summary:")
print(f"  bridge height:  {BRIDGE_H:.3f} m")
print(f"  ramp angle:     {ANGLE_DEG:.4f} deg  ({ANGLE:.6f} rad)")
print(f"  ramp run:       {RAMP_RUN:.4f} m per side  (horizontal)")
print(f"  ramp slant:     {RAMP_SLANT:.4f} m per side  (along face)")
print(f"  flat top len:   {TOP_LEN:.3f} m")
print(f"  total span:     {X_DOWN_END - X_UP_START:.4f} m")
print(f"\n  ≥{CLEARANCE_MIN*100:.0f} cm clearance section:")
print(f"    starts at x = {x_30_start:.4f} m  (on up-ramp)")
print(f"    ends   at x = {x_30_end:.4f} m  (on down-ramp)")
print(f"    length       = {len_30:.4f} m")

# ---- end ----
