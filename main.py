import sys
import sys, time

from Daemon import Daemon
from secrets.Secrets import DAEMON_FILE


if __name__ == "__main__":
    daemon = Daemon()
    usageMessage = f"Usage: {sys.argv[0]} (start|stop|restart|status|reload|version)"
    if len(sys.argv) == 2:
        choice = sys.argv[1]
        if choice == "start":
            daemon.start()
        elif choice == "stop":
            daemon.stop()
        elif choice == "restart":
            daemon.restart()
        elif choice == "status":
            daemon.status()
        elif choice == "reload":
            daemon.reload()
        elif choice == "version":
            daemon.version()
        else:
            print("Unknown command.")
            print(usageMessage)
            sys.exit(1)
        sys.exit(0)
    else:
        print(usageMessage)
        sys.exit(1)