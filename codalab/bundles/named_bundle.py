'''
NameBundle is an abstract Bundle supertype that all other bundle types subclass.
It requires name, description, and tags metadata for all of its subclasses.
'''
import re
import time

from codalab.common import UsageError
from codalab.objects.bundle import Bundle
from codalab.objects.metadata_spec import MetadataSpec


class NamedBundle(Bundle):
  NAME_REGEX = re.compile('^[a-zA-Z_][a-zA-Z0-9_\.\-]*\Z')
  METADATA_SPECS = (
    MetadataSpec('name', basestring, 'name: %s' % (NAME_REGEX.pattern,)),
    MetadataSpec('description', basestring, 'human-readable description'),
    MetadataSpec('tags', set, 'list of searchable tags', metavar='TAG'),
    MetadataSpec('created', int, '', generated=True),
    MetadataSpec('data_size', int, '', generated=True),
    MetadataSpec('failure_message', basestring, '', generated=True),
  )

  @classmethod
  def construct(cls, row):
    # The base NamedBundle construct method takes a bundle row and adds in
    # automatically generated metadata values.
    row['metadata'] = dict(row['metadata'], created=int(time.time()))
    return cls(row)

  def validate(self):
    super(NamedBundle, self).validate()
    bundle_type = self.bundle_type.title()
    if not self.metadata.name:
      raise UsageError('%ss must have non-empty names' % (bundle_type,))
    if not self.NAME_REGEX.match(self.metadata.name):
      raise UsageError(
        '%s names must match %s, was %s' %
        (bundle_type, self.NAME_REGEX.pattern, self.metadata.name)
      )
    if not self.metadata.description:
      raise UsageError('%ss must have non-empty descriptions' % (bundle_type,))

  def __repr__(self):
    return '%s(uuid=%r, name=%r)' % (
      self.__class__.__name__,
      str(self.uuid),
      str(self.metadata.name),
    )
