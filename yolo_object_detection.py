import cv2 as cv
import numpy as np
import time
TRAGET_IMAGE_DIMENSIONS = (640,640)
COLORS = [(255, 255, 0), (0, 255, 0), (0, 255, 255), (255, 0, 0)]
LABEL_NAMES = ['bicycle', 'bus', 'car', 'motorcycle', 'truck']
def create_yolo_model():
    yolo_net =cv.dnn.readNetFromONNX(r"yolo_model\best.onnx")
    return yolo_net

YOLO = create_yolo_model()


def image_format(image):
    
    colums, row, _ = image.shape
    max_of_dimensions = max(colums,row)

    reshape = np.zeros((max_of_dimensions, max_of_dimensions,3), np.uint8)
    reshape[0:colums,0:row] = image

    return reshape

def detect_objects(resized_image,yolo_net):
    formatted_image = cv.dnn.blobFromImage(resized_image, 1/255.0, TRAGET_IMAGE_DIMENSIONS, swapRB = True, crop=True)
    yolo_net.setInput(formatted_image)
    return yolo_net.forward()

def refactor_box_dimenstions(detection_row,image):

    img_height , img_width,_ = image.shape

    x = detection_row[0]
    y = detection_row[1]
    w = detection_row[2]
    h = detection_row[3]


    left = int((x - 0.5 * w) * (img_width/TRAGET_IMAGE_DIMENSIONS[0]))
    top = int((y - 0.5 * h) * (img_height/TRAGET_IMAGE_DIMENSIONS[1]))
    width = int(w * (img_width/TRAGET_IMAGE_DIMENSIONS[0]))
    height = int(h * (img_height/TRAGET_IMAGE_DIMENSIONS[1]))

    box = np.array([left, top, width, height])

    return box

def unravel_detections(resized_image,yolo_detections):

    rows = yolo_detections.shape[1]

    label_indexes = []
    confidences =[]
    boxes = []


    for i in range(yolo_detections.shape[0]):
        for row_index in range(rows):
            detection_row = yolo_detections[i][row_index]
            label_confidence = detection_row[4]

            if label_confidence >=0.45:
            
                label_scores = detection_row[5:]
                _,_,_,max_index = cv.minMaxLoc(label_scores)

                label_id = max_index[1]
                
                if label_scores[label_id] > 0.25 :
                    
                    confidences.append(label_confidence)
                    label_indexes.append(label_id)
                    boxes.append(refactor_box_dimenstions(detection_row,resized_image))

    nms_box_indexes = cv.dnn.NMSBoxes(boxes,confidences,0.25, 0.45)

    final_label_indexes= []
    final_confidences =[]
    final_boxes = []

    for nbi in nms_box_indexes:
        final_label_indexes.append(label_indexes[nbi])
        final_confidences.append(confidences[nbi])
        final_boxes.append(boxes[nbi])

    
    return final_confidences, final_label_indexes, final_boxes
       
                
def getDetectedObjectsBox(image):

    # #creating yolo model
    # yolo = create_yolo_model()
    
    #resizing the image according to yolov5 architecture
    resized_image = image_format(image)
    
    #passing the formatted image to yolo and finding the detections
    yolo_detections = detect_objects(resized_image,YOLO)

    #getting the label_indexes, confidences and respective boxes of the 
    confidences,label_indexes, boxes = unravel_detections(resized_image, yolo_detections)

    return confidences,label_indexes,boxes





if __name__ == "__main__":
    start = time.time_ns()
    frame_count = 0
    total_frames = 0
    fps = -1
    
    # yolo = create_yolo_model()
    
    # creating the capture object
    capture = cv.VideoCapture("video\GTA-V_trimmed1.mp4")
    capture.set(cv.CAP_PROP_FPS, 60)
    capture.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
    while(True):
        #reading the frame
        status,image = capture.read()
        if image is None:
            break
        
        frame_count += 1
        total_frames += 1
        # #formatting the image to yolov5 input dimensions
        # resized_image = image_format(image)

        # #passing the formatted image to yolo and finding the detections
        # yolo_detections = detect_objects(resized_image,yolo)

        # #getting the label_indexes, confidences and respective boxes of the 
        confidences,label_indexes, boxes = getDetectedObjectsBox(image)

        for (confidence, labelid, box) in zip(confidences,label_indexes, boxes):

            color = COLORS[int(labelid) % len(COLORS)]
            cv.rectangle(image, box, color, 2)
            cv.rectangle(image, (box[0], box[1] - 20), (box[0] + box[2], box[1]), color, -1)
            cv.putText(image, LABEL_NAMES[labelid], (box[0], box[1] - 10), cv.FONT_HERSHEY_SIMPLEX, .5, (0,0,0))

        if frame_count >= 30:
            end = time.time_ns()
            fps = 1000000000 * frame_count / (end - start)
            frame_count = 0
            start = time.time_ns()

        if fps > 0:
            fps_label = "FPS: %.2f" % fps
            cv.putText(image, fps_label, (10, 25), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv.imshow("output",image)

        if cv.waitKey(1)>-1:
            print('exited')
            break
    capture.release()
    cv.destroyAllWindows()
