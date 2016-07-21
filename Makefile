# Makefile test

.PHONY: all
all: ;

# install sample check and restart DD-agent
.PHONY: install
install:
	@echo
	@echo Not deployed yet.

# setting sample and restart
.PHONY: set_logcheck
set_sample: logcheck_syslog restart
	@echo wait 10 seconds to DD-agent to stabilize then run info command.
	sleep 10
	/etc/init.d/datadog-agent info

# run datadog-agent stop command
.PHONY: stop
stop:
	/etc/init.d/datadog-agent stop

# run datadog-agent start command
.PHONY: start
start:
	/etc/init.d/datadog-agent start

# run datadog-agent restart command
.PHONY: restart
restart:
	/etc/init.d/datadog-agent restart

# run datadog-agent info command
.PHONY: info
info:
	/etc/init.d/datadog-agent info

# set sample checks to /etc/dd-agent
.PHONY: logcheck_syslog
logcheck_syslog:
	cp conf.d/logcheck_syslog.yaml /etc/dd-agent/conf.d/
	cp checks.d/logcheck_syslog.py /etc/dd-agent/checks.d/

# Cleaning all unwanted files
.PHONY: clean
clean:
	rm -f *.pyc