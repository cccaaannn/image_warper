import os
import cv2
import pathlib
import numpy as np


class image_warper():
    def __init__(self, image_path, save_folder="out", windows_size=(1200, 700)):
        self.image_path = image_path
        self.save_folder = save_folder
        self.windows_size = windows_size

        self.setup()

    def setup(self):
        """setup for opencv window"""
        self.window_name = "warp image"
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, self.windows_size[0], self.windows_size[1])
        cv2.setMouseCallback(self.window_name, self.draw_circle)


    def warp_image(self):
        """warps image with opecv findHomography and warpPerspective functions"""
        image = cv2.imread(self.image_path)
        points = np.array(self.points)
    
        image_array = np.array([[0, 0],[image.shape[1], 0],[0, image.shape[0]],[image.shape[1], image.shape[0]]])

        h, status = cv2.findHomography(points, image_array)

        new_image = cv2.warpPerspective(image, h, (image.shape[1],image.shape[0]))

        return new_image

    def refresh_image(self):
        self.image = cv2.imread(self.image_path)
        self.points = []

    def draw_circle(self, event, x, y, flags, param):
        if(event == cv2.EVENT_LBUTTONDOWN):
            if(len(self.points) < 4):
                cv2.circle(self.image,(x,y),3,(255,0,0),-1)

                points_temp = []
                points_temp.append(x)
                points_temp.append(y)
                self.points.append(points_temp)
                print("points: {0}".format(self.points))
            else:
                print("can not select more than 4 points")

    def create_unique_file_name(self, file_path, before_number="(", after_number=")"):
        temp_file_path = file_path
        file_name_counter = 1
        if(os.path.isfile(temp_file_path)):
            while(True):
                save_path, temp_file_name = os.path.split(temp_file_path)
                temp_file_name, temp_file_extension = os.path.splitext(temp_file_name)
                temp_file_name = "{0}{1}{2}{3}{4}".format(temp_file_name, before_number, file_name_counter, after_number, temp_file_extension)
                temp_file_path = os.path.join(save_path, temp_file_name)
                file_name_counter += 1
                if(os.path.isfile(temp_file_path)):
                    temp_file_path = file_path
                else:
                    file_path = temp_file_path
                    break

        return file_path


    def start_warper(self):
        """starts opencv window"""
        print("please select points with this order.\ntop left, top right, bottom left, bottom right")

        self.image = cv2.imread(self.image_path)
        self.points = []
        while(True):
            cv2.imshow(self.window_name, self.image)
            key = cv2.waitKey(1)

            if(key == ord("s")):
                if(len(self.points) == 4):
                    # warp image
                    new_image = self.warp_image()

                    # create new path
                    pathlib.Path(self.save_folder).mkdir(parents=True, exist_ok=True)
                    _, image_name = os.path.split(self.image_path)
                    save_path = os.path.join(self.save_folder, image_name)                    
                    save_path = self.create_unique_file_name(save_path)

                    # save and show new image
                    cv2.imwrite(save_path, new_image)
                    cv2.imshow("warped image", new_image)
                    print("image saved '{0}'".format(save_path))

                    # refresh image
                    self.refresh_image()
                else:
                    print(self.points)
                    print("select more points or\nclear selected points with c")

            # options
            if(key == ord("c")):
                print("image reloaded")
                self.refresh_image()

            # exit
            if(cv2.getWindowProperty(self.window_name, 0) < 0):
                break

            if(key == 27):
                break

        cv2.destroyAllWindows()




if __name__ == "__main__":
    warper = image_warper("example_images/1.jpeg")
    warper.start_warper()
