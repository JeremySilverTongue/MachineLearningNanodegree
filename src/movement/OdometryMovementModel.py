import math
import random

ALPHA_1 = .1
ALPHA_2 = .01
ALPHA_3 = .1
ALPHA_4 = .01


def target_rotation(pose1, pose2):
    x_start, y_start, t_start = pose1
    x_end, y_end = pose2
    return x_end, y_end, math.atan2(y_end - y_start, x_end - x_start)


def sample_motion_model_no_final_rotation(pose1, pose2, a1=ALPHA_1, a2=ALPHA_2, a3=ALPHA_3, a4=ALPHA_4):
    return sample_motion_model(pose1, target_rotation(pose1, pose2), a1, a2, a3, a4)


def sample_motion_model(pose, rotation, translation, a1=ALPHA_1, a2=ALPHA_2, a3=ALPHA_3, a4=ALPHA_4):
    y_start, x_start, t_start = pose

    d_r1 = rotation
    d_trans = translation

    d_r1_hat = d_r1 - random.normalvariate(0, a1 * d_r1 + a2 * d_trans)
    d_trans_hat = d_trans - random.normalvariate(0, a3 * d_trans + a4 * d_r1)

    x_actual = x_start + d_trans_hat * math.cos(t_start + d_r1_hat)
    y_actual = y_start + d_trans_hat * math.sin(t_start + d_r1_hat)
    t_actual = t_start + d_r1_hat

    return y_actual, x_actual, t_actual
