# coding: utf-8
from ephem import readtle, Observer
from datetime import datetime, timedelta
from geopy.distance import distance
from math import degrees
from tqdm import tqdm
from django.contrib.gis.geos import Point
from .models import SubsatellitePoint

class DateTimeRange(object):
    def __init__(self, start, stop, step=1):
        self.start = start
        self.stop = stop
        self.step = step

    def __len__(self):
        start = self.start.timestamp()
        stop = self.stop.timestamp()
        return int((stop - start) / self.step)

    def __iter__(self):
        return self

    def __next__(self):
        if self.start <= self.stop:
            start = self.start
            self.start += timedelta(seconds=self.step)
            return start, self.start
        else:
            raise StopIteration()


class DayRange(DateTimeRange):
    def __init__(self, *args):
        super(DayRange, self).__init__(*args)
        self.step *= 86400

    def __next__(self):
        if self.start < self.stop:
            start = self.start
            self.start += timedelta(seconds=self.step)
            return start, self.start
        else:
            raise StopIteration()


def chunker(chunk_size, iterable):
    count = len(iterable)//chunk_size
    for i in range(count+1):
        yield iterable[:chunk_size]
        iterable = iterable[chunk_size:]


def update_track(tle, delta=timedelta(days=3), step_in_sec=1):
    start = tle.datetime_in_lines
    stop = start+delta
    SubsatellitePoint.objects.filter(date_time__gte=start).delete()
    iss = readtle(tle.title_line, tle.line1, tle.line2)
    for loc_start, loc_stop in tqdm(DayRange(start, stop, 1), leave=True):
        subsat_points = []
        print('\n{}'.format(loc_start.date()))
        for iss_time, next_time in tqdm(DateTimeRange(loc_start, loc_stop, step_in_sec), leave=True):
            iss.compute(iss_time)
            sublong, sublat = map(degrees, (iss.sublong, iss.sublat))
            subsat_points.append(SubsatellitePoint(date_time=iss_time, location=Point(sublong, sublat), tle=tle))

        yield loc_start.date(), subsat_points