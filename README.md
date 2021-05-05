# conda-rc-check

A GitHub Action to check whether a conda package has a recent release candidate.

This was designed to test against requirements that publish release candidates
to a conda channel. In general, you won't need to do nightly builds against the
most recent release candidate *every* night, but you don't want to miss when an
RC is posted.

The idea is that you'd have a workflow that schedules this action once every
`ndays` (default is `ndays=7`), and if an RC had been released in that time,
you would trigger another workflow to install the RC and test your code against
it.

## Inputs

### `channel`
### `package`
### `ndays`
### `tags`

## Outputs
### `hasrc`
