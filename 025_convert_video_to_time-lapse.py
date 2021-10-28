import pathlib
import queue
import threading

import cv2

import time

# PEP8に準拠するとimportが先頭に行くので苦肉の策
while True:
    import sys
    sys.path.append("../000_mymodule/")
    import logger
    from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
    DEBUG_LEVEL = INFO
    break

INPUT_FRAME_RATE = 30
TIME_LAPSE_FRAME_RATE = 100
OUTPUT_FRAME_RATE = 20

log = logger.Logger("MAIN", level=DEBUG_LEVEL)


def convert_time(ct_time):
    ct_hour = int(ct_time / 3600)
    ct_minute = int((ct_time - ct_hour * 3600) / 60)
    ct_second = int(ct_time - ct_hour * 3600 - ct_minute * 60)
    return f"{ct_hour:02}h{ct_minute:02}m{ct_second:02}sec"


def read_frame(target_paths, frame_queue):
    # ファイルの読み込み
    for path in target_paths:
        capture = cv2.VideoCapture(str(path))

        # ファイルの有無確認
        if not capture.isOpened():
            return
        
        frame_index = 0
        while True:
            result, frame = capture.read()
            # リードの可否確認
            if not result:
                break
            if frame_index % TIME_LAPSE_FRAME_RATE == 0:
                log.info(f"[read] {path}:{convert_time(frame_index/INPUT_FRAME_RATE)}")
                # キューに画像データを渡す
                frame_queue.put(frame)
            frame_index += 1
        capture.release()
    # すべてが終了したらキューにNoneを送り終了させる
    frame_queue.put(None)


def write_frame(frame_queue):
    # VideoWriterオブジェクトを作成
    # 出力はout.mp4
    # リサイズと整合を合わせること
    video_writer = cv2.VideoWriter(
        "out.mp4", cv2.VideoWriter_fourcc("m", "p", "4", "v"), OUTPUT_FRAME_RATE, (1280, 720))

    while True:
        # キューからデータを取得する
        frame = frame_queue.get()
        try:
            # キューにデータが無い場合は終了
            if frame is None:
                break
            else:
                # リサイズ
                frame_resize = cv2.resize(frame, dsize=(1280, 720))
                # 文字入力
                cv2.putText(frame_resize,
                            convert_time(frame_index / INPUT_FRAME_RATE)+":2021/10/26@TKL",
                            (0, 50),
                            cv2.FONT_HERSHEY_PLAIN,
                            3,
                            (0, 0, 0),
                            5,
                            cv2.LINE_AA)

                video_writer.write(frame_resize)
        finally:
            # キューにタスク完了を示す
            frame_queue.task_done()

    video_writer.release()


def main():
    # 時間計測用
    start = time.perf_counter()

    # ファイル取得
    # カレントディレクトリを示す
    target_dir = pathlib.Path(".")
    # MTSファイルを取得、ソートする
    target_paths = sorted(target_dir.glob("*.MTS"))

    # キューの設定
    frame_queue = queue.Queue(maxsize=100)

    read_frame_worker = threading.Thread(
        target=read_frame,
        daemon=True,
        kwargs={"target_paths": target_paths, "frame_queue": frame_queue},)
    read_frame_worker.start()

    write_frame_worker = threading.Thread(
        target=write_frame, daemon=True, kwargs={"frame_queue": frame_queue},)
    write_frame_worker.start()

    # キューの処理が終わるまでブロックする
    read_frame_worker.join()
    write_frame_worker.join()

    log.warn(f"経過時間:{convert_time(time.perf_counter() - start)}")


if __name__ == "__main__":
    main()
