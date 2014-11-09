import uuid
import datetime
from random import randrange


def log_generator(logfile, rand_uuid, num_log=100000):
    start_date = datetime.datetime(100, 1, 1, 11, 34, 59)
    curr_time = datetime

    bunch_size = 1000000     # Experiment with different sizes
    bunch = []
    with open(logfile, "a") as logfile:
        for i in range(num_log):
            random_id = rand_uuid[randrange(len(rand_uuid)+1)]

            curr_date = start_date + curr_time.timedelta(0, 3)  # days, seconds, then other fields.
            start_date = curr_date
            display_date = curr_date.time().strftime("%d / %b / %Y: %H: %M: %S -0300")

            timestamp_line = '177.126.180.83 - - ['+display_date+'] "GET /lolcats.jpg HTTP / 1.1" 200 5143 "-"'
            user_id_line = '\"userid = '+str(random_id)+'\"'

            bunch.append(timestamp_line+"\n"+user_id_line+"\n")
            if len(bunch) == bunch_size:
                logfile.writelines("".join(bunch))
                bunch = []

        logfile.writelines("".join(bunch))


__author__ = 'Ejiro'
if __name__ == '__main__':

    # make a random UUID
    rand_uuid = [uuid.uuid4() for i in range(11)]

    # Generate logs
    log_generator("log_test3.txt", rand_uuid, 5)
    log_generator("log_test4.txt", rand_uuid, 9)
    print ""
