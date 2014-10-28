CC=ghc

all: multicast-send multicast-receive

multicast-send:	multicast-send.hs
	$(CC) $@

multicast-receive:	multicast-receive.hs
	$(CC) $@

clean:
	rm multicast-send.o multicast-send.hi multicast-send multicast-receive.o multicast-receive.hi multicast-receive

