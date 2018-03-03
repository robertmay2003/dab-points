#!/bin/bash

allwait() {
  PID=$1
  while ps -p "$PID" > /dev/null; do sleep 1; done
}

while true; do afplay $1 &  echo $! >/tmp/cu-song.pid;allwait "$(cat /tmp/cu-song.pid)"; done
