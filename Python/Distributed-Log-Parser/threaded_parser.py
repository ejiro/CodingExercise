import threading
import Queue
import re
import collections
from datetime import datetime
import time
import sys
import os


class UserLog(object):
    """A user logs corresponding to individual logged item pertaining, such as time stamp and user id
    """
    def __init__(self, userid, timestamp):
        self.userid = userid
        self.timestamp = timestamp

    def get_user_id(self):
        line = self.userid
        if line is None:
            return None
        return line.split("=")[1].strip()[:-1]

    def get_date(self):
        line = self.timestamp
        if line is None:
            return None
        date_str = regex_date_pattern.findall(line.strip())
        if len(date_str) > 0:
            d = datetime.strptime(date_str[0], '%d / %b / %Y: %H: %M: %S -0300')
            return d
        else:
            return None

    def __repr__(self):
        return repr("UserLog(" + self.get_user_id() + ")")

    def __hash__(self):
        return hash(self.get_user_id())

    def __eq__(self, other):
        return self.get_date() == other.get_date()


class Worker(threading.Thread):
    """A worker thread that takes log file name from a log queue, find all unique user id and time stamp
        in them, output individual logs in their respective file, using user id as file name, then
        reports back the results in the result queue

        The thread an be stop by using join()
    """
    def __init__(self, log_q, result_q):
        super(Worker, self).__init__()
        self.log_q = log_q
        self.result_q = result_q
        self.stop_request = threading.Event()

    def run(self):
        """
        This function executes in the context of this worker thread, it utilizes a threading event to notify the
        worker thread to stop.  It receive work to be done via the log queue which uses the blocking 'get' with a
        timeout so no CPU cycles are waisted waiting.  The timeout ensures that the threading stop request event
        is continuously checked.
        :return:
        """
        while not self.stop_request.isSet():
            try:
                # Block this thread until there is work to be done
                # throws a queue empty after timeout if no work to be done
                logfile = self.log_q.get(True, 0.005)
                if logfile is None:
                    break

                # Loop thru the generator
                num_logs = 0
                for user_log in self.get_user_log_generator(logfile):
                    #user_logs.append(user_log)
                    num_logs += 1

                # Report back to main thread that work is done for this log file
                self.result_q.put((self.name, logfile))

            except Queue.Empty:
                continue

    def join(self, timeout=None):
        """
        This function is executed from the context of the main thread.  It indicates to the thread to stop running
        giving the timeout
        :param timeout:
        :return:
        """
        self.stop_request.set()
        super(Worker, self).join(timeout)

    def get_user_log_generator(self, logfile):
        """ Given a log file name, yields the user id and time stamps of every entry.
            For optimization, a particular user log is bundle in bunch sizes are output-ed to a
            text file of that specific user
        :rtype : yields UserLog object
        :param logfile:
        """
        # Size of the bundle before outputing the individual user logs to its file
        # To prevent trashing your hardrive
        bunch_size = 1000000     # Experiment with different sizes

        # Dictionary with a list backing store for holding each log
        bunch_store = collections.defaultdict(list)

        # Using a lazy reference to this log file object, access each line and process it
        bunch_counter = 0
        with open(logfile, "rb") as in_file:
            for line in in_file:
                bunch_counter += 1
                # Using a regex searching mechanism, determine if this line pertains to the userid
                if regex_user_id_search(line) and prev != "":
                    # Create a UserLog object using this current line and the previous line
                    user_log = UserLog(line.strip(), prev.strip())

                    # Add to the dictionary hash of this specific user
                    user_data = user_log.timestamp+"\n"+user_log.userid+"\n"
                    bunch_store[user_log.get_user_id()].append(user_data)

                    # Output to the user file if bunch size is reached
                    if bunch_counter >= bunch_size:
                        for uid, data_list in bunch_store.iteritems():
                            with open("tmp/"+uid+".txt", "a") as out_file:
                                out_file.writelines("".join(data_list))

                        print "processing bundle for log: ", logfile,
                        print "time: ", datetime.now()

                        # Reset bundle and counter
                        bunch_store = collections.defaultdict(list)
                        bunch_counter = 0

                    # yield the user log - no particular reason actually
                    # print user_data
                    yield user_log
                else:
                    # save a reference of previous line, perhaps the timestamp line of the user
                    prev = line

            # Output to the user file, the remainder data in the bunch store
            for uid, data_list in bunch_store.iteritems():
                with open("tmp/"+uid+".txt", "a") as out_file:
                    out_file.writelines("".join(data_list))


