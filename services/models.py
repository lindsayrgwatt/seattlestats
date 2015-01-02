from datetime import datetime

#import urllib
import urllib2
import json
#import datetime
#import pytz
import logging
#import os
#import csv

from django.contrib.gis.db import models
from django.core.exceptions import ObjectDoesNotExist

log = logging.getLogger(__name__)

class PoliceManager(models.GeoManager):
    def police_url(self):
        # Get most recent record or go back two years if does not exist
        try:
            latest = self.latest('date')
            date = latest.date
        except ObjectDoesNotExist:
            now = datetime.now()
            date = datetime(now.year - 2, now.month, now.day, now.hour, now.minute, now.second, now.microsecond)

        url = "https://data.seattle.gov/resource/3k2p-39jp.json?%%24where=event_clearance_date%%20%%3E%%20%%27%d-%d-%d%%20%d:%d:%d%%27&$order=event_clearance_date" % (date.year, date.month, date.day, date.hour, date.minute, date.second)

        return url

    def update_data(self):
        url = self.police_url()

        try:
            response = urllib2.urlopen(url)

            if response.code == 200:
                all_data = json.load(response)

                for data in all_data:
                    if 'event_clearance_description' in data: # Ignore records with no descriptions. Do not know why these appear
                        try:
                            point = fromstr("POINT(%s %s)" % (data['longitude'], data['latitude']))
                            date = datetime.datetime.strptime(data['event_clearance_date'], "%Y-%m-%dT%H:%M:%S")

                            # Use get_or_create so that we never risk creating the same incident twice
                            police_obj, created = Police911Call.objects.get_or_create(
                                                    general_offense_number=data['general_offense_number'],
                                                    defaults={
                                                        'description':data['event_clearance_description'].strip(),
                                                        'group':group,
                                                        'address':data['hundred_block_location'],
                                                        'date':date,
                                                        'point':point
                                                    })


                        except KeyError, e:
                            log.error("Missing key %s in police data for general offense number: %s" % (e, data['general_offense_number']))
            else:
                log.error("Non-200 code getting police data: %s" % str(response.code))
        except urllib2.HTTPError, e:
            log.error("HTTPError getting police data: %s" % e.getcode())

# Sample police data:
# http://data.seattle.gov/resource/3k2p-39jp.json?%24where=event_clearance_date%20%3E%20%272014-12-17%2000:00:00%27&$order=event_clearance_date%20DESC

# Issues with Seattle police data:
# 1) Descriptions of issues change across same General Offense Number (look up 201399972 in both data sets)
# 2) Multiple duplicate records in incident reports
# 3) Sometimes lat/lng for Police911Incidents is (0,0)

# Police 911 calls that generated a response
class Police911Response(models.Model):
    general_offense_number = models.BigIntegerField(unique=True)
    cad_event_number = models.BigIntegerField(default=0)

    description = models.CharField(max_length=75) # Event Clearance Description and Initial Type Description
    initial_description = models.CharField(max_length=75, blank=True, default="") # Initial description, if available
    group = models.CharField(max_length=75) # Event Clearance Group
    initial_group = models.CharField(max_length=75, blank=True, default="") # Initial group, if available
    subgroup = models.CharField(max_length=75) # Event Clearance Subgroup
    initial_subgroup = models.CharField(max_length=75, blank=True, default="") # Initial subgroup, if available
    
    date = models.DateTimeField() # Event clearance date
    
    address = models.CharField(max_length=75) # Hundred block location
    zone_beat = models.CharField(max_length=10) # Zone/beat
    district_sector = models.CharField(max_length=10) # District/sector

    point = models.PointField(help_text="Represented as 'POINT(longitude, latitude)'")
    objects = PoliceManager()
    
    def __unicode__(self):
        return str(self.general_offense_number) + " :: " + self.description + " :: "+ str(self.date)
    
    def lat(self):
        return self.point.get_coords()[1]
    
    def lng(self):
        return self.point.get_coords()[0]

    class Meta:
        ordering = ['-date', '-general_offense_number'] # Some general_offense_numbers have extra digit so 10X larger than others
