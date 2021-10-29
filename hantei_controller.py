import threading
import torch
from torch.nn import Module
from yolov5.models.experimental import Ensemble
from yolov5.utils.plots import Annotator, colors
from yolov5.utils.datasets import LoadStreams
from typing import Union
from yolov5.utils.torch_utils import time_sync
from yolov5.utils.general import non_max_suppression, scale_coords


# 判定の処理を行うクラス
class HanteiController:
    model: Union[Module, Ensemble]
    input: Union[None, torch.Tensor] = None
    command: int = -1
    thread: threading.Thread

    # streamType is same as index at VideoCapture(index)
    def __init__(self, streamType: int):
        self.thread = threading.Thread(
            target=self.execute,
            args=([streamType]),
            daemon=True
        )
        self.thread.start()

    def execute(self, streamType: int):
        model = torch.hub.load('.', 'custom', autoshape=True, path='best.pt', source='local', device='cpu')
        model.conf = 0.5  # minimum confidence threshold
        # torch.cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(f'{streamType}')
        bs = len(dataset)  # batch_size
        names = model.module.names if hasattr(model, 'module') else model.names  # get class names

        dt, seen = [0.0, 0.0, 0.0], 0
        conf_thres = 0.4  # confidence threshold
        iou_thres = 0.45  # NMS IOU threshold
        max_det = 1000  # maximum detections per image
        agnostic_nms = False

        for path, img, im0s, vid_cap in dataset:
            t1 = time_sync()
            img = torch.from_numpy(img).to('cpu')
            img = img.float()
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if len(img.shape) == 3:
                img = img[None]  # expand for batch dim
            t2 = time_sync()
            dt[0] += t2 - t1

            pred = model(img)[0]

            t3 = time_sync()
            dt[1] += t3 - t2

            # NMS
            pred = non_max_suppression(
                pred,
                conf_thres,
                iou_thres,
                classes=[15, 16, 17],
                agnostic=agnostic_nms,
                max_det=max_det
            )
            dt[2] += time_sync() - t3
            print(pred)

            command = ''

            # Process predictions
            for i, det in enumerate(pred):  # per image
                seen += 1
                p, s, im0, frame = path[i], f'{i}: ', im0s[i].copy(), dataset.count

                s += '%gx%g ' % img.shape[2:]  # print string
                annotator = Annotator(im0, line_width=None, example=str(names))
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                    # Write results
                    for *xyxy, conf, cls in reversed(det):
                        c = int(cls)  # integer class
                        command = names[c]
                        label = f'{names[c]} {conf:.2f}'
                        annotator.box_label(xyxy, label, color=colors(c, True))

                # Print time (inference-only)
                print(f'{s}Done. ({t3 - t2:.3f}s)')
                if command == 'goo':
                    self.command = 0
                elif command == 'choki':
                    self.command = 1
                elif command == 'par':
                    self.command = 2
                print(f'command: {self.command}')

                # # Stream results
                # im0 = annotator.result()
                #
                # cv2.imshow(s, im0)
                # cv2.waitKey(1)
                # cv2.destroyWindow(s)


