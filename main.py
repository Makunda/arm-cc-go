import sys
import sys, time

from Daemon import Daemon
from secrets.Secrets import DAEMON_FILE


class MyDaemon(Daemon):
    def run(self):
        while True:
            time.sleep(1)


if __name__ == "__main__":
    daemon = MyDaemon(DAEMON_FILE)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'run' == sys.argv[1]:
            daemon.restart()
        else:
            print(f"Unknown command: {sys.argv}")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart|run" % sys.argv[0])
        sys.exit(2)
