import cv2
import numpy as np
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

from calculateAngle import calculate_angle

class Exercise:
    def __init__(self):
        self.counter = 0
        self.stage = 'up'
        self.arm_error_printed = False
        self.back_error_printed = False
        self.palms_error_printed = False
        self.alignment_error_printed = False

    def pushups(self, image, lm, reps):
        #arms
        r1 = [int(lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * image.shape[1]), int(lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image.shape[0])]
        r2 = [int(lm[mp_pose.PoseLandmark.RIGHT_ELBOW].x * image.shape[1]), int(lm[mp_pose.PoseLandmark.RIGHT_ELBOW].y * image.shape[0])]
        r3 = [int(lm[mp_pose.PoseLandmark.RIGHT_WRIST].x * image.shape[1]), int(lm[mp_pose.PoseLandmark.RIGHT_WRIST].y * image.shape[0])]
        l1 = [int(lm[mp_pose.PoseLandmark.LEFT_SHOULDER].x * image.shape[1]), int(lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y * image.shape[0])]
        l2 = [int(lm[mp_pose.PoseLandmark.LEFT_ELBOW].x * image.shape[1]), int(lm[mp_pose.PoseLandmark.LEFT_ELBOW].y * image.shape[0])]
        l3 = [int(lm[mp_pose.PoseLandmark.LEFT_WRIST].x * image.shape[1]), int(lm[mp_pose.PoseLandmark.LEFT_WRIST].y * image.shape[0])]
        
        #back and legs
        l4 = [int(lm[mp_pose.PoseLandmark.LEFT_HIP].x * image.shape[1]), int(lm[mp_pose.PoseLandmark.LEFT_HIP].y * image.shape[0])]
        l5 = [int(lm[mp_pose.PoseLandmark.LEFT_KNEE].x * image.shape[1]), int(lm[mp_pose.PoseLandmark.LEFT_KNEE].y * image.shape[0])]
        l6 = [int(lm[mp_pose.PoseLandmark.LEFT_ANKLE].x * image.shape[1]), int(lm[mp_pose.PoseLandmark.LEFT_ANKLE].y * image.shape[0])]
        r4 = [int(lm[mp_pose.PoseLandmark.RIGHT_HIP].x * image.shape[1]), int(lm[mp_pose.PoseLandmark.RIGHT_HIP].y * image.shape[0])]
        r5 = [int(lm[mp_pose.PoseLandmark.RIGHT_KNEE].x * image.shape[1]), int(lm[mp_pose.PoseLandmark.RIGHT_KNEE].y * image.shape[0])]
        r6 = [int(lm[mp_pose.PoseLandmark.RIGHT_ANKLE].x * image.shape[1]), int(lm[mp_pose.PoseLandmark.RIGHT_ANKLE].y * image.shape[0])]
        
        #hands
        rpalm = [int(lm[mp_pose.PoseLandmark.RIGHT_PINKY].x * image.shape[1]), int(lm[mp_pose.PoseLandmark.RIGHT_PINKY].y * image.shape[0])]
        lpalm = [int(lm[mp_pose.PoseLandmark.LEFT_PINKY].x * image.shape[1]), int(lm[mp_pose.PoseLandmark.LEFT_PINKY].y * image.shape[0])]

        angleR = calculate_angle(r1, r2, r3)
        angleL = calculate_angle(l1, l2, l3)
        back_angleR = calculate_angle(r1, r4, r5)
        back_angleL = calculate_angle(l1, l4, l5)
        
        #palm distance
        palms_distance = np.linalg.norm(np.array(rpalm) - np.array(lpalm))

        #hips and sholder alignment
        shoulder_diff = abs(r1[1] - l1[1])
        hip_diff = abs(r4[1] - l4[1])
        alignment_threshold = 50  
        
        
        #cv line function
        def draw_line(start, end, color):
            cv2.line(image, tuple(start), tuple(end), color, 4)

        #cv circle function
        def draw_circle(joint):
            cv2.circle(image, tuple(joint), 10, (255, 255, 255), -1)

        #color without error
        upper_body_color = (255, 255, 255)
        lower_body_color = (255, 255, 255)

        #color with error
        has_error = False
        if angleR <= 50 or angleL <= 50:
            upper_body_color = (0, 0, 255)
        if back_angleR <= 120 or back_angleL <= 120:
            lower_body_color = (0, 0, 255)
            has_error = True
        if palms_distance < 50:
            upper_body_color = (0, 0, 255)
        if shoulder_diff > alignment_threshold or hip_diff > alignment_threshold:
            upper_body_color = (0, 0, 255)
            lower_body_color = (0, 0, 255)
            


        draw_line(r1, r2, upper_body_color)
        draw_line(r2, r3, upper_body_color)
        draw_line(l1, l2, upper_body_color)
        draw_line(l2, l3, upper_body_color)
        draw_line(r1, l1, upper_body_color)
        draw_line(r4, r5, lower_body_color)
        draw_line(r5, r6, lower_body_color)
        draw_line(l4, l5, lower_body_color)
        draw_line(l5, l6, lower_body_color)
        draw_line(r1, r4, lower_body_color)
        draw_line(l1, l4, lower_body_color)
        for joint in [r1, r2, r3, l1, l2, l3, r4, r5, r6, l4, l5, l6]:
            draw_circle(joint)


        #feedback
        if angleR <= 50 or angleL <= 50:
            if not self.arm_error_printed:
                print("Keep your arms straight!")
                self.arm_error_printed = True
        else:
            self.arm_error_printed = False

        if back_angleR <= 120 or back_angleL <= 120:
            if not self.back_error_printed:
                print("Keep your back straight!")
                self.back_error_printed = True
        else:
            self.back_error_printed = False

        if palms_distance < 30:
            if not self.palms_error_printed:
                print("Keep your palms further apart!")
                self.palms_error_printed = True
        else:
            self.palms_error_printed = False

        if shoulder_diff > alignment_threshold or hip_diff > alignment_threshold:
            if not self.alignment_error_printed:
                print("Align your shoulders and hips horizontally!")
                self.alignment_error_printed = True
        else:
            self.alignment_error_printed = False

        #counter
        if not has_error:
            if angleL < 90 and angleR < 90:
                if self.stage == 'up':
                    self.counter += 1
                    print(f"Push-up count: {self.counter}")
                    self.stage = 'down'
            if angleL > 90 and angleR > 90:
                if self.stage == 'down':
                    self.stage = 'up'

        if self.counter >= reps:
            print("Exercise complete!")
            return True

        return False