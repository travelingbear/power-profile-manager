CC = gcc
CFLAGS = -Wall -Wextra -O2
DAEMON = power-profiled
CTL = power-profile-ctl

all: $(DAEMON) $(CTL)

$(DAEMON): power-profiled.c
	$(CC) $(CFLAGS) -o $(DAEMON) power-profiled.c

$(CTL): power-profile-ctl.c
	$(CC) $(CFLAGS) -o $(CTL) power-profile-ctl.c

clean:
	rm -f $(DAEMON) $(CTL)

install: $(DAEMON) $(CTL)
	install -m 755 $(DAEMON) /usr/local/bin/
	install -m 755 $(CTL) /usr/local/bin/

uninstall:
	rm -f /usr/local/bin/$(DAEMON)
	rm -f /usr/local/bin/$(CTL)

.PHONY: all clean install uninstall
