"""
logcheck_syslog.py - Syslog parser and checker for Datadog Agent

Datadog implementation of logcheck.  You can send unknown logs into Datadog.

Datadog: https://www.datadoghq.com/
logcheck: http://logcheck.alioth.debian.org/

Usage:
    1. Add dd-agent user into adm group to read syslog
       adduser dd-agent adm
    2. Add dd-agent user into logcheck group to read logcheck ignore rules
       adduser dd-agent logcheck
    3. Write as follows into your datadog.conf
       dogstreams: /var/log/syslog:/path/to/logcheck_syslog.py:logcheck
    4. Restart datadog-agent
       service datadog-agent restart
"""

import re
import socket
from datetime import datetime
import glob
from checks import AgentCheck


# Constants
EVENT_TYPE = "logcheck.syslog"
EVENT_TITLE = "System Events on {}".format(socket.getfqdn())
LINE_REGEXP = re.compile(r'^(\w{3} \d+? [\d:]+?) \S+? (.*)$')


class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('hello.japan', 1)


# Load logcheck ignore rules
rules = set()
for file in glob.iglob("/etc/logcheck/ignore.d.server/*"):
    with open(file) as f:
        for regexp in f:
            regexp = regexp.rstrip()
            if len(regexp) == 0:
                break

            # Replace POSIX character class
            regexp = regexp.replace("[:alnum:]", r"0-9A-Za-z")
            regexp = regexp.replace("[:alpha:]", r"A-Za-z")
            regexp = regexp.replace("[:blank:]", r"\s")
            regexp = regexp.replace("[:digit:]", r"\d")
            regexp = regexp.replace("[:graph:]", r"!-~")
            regexp = regexp.replace("[:lower:]", r"a-z")
            regexp = regexp.replace("[:print:]", r"!-~ ")
            regexp = regexp.replace("[:punct:]", r"!\"#$%&'()*+,./:;<=>?@\[\\\]^`{|}~")
            regexp = regexp.replace("[:space:]", r"\s")
            regexp = regexp.replace("[:upper:]", r"A-Z")
            regexp = regexp.replace("[:xdigit:]", r"0-9A-Fa-f")

            rules.add(re.compile(regexp))


def logcheck(logger, line):
    if len(line) == 0:
        return None

    logger.debug(line)
    for rule in rules:
        if rule.search(line):
            return None

    # Prepare event object
    event = {
        "event_type": EVENT_TYPE,
        "msg_title": EVENT_TITLE,
        "msg_text": line,
        "alert_type": "error",
    }

    # Parse line
    try:
        date_str, msg = LINE_REGEXP.match(line).groups()
        event["msg_text"] = msg
        try:
            event["timestamp"] = _parse_datetime(dt_str)
        except Exception:
            None
    except:
        None

    return [event]


def _parse_datetime(dt_str):
    dt = datetime.strptime(dt_str, "%b %d %H:%M:%S")

    # Set correct year value
    if (dt.month > datetime.now().month):
        dt.replace(datetime.now().year - 1)
    else:
        dt.replace(datetime.now().year)

    # Return unix timestamp
    return int(dt.strftime('%s'))


# Test is not implemented yet
def test():
    return True

if __name__ == '__main__':
    test()