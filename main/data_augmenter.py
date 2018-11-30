import file_manager as fm
import Leap
import numpy.random as r
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class DataAugmenter:
    scaling_factor = 0.0
    angle_x = 0.0
    angle_y = 0.0
    angle_z = 0.0
    hand_variation = 0.0
    scaling_values = [-0.10, 0.10, -0.11, 0.11, -0.12, 0.12, -0.13, 0.13, -0.14, 0.14, -0.15, 0.15]
    angle_x_values = [-5, 5, -6, 6, -7, 7, -8, 8, -9, 9 - 10, 10]
    angles_values = [-10, 10, -11, 11, -12, 12, -13, 13, -14, 14 - 15, 15]
    hand_values = [-0.01, 0.01, -0.02, 0.02, -0.03, 0.03, -0.04, 0.04, -0.05, 0.05]

    def generate_variation(self):
        self.angle_x = np.radians(r.choice(self.angle_x_values))
        self.angle_y = np.radians(r.choice(self.angles_values))
        self.angle_z = np.radians(r.choice(self.angles_values))
        self.hand_variation = r.choice(self.hand_values)
        #self.scaling_factor = r.choice(self.scaling_values)
        self.scaling_factor = 0.2

    def augment_gesture(self, classified_gesture):
        self.generate_variation()
        print self.hand_variation

        for i in range(0, 60):
            classified_gesture.sequence.data_list[i] = self.augmented_frame(classified_gesture.sequence.data_list[i])
        return classified_gesture

    def augmented_frame(self, hand_model):

        # ROTAZIONE ASSE Z
        hand_model.delta_palm_position.x = hand_model.delta_palm_position.x * np.cos(
            self.angle_z) - hand_model.delta_palm_position.y * np.sin(self.angle_z)
        hand_model.delta_palm_position.y = hand_model.delta_palm_position.x * np.sin(
            self.angle_z) + hand_model.delta_palm_position.y * np.cos(self.angle_z)
        #
        ## ROTAZIONE ASSE X
        hand_model.delta_palm_position.z = hand_model.delta_palm_position.z * np.cos(
            self.angle_x) - hand_model.delta_palm_position.y * np.sin(self.angle_x)
        hand_model.delta_palm_position.y = hand_model.delta_palm_position.x * np.sin(
            self.angle_x) + hand_model.delta_palm_position.y * np.cos(self.angle_x)
        #
        ##
        #
        ## ROTAZIONE ASSE Y
        hand_model.delta_palm_position.x = hand_model.delta_palm_position.x * np.cos(
            self.angle_y) - hand_model.delta_palm_position.z * np.sin(self.angle_y)
        hand_model.delta_palm_position.z = hand_model.delta_palm_position.x * np.sin(
            self.angle_y) + hand_model.delta_palm_position.z * np.cos(self.angle_y)

        #
        hand_model.delta_palm_position.x += hand_model.delta_palm_position.x * self.scaling_factor
        hand_model.delta_palm_position.y += hand_model.delta_palm_position.y * self.scaling_factor
        hand_model.delta_palm_position.z += hand_model.delta_palm_position.z * self.scaling_factor

        for i in range(0, 5):
            hand_model.fingers[i].proximal_angle += hand_model.fingers[i].proximal_angle * (self.hand_variation)
            hand_model.fingers[i].distal_angle += hand_model.fingers[i].distal_angle * (self.hand_variation * 1.2)

            if hand_model.fingers[i].type is not Leap.Finger.TYPE_THUMB:
                hand_model.fingers[i].intermediate_angle += hand_model.fingers[i].intermediate_angle * (
                            self.hand_variation * 1.1)
        return hand_model

    def graph_gesture(self, gesture_list, new_gesture_list, element):
        sequence = gesture_list.sequence

        if element == "palm":
            old_x_values = []
            old_y_values = []
            old_z_values = []
            new_x_values = []
            new_y_values = []
            new_z_values = []
            old_act_pos_x = 0.0
            old_act_pos_y = 0.0
            old_act_pos_z = 0.0
            new_act_pos_x = 0.0
            new_act_pos_y = 0.0
            new_act_pos_z = 0.0
            old_frames = gesture_list.sequence.data_list
            new_frames = new_gesture_list.sequence.data_list
            j = 0
            for i in range(0, 60):
                old_act_pos_x += old_frames[i].delta_palm_position.x
                old_act_pos_y += old_frames[i].delta_palm_position.y
                old_act_pos_z += old_frames[i].delta_palm_position.z
                old_x_values.append(old_act_pos_x)
                old_y_values.append(old_act_pos_y)
                old_z_values.append(old_act_pos_z)

                new_act_pos_x += new_frames[i].delta_palm_position.x
                new_act_pos_y += new_frames[i].delta_palm_position.y
                new_act_pos_z += new_frames[i].delta_palm_position.z
                new_x_values.append(new_act_pos_x)
                new_y_values.append(new_act_pos_y)
                new_z_values.append(new_act_pos_z)

                fig = plt.figure()
                ax = fig.gca(projection='3d')
                ax.plot(old_x_values, old_z_values, old_y_values)
                ax.plot(new_x_values, new_z_values, new_y_values)
                ax.set_xbound([-150, 150])
                ax.set_ybound([-100, 100])
                ax.set_zbound([-100, 100])
                plt.savefig("../plot/" + str(j) + '.png')
                j += 1
                plt.show()

            # plt.plot(x_values, 'r', y_values, 'b', z_values, 'g')
        elif element == "arm":
            angles = []
            for frame in sequence.data_list:
                angles.append(frame.arm_angle)
            axes = plt.gca()
            axes.set_xlim([0, 60])
            axes.set_ylim([0, 100])
            plt.plot(angles)
            plt.show()

        elif element == 0:
            alphas = []
            gammas = []
            for frame in sequence.data_list:
                alphas.append(frame.thumb.proximal_angle)
                gammas.append(frame.thumb.distal_angle)
            axes = plt.gca()
            axes.set_xlim([0, 60])
            axes.set_ylim([0, 200])
            plt.plot(alphas, "r", gammas, "b")
            plt.show()

        elif type(element) is int:
            alphas = []
            betas = []
            gammas = []

            for frame in sequence.data_list:
                alphas.append(frame.fingers[element].proximal_angle)
                betas.append(frame.fingers[element].intermediate_angle)
                gammas.append(frame.fingers[element].distal_angle)
            axes = plt.gca()
            axes.set_xlim([0, 60])
            axes.set_ylim([0, 200])
            plt.plot(alphas, 'r', betas, 'b', gammas, 'g')
            plt.show()


if __name__ == '__main__':
    loader = fm.Loader()
    saver = fm.Saver()
    augmenter = DataAugmenter()
    files = ["1_lisa", "2_sara", "3_ramo", "4_ale", "5_gian", "6_must", "7_ilar", "8_chia", "9_mart",
             "10_fabi", "11_vitt", "12_fili", "13_bis", "14_fran", "15_jean", "16_alfr", "17_ele",
             "18_clau", "19_mart", "20_lore", "21_qi", "22_bea", "23_eleo", "24_chia", "25_marc",
             "26_edo", "31_simo", "28_rob", "29_cla", "30_dav"]

    for file_name in files:

        classified_list = loader.load_file(file_name)
        # augmenter.graph_gesture(classified_list[15], classified_list[15], 1)
        # augmenter.graph_gesture(classified_list[10], "palm")
        augmented_classified_list = []
        for gesture in classified_list:
            augmented_classified_list.append(augmenter.augment_gesture(gesture))

        saver.add_data_to_file(augmented_classified_list, "aug/3_aug_" + file_name)

    #classified_list = loader.load_file("1_lisa")
    #augmenter.graph_gesture(classified_list[10], augmented_classified_list[10], "palm")
