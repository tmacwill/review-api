#!/usr/bin/env python

import os
import sys

app = os.path.dirname(os.path.realpath(__file__)) + '/..'
sys.path.append(app)

import kata.config
import kata.db
import kata.schema

config_path = os.environ.get('CONFIG', app + '/api/config.ini')
kata.config.initialize(config_path)
kata.schema.reset('%s/schema' % app)

import api.model.user
api.model.user.User.create({
    'facebook_id': '10153798446717889',
    'facebook_token': 'abc',
    'email': 'tmacw09@gmail.com',
    'name': 'Tommy MacWilliam',
    'token': 'de855gppzz5jzx22'
})

import api.model.tag
kata.db.execute('''
    INSERT INTO %s
        (name)
    VALUES
        ('CS50'), ('pset1'), ('mario')
''' % api.model.tag.Tag.__table__)
