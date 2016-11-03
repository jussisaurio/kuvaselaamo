
# -*- coding: utf-8 -*-

import logging
import random
from django import template

LOG = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag
def finna_image(img_id, w=0, h=0):
  if w != 0 and h != 0:
    url = 'https://finna.fi/Cover/Show?id=%s&w=%d&h=%d' % (img_id, w, h)
  else:
    url = 'https://finna.fi/Cover/Show?id=%s&fullres=1&index=0' % img_id
  return url


@register.filter
def finna_default_image_url(img_id):
  return 'https://finna.fi/Cover/Show?id=%s&fullres=1&index=0' % img_id


@register.filter
def display_images(collection):
  ids = list(collection.records.all().values_list('record_id', flat=True))
  record_count = len(ids)
  image_urls = []

  if record_count == 0:
    image_urls.append('/static/hkm/img/collection_default_image.png')
  elif record_count < 3:
    image_urls.append(finna_image(ids[0]))
  else:
    image_urls = []
    for record_id in random.sample(ids, 3):
      image_urls.append(finna_image(record_id))
    return image_urls
  return image_urls


@register.filter
def is_favorite(record, user):
  return record.is_favorite(user)


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