def compare_date(date1, date2):
    """
    Static functions that returns true if date1 is lesser than date2
    """
    if date1 is None:
        return False
    if date1 is None:
        return True
    return date1 <= date2

#######
# Global variables
regex_user_id_pattern = re.compile(r"userid")
regex_user_id_search = regex_user_id_pattern.search
regex_date_pattern = re.compile(r'\[(.+?)\]', flags=re.DOTALL)


'''
Sample entry:
++++++++++++++++++

177.126.180.83 - - [15 / Aug / 2013: 13: 54: 38 -0300] "GET /meme.jpg HTTP / 1.1" 200 2148 "-"
"userid = 5352b590-05ac-11e3-9923-c3e7d8408f3a"
177.126.180.83 - - [15 / Aug / 2013: 13: 54: 38 -0300] "GET /lolcats.jpg HTTP / 1.1" 200 5143 "-"
"userid = f85f124a-05cd-11e3-8a11-a8206608c529"
177.126.180.83 - - [15 / Aug / 2013: 13: 57: 48 -0300] "GET /lolcats.jpg HTTP / 1.1" 200 5143 "-"
"userid = 5352b590-05ac-11e3-9923-c3e7d8408f3a"


Example of output:
++++++++++++++++++

3 On the server (for example) there is a file called / tmp / 5352b590-05ac-11e3-9923-c3e7d8408f3a lines containing:
----------

177.126.180.83 - - [15 / Aug / 2013: 13: 54: 38 -0300] "GET /meme.jpg HTTP / 1.1" 200 2148 "-"
"userid = 5352b590-05ac-11e3-9923-c3e7d8408f3a"
177.126.180.83 - - [15 / Aug / 2013: 13: 57: 48 -0300] "GET /lolcats.jpg HTTP / 1.1" 200 5143 "-"
"userid = 5352b590-05ac-11e3-9923-c3e7d8408f3a"

2 On the server (for example) there is a file called / tmp / f85f124a-05cd-11e3-8a11-a8206608c529 that contains the line:
-----------

177.126.180.83 - - [15 / Aug / 2013: 13: 54: 38 -0300] "GET /lolcats.jpg HTTP / 1.1" 200 5143 "-"
"userid = f85f124a-05cd-11e3-8a11-a8206608c529"
'''

# it should be runnable like this:
# python threaded_parser.py logfile1 logfile2 logfile3 logfile4
__author__ = 'Ejiro'
if __name__ == '__main__':

    print sys.argv
    # Get the logs
    LOGS = sys.argv[1:]
    if len(LOGS) <= 0:
        # usage
        #LOGS = ["log1.txt", "log2.txt"]
        print 'usage: $python threaded_parser.py logfile1 logfile2 logfile3 logfile4\n'
        sys.exit(2)

    # Validate output directory
    tmp_dir = "tmp"
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    # Create a single job queue for all threads
    log_queue = Queue.Queue()
    result_queue = Queue.Queue()

    # Create the thread pool
    thread_pool = []
    for i in range(4):
        print "Creating thread ", i
        w = Worker(log_queue, result_queue)
        w.daemon = True
        thread_pool.append(w)

    # Starts threads
    for thread in thread_pool:
        thread.start()

    # Give the workers threads log files to process - eg simulating the distributed environment
    log_count = len(LOGS)
    for LOG in LOGS:
        print "Adding LOG to queue for processing: ", LOG
        log_queue.put(LOG)

    print "Please wait..."

    # Now get all the results
    while log_count > 0:
        # Blocking 'get' from result log Queue.
        result = result_queue.get()
        print 'From thread %s: parsing completed for log file: %s' % (result[0], result[1])
        log_count -= 1

    # Ask threads to die and wait for them to do it
    for thread in thread_pool:
        thread.join()

    print "Done"