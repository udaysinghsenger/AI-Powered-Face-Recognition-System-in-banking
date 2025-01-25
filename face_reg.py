import cv2, sys, numpy, os
import string
import random
 
# initializing size of string
N = 4
 
# using random.choices()
# generating random strings
res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=N))

path1='D:/project ml/NOT RUN/Bank_Web_CRT_2021/datasets/invalid/'
path2='D:/project ml/NOT RUN/Bank_Web_CRT_2021/datasets/unauthorized/'
def face_reg(name):
    size = 4
    haar_file ="haarcascade_frontalface_alt2.xml"
    datasets = './datasets'
    print('Recognizing Face Please Be in sufficient Lights...') 
    (images, lables, names, id) = ([], [], {}, 0) 
    for (subdirs, dirs, files) in os.walk(datasets): 
        for subdir in dirs: 
            names[id] = subdir 
            subjectpath = os.path.join(datasets, subdir) 
            for filename in os.listdir(subjectpath): 
                path = subjectpath + '/' + filename 
                lable = id
                images.append(cv2.imread(path, 0)) 
                lables.append(int(lable)) 
            id += 1
    (width, height) = (130, 100) 
    (images, lables) = [numpy.array(lis) for lis in [images, lables]] 
    print(images)
    model = cv2.face.LBPHFaceRecognizer_create() 
    model.train(images, lables) 
    face_cascade = cv2.CascadeClassifier(haar_file) 
    webcam = cv2.VideoCapture(0)
    su=1
    er=1
    while True: 
        (_, im) = webcam.read() 
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
        faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
        for (x, y, w, h) in faces: 
            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2) 
            face = gray[y:y + h, x:x + w] 
            face_resize = cv2.resize(face, (width, height)) 
            prediction = model.predict(face_resize) 
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3) 
            if prediction[1]<70:
                cv2.putText(im, '% s - %.0f' % (names[prediction[0]], prediction[1]), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)) 
                su+=1
                if su==30:
                    if names[prediction[0]] == name :
                        return 'Authorized'
                    else:
                        
                        cv2.imwrite('% s/% s.png' % (path1,res), face_resize) 
                        return 'Invalid User'

            else:
                cv2.putText(im, 'not recognized',  (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)) 
                er+=1
                if er==30:
                        
                        cv2.imwrite('% s.png' % (path2), face_resize) 
                        return 'Unauthorized' 
        cv2.imshow('OpenCV', im) 
        key = cv2.waitKey(10) 
        if key == 27: 
            break
    webcam.release()
    cv2.destroyAllWindows()