import pathlib
import queue
import threading

import cv2

FRAME_RATE = 600


def read_frame(target_paths, frame_queue):
    for path in target_paths:
        capture = cv2.VideoCapture(str(path))
        if not capture.isOpened():
            return
        frame_index = 0
        while True:
            result, frame = capture.read()
            if not result:
                break
            # print("[read] {}:{}".format(path, frame_index))
            frame_queue.put(frame)
            frame_index += 1
        capture.release()
    frame_queue.put(None)


def write_frame(frame_queue):
    video_writer = cv2.VideoWriter(
        "out.mp4", cv2.VideoWriter_fourcc("m", "p", "4", "v"), 20, (1920, 1080)
    )

    frame_index = 0
    while True:
        frame = frame_queue.get()
        try:
            if frame is None:
                break
            if frame_index % FRAME_RATE == 0:
                print("[write] {}".format(frame_index))
                video_writer.write(frame)
            frame_index += 1
        finally:
            frame_queue.task_done()

    video_writer.release()


target_dir = pathlib.Path(".")
target_paths = sorted(target_dir.glob("**/*.MTS"))

frame_queue = queue.Queue(maxsize=10)

read_frame_worker = threading.Thread(
    target=read_frame,
    daemon=True,
    kwargs={"target_paths": target_paths, "frame_queue": frame_queue},
)
read_frame_worker.start()

write_frame_worker = threading.Thread(
    target=write_frame, daemon=True, kwargs={"frame_queue": frame_queue},
)
write_frame_worker.start()

read_frame_worker.join()
write_frame_worker.join()

print("done")
