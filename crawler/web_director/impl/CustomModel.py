# !/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################
#
# (c) Copyright University of Southampton, 2022
# # Copyright in this software belongs to University of Southampton,
# Highfield, University Road, Southampton SO17 1BJ
#
# Created By : Sohaib Karous
# Created Date : 2022/08/18
# Project : FloraGuard
# ######################################################################

from crawler.web_director.abc import ModelAbstractClass


class CustomModel(ModelAbstractClass.ModelABC):

    def __init__(self, model, acceptance):
        self.acceptance = acceptance
        self.model = model

    def accept(self, comments):
        return self.acceptance(self.model.predict(comments))
