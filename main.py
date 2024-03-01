from Front_detection import *
from Flag import *

def main():
    """首先创建四个图像"""
    # 保存各个图像名称的列表
    roi_image_arr = [
        ["roi_left_front.jpg", 'front'],
        ["roi_right_front.jpg", 'front'],
        ["roi_left_back.jpg", 'back'],
        ["roi_right_back.jpg", 'back']
    ]

    for image_name in roi_image_arr:
        if PRETRAIN_FLAG:
            # 先划定感兴趣区域，先左后右，先前后尾
            get_ROI(image_name)
            img = cv2.imread(image_name[0])
            cv2.imshow('image_catched', img)
            cv2.waitKey(0)
    print("ROI pictures created successfully!")

    """保存两条赛道四条边界线、八个对应参数的变量"""
    track_line = []  # 分别是前左、前右、后左、后右
    for idx in range(4):
        line = Line_State()
        line.l_b, line.l_k, line.r_b, line.r_k = get_weight_bias_of_trackline(name=roi_image_arr[idx][0],
                                                                              forward=roi_image_arr[idx][1])
        track_line.append(line)

    # with open("line_data.json", 'w') as f:
    #     for i in range(4):
    #         f.write(roi_image_arr[i][0]+':\n')
    #         f.write('left_b='+str(track_line[i].l_b) + ' ,left_k=' + str(track_line[i].l_k)
    #                 + ' ,right_b=' + str(track_line[i].r_b) +
    #                 ' ,right_k=' + str(track_line[i].r_k) + '\n\n')

    roads = ["roi_left_front.jpg", "roi_right_front.jpg", "roi_left_back.jpg", "roi_right_back.jpg"]
    sides = ["left", "right"]
    datas = ["slope", "intercept"]
    s = 0

    with open('line_data.json', 'w') as f:
        f.write('{\n')
        f.write('  "image": {\n')
        for i in range(4):
            f.write('    \"' + roads[i] + '\": {\n')
            for j in range(2):
                f.write('      \"' + sides[j] + '\": {\n')
                for k in range(2):
                    if k == 0:
                        f.write('        \"' + datas[k] + '\": ' + str(track_line[i].l_k) + ',\n')
                    else:
                        f.write('        "' + datas[k] + '\": ' + str(track_line[i].l_b) + '\n')
                s = s + 1
                if j == 0:
                    f.write('      },\n')
                else:
                    f.write('      }\n')
            if i == 3:
                f.write('    }\n')
            else:
                f.write('    },\n')
        f.write('  }\n')
        f.write('}\n')

    return track_line


if __name__ == '__main__':
    main()
