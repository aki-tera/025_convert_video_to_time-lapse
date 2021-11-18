import pathlib
import queue
import threading

import cv2

import json


# グローバル変数を示す
INPUT_FILE = ""
TIME_LAPSE_FRAME_RATE = 0
OUTPUT_FRAME_RATE = 0
OUTPUT_WIDTH = 0
OUTPUT_HEIGHT = 0
DISPLAY_STRING = ""


def convert_time(ct_time):
    """Convert seconds to hours, minutes, and seconds.

    Args:
        ct_time (int/float):Seconds to be converted.

    Returns:
        string: Hours, minutes, seconds converted from seconds.
    """
    ct_hour = int(ct_time / 3600)
    ct_minute = int((ct_time - ct_hour * 3600) / 60)
    ct_second = int(ct_time - ct_hour * 3600 - ct_minute * 60)
    return f"{ct_hour:02}h{ct_minute:02}m{ct_second:02}sec"


def read_frame(target_paths, frame_queue):
    """Extract a specific video frame from the videos indicated by the paths.

    Args:
        target_paths (list): Input video including path
        frame_queue (instance): a FIFO queue
    """
    # タイムラプスで示す経過時間
    total_frame_index = 0

    # ファイルの読み込み
    for path in target_paths:
        # フレームレートの取得
        capture = cv2.VideoCapture(str(path))
        
        # ファイルの有無確認
        if not capture.isOpened():
            return
        
        # 入力ファイルのfpsを取得
        frame_fps = capture.get(cv2.CAP_PROP_FPS)

        # 個々のビデオの経過時間
        frame_index = 0

        while True:
            
            result, frame = capture.read()
            # リードの可否確認
            if not result:
                break
            if frame_index % TIME_LAPSE_FRAME_RATE == 0:
                
                # キューに画像データを渡す
                frame_queue.put([total_frame_index, frame_fps, frame])

            frame_index += 1
            total_frame_index += 1
            
        capture.release()
    # すべてが終了したらキューにNoneを送り終了させる
    frame_queue.put([total_frame_index, frame_fps, None])


def write_frame(frame_queue):
    """Output a video of a new size by adding time and text to the input frame.

    Args:
        frame_queue (list): total_frame_index, frame_fps, frame
    """
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
                
                # リサイズ
                frame_resize = cv2.resize(frame, dsize=(OUTPUT_WIDTH, OUTPUT_HEIGHT))
                # 文字入力
                cv2.putText(frame_resize,
                            # 出力する文字列
                            convert_time(total_frame_index / frame_fps) + DISPLAY_STRING,
                            # 表示位置、文字列の右下
                            (0, 50),
                            # フォントの種類
                            cv2.FONT_HERSHEY_PLAIN,
                            # 文字のスケール
                            3.0,
                            # 文字の色(青, 緑, 赤)
                            (255, 255, 255),
                            # 文字の選の太さ
                            5,
                            # 文字を描画するアルゴリズム
                            cv2.LINE_AA)

                video_writer.write(frame_resize)
                
        finally:
            # キューにタスク完了を示す
            frame_queue.task_done()
    video_writer.release()


def main():

    # jsonファイルの設定ファイル読み込み
    global INPUT_FILE
    global TIME_LAPSE_FRAME_RATE
    global OUTPUT_FRAME_RATE
    global OUTPUT_WIDTH
    global OUTPUT_HEIGHT
    global DISPLAY_STRING

    setting = json.load(open("setting.json", "r", encoding="utf-8"))
    INPUT_FILE = setting["SEARCH_FILE"]["NAME"]
    TIME_LAPSE_FRAME_RATE = setting["INPUT_FILE"]["TIME_LAPSE_SPEED"]
    OUTPUT_FRAME_RATE = setting["OUTPUT_FILE"]["FRAME_RATE"]
    OUTPUT_WIDTH = setting["OUTPUT_FILE"]["OUTPUT_WIDTH"]
    OUTPUT_HEIGHT = setting["OUTPUT_FILE"]["OUTPUT_HEIGHT"]
    DISPLAY_STRING = setting["DISPLAY"]["STRING"]

    # ファイル取得
    # カレントディレクトリを示す
    target_dir = pathlib.Path(".")
    # MTSファイルを取得、ソートする
    target_paths = sorted(target_dir.glob(INPUT_FILE))

    if target_paths:
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

    else:
        print(f"There is no videos named {INPUT_FILE}.")


if __name__ == "__main__":
    main()
