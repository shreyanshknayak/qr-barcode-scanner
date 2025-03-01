import cv2
import numpy as np
from pyzbar.pyzbar import decode


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5,5), 0)

    barcode = decode(blurred)

    for barcode in barcode:
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1,1,2))

        cv2.polylines(frame, [pts], True, (0,255,0), 2)

        barcode_text = barcode.data.decode("utf-8")
        barcode_type = barcode.type

        cv2.putText(frame, f'{barcode_type}: {barcode_text}', (barcode.rect.left, barcode.rect.top-10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Barcode & QR Code Scanner", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()