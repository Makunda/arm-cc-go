#!/usr/bin/env python
import signal
import threading

import psutil

from Server import Server
import sys, os, time, atexit
from signal import SIGTERM
from typing import IO

from secrets.Secrets import STD_OUT_FILE, STD_ERR_FILE


class Daemon(object):
    """
    Usage: - create your own a subclass Daemon class and override the run() method. Run() will be periodically the calling inside the infinite run loop
           - you can receive reload signal from self.isReloadSignal, and then you have to set back self.isReloadSignal = False
    """

    def __init__(self, pidfile, stdin='/dev/null', stdout=STD_OUT_FILE, stderr=STD_ERR_FILE):
        self.ver = 1.0  # version
        self.pauseRunLoop = 0  # 0 means none pause between the calling of run() method.
        self.restartPause = 1  # 0 means without a pause between stop and start during the restart of the daemon
        self.waitToHardKill = 3  # when terminate a process, wait until kill the process with SIGTERM signal
        self.isReloadSignal = False
        self._canDaemonRun = True
        self.processName = os.path.basename(sys.argv[0])
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def _sigterm_handler(self, signum, frame):
        self._canDaemonRun = False

    def _reload_handler(self, signum, frame):
        self.isReloadSignal = True

    def _makeDaemon(self):
        """
        Make a daemon, do double-fork magic.
        """
        try:
            pid = os.fork()
            if pid > 0:
                # Exit first parent.
                sys.exit(0)
        except OSError as e:
            m = f"Error: Fork #1 failed: {e}"
            print(m)
            sys.exit(1)

        # Decouple from the parent environment.
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # Do second fork.
        try:
            pid = os.fork()
            if pid > 0:
                # Exit from second parent.
                sys.exit(0)
        except OSError as e:
            m = f"Error: Fork #2 failed: {e}"
            print(m)
            sys.exit(1)

        m = "The daemon process is going to background."
        print(m)
        # Redirect standard file descriptors.
        sys.stdout.flush()
        sys.stderr.flush()

        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as pid_file:
            pid_file.write("%s\n" % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def _getProces(self):
        procs = []
        for p in psutil.process_iter():
            if self.processName in [part.split('/')[-1] for part in p.cmdline()]:
                # Skip  the current process
                if p.pid != os.getpid():
                    procs.append(p)
        return procs

    def start(self):
        """
        Start daemon.
        """
        # Handle signals
        signal.signal(signal.SIGINT, self._sigterm_handler)
        signal.signal(signal.SIGTERM, self._sigterm_handler)
        signal.signal(signal.SIGHUP, self._reload_handler)
        # Check if the daemon is already running.
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = open(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Daemonize the main process
        self._makeDaemon()
        # Start a infinitive loop that periodically runs run() method
        self._infiniteLoop()

    def version(self):
        m = f"The daemon version {self.ver}"
        print(m)

    def status(self):
        """
        Get status of the daemon.
        """
        # Get the pid from the pidfile
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())

        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon is not running.\n"
            sys.stderr.write(message % self.pidfile)
            return  # not an error in a restart
        else:
            try:
                proc = psutil.Process(pid)
                message = "Daemon is in %s mode with PID [%s].\n"
                sys.stdout.write(message % (str(proc.status()), pid))
            except:
                message = "Failed to get the status of daemon with PID [%s].\n"
                sys.stderr.write(message % pid)
                self.delpid()
                return  # not an error in a restart

    def reload(self):
        """
        Reload the daemon.
        """
        procs = self._getProces()
        if procs:
            for p in procs:
                os.kill(p.pid, signal.SIGHUP)
                m = f"Send SIGHUP signal into the daemon process with PID {p.pid}."
                print(m)
        else:
            m = "The daemon is not running!"
            print(m)

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    self.delpid()
            else:
                print(f"Failed to kill the daemon process: {str(err)}")
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon.
        """
        self.stop()
        if self.restartPause:
            time.sleep(self.restartPause)
        self.start()

    def _infiniteLoop(self):
        try:
            Server.run()
        except Exception as e:
            m = f"Run method failed: {e}"
            sys.stderr.write(m)
            sys.exit(1)
    # this method you have to override
