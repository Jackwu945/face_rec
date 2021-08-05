try:
    import face_recognition
    import cv2
    from threading import Thread
    from PIL import Image
    import os
    import time

    print('加载中')
    flag=False
    capimshow=False
    capstatus='running'
    ask=None

    def path_count(path_dir):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        return len([lists for lists in os.listdir(dir_path+path_dir) if os.path.isfile(os.path.join(dir_path+path_dir, lists))])


    def sample():
        #取样
        samplelist=[]
        path_dir = '/capt/sample'
        for i in range(path_count(path_dir)):
            sample=face_recognition.load_image_file('capt/sample/sample{}.jpg'.format(i))
            encode=face_recognition.face_encodings(sample)
            if encode != []:
                samplelist.append(encode[0])
        return samplelist

    #实时获取人脸,调用摄像机
    def camera():
        global flag,capstatus,ask
        print(capstatus)
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 电脑自身摄像头
        while True:
            while capstatus == 'running':
                reg, frame = cap.read()
                frame = cv2.flip(frame, 1)  # 图片左右调换
                filename = 'capt.png'  # filename为图像名字，将photoname作为编号命名保存的截图
                cv2.imwrite('capt/' + filename, frame)  # 截图 前面为放在桌面的路径 frame为此时的图像
                flag = True
            while capstatus == 'imshow':
                img = Image.open('capt/capt.png')
                img.show()
                capstatus='release'
            while capstatus == 'release':
                cap.release()
                break
            break

    def video_demo(samplelist):
        global flag,capstatus,capimshow
        while True:
            if flag==True:
                captface = face_recognition.load_image_file('capt/capt.png')
                faceencoding = face_recognition.face_encodings(captface)
                if faceencoding == []:
                    # print('未检测到脸')
                    continue
                faceno=0
                for sampleencoding in samplelist:
                    if face_recognition.compare_faces(sampleencoding, faceencoding) == [True]:
                        # print('检测到此人为{}'.format(faceno))
                        capstatus = 'release'
                        return faceno
                    faceno+=1
            else:
                continue

    def face_record():
        global flag,capstatus,ask
        while True:
            if flag==True:
                captface = face_recognition.load_image_file('capt/capt.png')
                faceencoding = face_recognition.face_encodings(captface)
                if len(faceencoding) == 1:
                    capstatus = 'imshow'
                    ask=input('是否录入该人脸(y/n)')
                    if ask == 'y':
                        capstatus = 'release'
                        return True
                    elif ask == 'n':
                        break
                else:
                    continue
            else:
                continue

    # samplelist=sample()
    # Thread(target=camera).start()
    # vd=video_demo(samplelist)
    # print(vd)

    while True:
        mode=int(input('请选择\n1:人脸录入\n2:人脸识别\n请选择'))
        if mode == 1:
            capstatus='running'
            Thread(target=camera).start()
            time.sleep(11)
            vd=face_record()
            if vd==True:
                path_dir = '/capt/sample'
                pc=path_count(path_dir)
                os.rename('capt/capt.png','capt/sample/sample{}.jpg'.format(pc))
        elif mode ==2:
            try:
                capstatus='running'
                Thread(target=camera).start()
                time.sleep(1)
                print('人脸位于索引'+str(video_demo(sample())))
            except Exception as e:
                capstatus='release'
                print('肥肠抱歉,相机获取的图片炸了,正在重试')
                capstatus='running'
                Thread(target=camera).start()
                time.sleep(1)
                print('人脸位于索引'+str(video_demo(sample())))
except Exception as e:
    print(e)