from multiprocessing import Queue, Process
import time

def f2(q):
    print("start f2")
    time.sleep(3)
    # 3秒後に、キューに値を渡します.
    q.put([42, None, "Hello"])

if __name__ == "__main__":
    # スレッド間でやり取りするためのキューを作成します.
    q = Queue()
    # キューを引数に渡して、サブプロセスを作成します.
    p = Process(target=f2, args=(q,))
    # サブプロセスを開始します.
    p.start()
    # q.get()できるまで待ちます.
    print(q.get())
    # サブプロセス完了を待ちます.
    p.join()