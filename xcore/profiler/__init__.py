import hotshot
import os
import time

def profile(log_file_path):
    """Profile some callable.

    modified version of https://code.djangoproject.com/wiki/ProfilingDjango

    This decorator uses the hotshot profiler to profile some callable (like
    a view function or method) and dumps the profile data somewhere sensible
    for later processing and examination.

    It takes one argument, the profile log name. If it's a relative path, it
    places it under the PROFILE_LOG_BASE. It also inserts a time stamp into the
    file name, such that 'my_view.prof' become 'my_view-20100211T170321.prof',
    where the time stamp is in UTC. This makes it easy to run and compare
    multiple trials.
    """

    if not os.path.isabs(log_file_path):
        log_file = os.path.join("/tmp/", log_file_path)

    def _outer(f):
        def _inner(*args, **kwargs):
            # Add a timestamp to the profile output when the callable
            # is actually called.
            (base, ext) = os.path.splitext(log_file)
            base = base + "-" + time.strftime("%Y%m%dT%H%M%S", time.gmtime())
            final_log_file = base + ext

            prof = hotshot.Profile(final_log_file)
            try:
                ret = prof.runcall(f, *args, **kwargs)
            finally:
                prof.close()
            return ret

        return _inner
    return _outer


def profile_result():
    """
    Print profile results
    """
    from django.bin.profiling import gather_profile_stats
    import pstats
    gather_profile_stats.gather_stats("/tmp")
    s=pstats.Stats("/tmp/.agg.prof")
    s.print_stats()

