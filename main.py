import cv2
import PoseModule as pm

cam = cv2.VideoCapture(0)
pose = pm.poseDetector()

counter = 0
stage = "None"

while True:
    success, frame = cam.read()

    if success:

        frame = pose.findPose(frame)
        lm, l = pose.findPosLm(frame)

        if lm:
            rightShoulder = lm[12]
            rightElbow = lm[14]
            rightWrist = lm[16]

            angle = int(pose.findAngle(rightShoulder, rightElbow, rightWrist))

            cv2.putText(frame, f"angle: {str(angle)}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

            # curl counter
            if angle > 160:
                stage = "down"
            if angle < 30 and stage == 'down':
                stage = "up"
                counter += 1

            cv2.rectangle(frame, (10, 70), (155, 190),
                          (0, 0, 0), cv2.FILLED)
            cv2.rectangle(frame, (10, 70), (155, 190),
                          (255, 0, 255), 5)

            cv2.putText(frame, str(counter), (20, 150), cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
                        3, (255, 255, 255), 18)
            cv2.putText(frame, str(stage), (500, 70), cv2.FONT_HERSHEY_PLAIN,
                        3, (255, 0, 255), 6)



        cv2.imshow("AI GYM TRAINER", frame)
        k = cv2.waitKey(1)

        if k == ord("q"):
            break

cam.release()
cv2.destroyAllWindows()