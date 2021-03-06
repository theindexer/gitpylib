# gitpylib - a Python library for Git.
# Copyright (c) 2013  Santiago Perez De Rosso.
# Licensed under GNU GPL, version 2.

"""Module for dealing with Git branches."""


import re

import common


SUCCESS = 1
UNFETCHED_OBJECT = 2
INVALID_NAME = 3


def checkout(name):
  """Checkout branch.

  Args:
    name: the name of the branch to checkout.
  """
  common.safe_git_call('checkout %s' % name)


def create(name):
  """Creates a new branch with the given name.

  Args:
    name: the name of the branch to create.
  """
  ok, unused_out, err = common.git_call('branch %s' % name)
  if not ok:
    # TODO(sperezde): check for other errors?
    return INVALID_NAME
  return SUCCESS


def force_delete(name):
  """Force-deletes the branch with the given name.

  Args:
    name: the name of the branch to delete.
  """
  common.safe_git_call('branch -D %s' % name)


def current():
  """Get the name of the current branch."""
  for name, is_current, unused_tracks in status_all():
    if is_current:
      return name


def status(name):
  """Get the status of the branch with the given name.

  Args:
    name: the name of the branch to status.

  Returns:
    a tuple (exists, is_current, tracks) where exists and is_current are
    boolean values and tracks is a string representing the remote branch it
    tracks (in the format 'remote_name/remote_branch') or None if it is a local
    branch.
  """
  out, unused_err = common.safe_git_call('branch --list -vv %s' % name)
  if not out:
    return (False, False, None)

  unused_name, is_current, tracks = _parse_output(out)
  return (True, is_current, tracks)


def status_all():
  """Get the status of all existing branches.

  Yields:
    tuples of the form (name, is_current, tracks) where is_current is a boolean
    value and tracks is a string representing the remote branch it tracks (in
    the format 'remote_name/remote_branch') or None if it is a local branch.
    name could be equal to '(no branch)' if the user is in no branch.
  """
  out, unused_err = common.safe_git_call('branch --list -vv')
  for b in out.splitlines():
    yield _parse_output(b)


def set_upstream(branch, upstream_branch):
  """Sets the upstream branch to branch.

  Args:
    branch: the branch to set an upstream branch.
    upstream_branch: the upstream branch.
  """
  ok, out, err = common.git_call(
      'branch --set-upstream %s %s' % (branch, upstream_branch))

  if not ok:
    if 'Not a valid object name' in err:
      return UNFETCHED_OBJECT

  return SUCCESS


def _parse_output(out):
  """Parses branch list output.

  Args:
    out: the output for one branch.

  Returns:
    a tuple (name, is_current, tracks) where is_current is a boolean value and
    tracks is a string representing the remote branch it tracks (in
    the format 'remote_name/remote_branch') or None if it is a local branch.
  """
  # * indicates whether it's the current branch or not, next comes the name of
  # the branch followed by the sha1, optionally followed by some remote tracking
  # info (between brackets) and finally the message of the last commit.
  if out.startswith('* (no branch)'):
    return ('(no branch)', True, None)

  pattern = '([\*| ]) ([^\s]+)[ ]+\w+ (.+)'
  result = re.match(pattern, out)
  if not result:
    raise Exception('Unexpected output %s' % out)

  tracks = None
  if result.group(3)[0] == '[':
    track_info = result.group(3).split(']')[0][1:]
    tracks = ''
    if ':' in track_info:
      tracks = track_info.split(':')[0]
    else:
      tracks = track_info

  return (result.group(2).strip(), result.group(1) == '*', tracks)
