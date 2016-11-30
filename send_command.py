import argparse

import zmq

if __name__ == "__main__":

  parser = argparse.ArgumentParser(description="LED Matrix Animation Remote")
  parser.add_argument("command", metavar="C", type=str)

  args = parser.parse_args()

  context = zmq.Context()
  socket = context.socket(zmq.PUSH)
  socket.connect("tcp://localhost:%s" % 5555)
  socket.send(args.command)
