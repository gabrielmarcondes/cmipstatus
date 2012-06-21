from django.db import models
from datetime import datetime
from os.path import join
from os import getenv
from django.contrib.auth.models import User


class People(User):
    name = models.CharField(max_length=100)
    about = models.TextField(default='INPE GMAO Researcher')
    photo = models.ImageField(max_length=1048, upload_to='media', default='profile_default.png')

    def __unicode__(self):
        return self.name


class Experiment(models.Model):
    name = models.CharField(max_length=15)

    def get_status(self, tupa_data):
        done, total = check_restart_list(self.name, '')
        current = check_status(self.name, '', tupa_data)
        return done, total, current

    def __unicode__(self):
        return self.name


class Member(models.Model):
    name = models.CharField(max_length=3)
    exp = models.ForeignKey('Experiment')

    def get_status(self,tupa_data):
        done, total = check_restart_list(self.exp.name, self.name)
        current = check_status(self.exp.name, self.name, tupa_data)
        return done, total, current

    def __unicode__(self):
        return self.name

FETCHED_DATA_DIR = join(getenv('HOME'), 'cmipsite', 'cmipstatus', 'fetched_data')
RESTART_LIST_FILE = "RESTARTLIST.{0}.tmp"

def check_restart_list(exp_name, member_name):
    print "checking restart count..."
    restart_list = open(join(FETCHED_DATA_DIR, RESTART_LIST_FILE.format(exp_name+member_name)), 'r')
    restarts = 0
    done = 0
    error = 0
    for line in restart_list:
        restarts += 1
        if 'END' in line:
            done += 1
        if 'ERR' in line:
            error += 1
    if error > 0:
        done *= -1
    return done, restarts


def check_status(exp_name, member_name, tupa_data):
    print "checking runnning stats"
    if tupa_data:
        lines = tupa_data.split('\n')
        lines.pop(0)
        for line in lines:
            columns = line.split()
            if len(columns) > 0 and columns[1].endswith(exp_name+member_name):
                return columns
    return [None, 'M_'+exp_name+member_name, None, None, '0%']

RUNNING_STATS_FILE = 'running_stats.txt'

def get_tupa_data():
    f = open(join(FETCHED_DATA_DIR, RUNNING_STATS_FILE), 'r')
    query_result = f.read()
    f.close()
    return query_result
