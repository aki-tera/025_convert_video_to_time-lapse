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
    DEBUG_LEVEL = DEBUG
    break

TIME_LAPSE_FRAME_RATE = 5

OUTPUT_FRAME_RATE = 20
OUTPUT_WIDTH = 1280
OUTPUT_HEIGHT = 720

OUTPUT_DISPLAY_STRING = ":2021/10/26"


log = logger.Logger("MAIN", level=DEBUG_LEVEL)


def convert_time(ct_time):
    ct_hour = int(ct_time / 3600)
    ct_minute = int((ct_time - ct_hour * 3600) / 60)
    ct_second = int(ct_time - ct_hour * 3600 - ct_minute * 60)
    return f"{ct_hour:02}h{ct_minute:02}m{ct_second:02}sec"


def read_frame(target_paths, frame_queue):
    total_frame_index = 0

    # ファイルの読み込み
    for path in target_paths:
        # フレームレートの取得
        capture = cv2.VideoCapture(str(path))
        frame_fps = capture.get(cv2.CAP_PROP_FPS)

        # ファイルの有無確認
        if not capture.isOpened():
            return

        frame_index = 0
        while True:
            log.debug("[read]START")
            result, frame = capture.read()
            # リードの可否確認
            if not result:
                break
            if frame_index % TIME_LAPSE_FRAME_RATE == 0:
                log.info(f"[read] {path}:{convert_time(frame_index/frame_fps)}")
                # キューに画像データを渡す
                frame_queue.put([total_frame_index, frame_fps, frame])

            frame_index += 1
            total_frame_index += 1
            log.debug("[read]END")
        capture.release()
    # すべてが終了したらキューにNoneを送り終了させる
    frame_queue.put([frame_index, frame_fps, None])


def write_frame(frame_queue):
    # VideoWriterオブジェクトを作成
    # 出力はout.mp4
    # リサイズと整合を合わせること
    video_writer = cv2.VideoWriter("out.mp4",
                                   cv2.VideoWriter_fourcc("m", "p", "4", "v"),
                                   OUTPUT_FRAME_RATE,
                                   (OUTPUT_WIDTH, OUTPUT_HEIGHT))

    while True:
        # キューからデータを取得する
        total_frame_index, frame_fps, frame = frame_queue.get()
        try:
            # キューにデータが無い場合は終了
            if frame is None:
                break
            else:
                log.debug("[write]START")
                # リサイズ
                frame_resize = cv2.resize(frame, dsize=(OUTPUT_WIDTH, OUTPUT_HEIGHT))
                # 文字入力
                cv2.putText(frame_resize,
                            # 出力する文字列
                            convert_time(total_frame_index / frame_fps) + OUTPUT_DISPLAY_STRING,
                            # 表示位置、文字列の右下
                            (0, 50),
                            # フォントの種類
                            cv2.FONT_HERSHEY_PLAIN,
                            # 文字のスケール
                            3.0,
                            # 文字の色(青, 緑, 赤)
                            (0, 0, 0),
                            # 文字の選の太さ
                            5,
                            # 文字を描画するアルゴリズム
                            cv2.LINE_AA)

                video_writer.write(frame_resize)
                log.debug("[write]END")
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
    frame_queue = queue.Queue(maxsize=10)

    # スレッド処理の設定
    # 但し並列処理と変わらない？？
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

    log.info(f"経過時間:{convert_time(time.perf_counter() - start)}")


if __name__ == "__main__":
    main()
