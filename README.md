# conda-rc-check

A GitHub Action to check whether a conda package has a recent release candidate.

This was designed to test against requirements that publish release candidates
to a conda channel. In general, you won't need to do nightly builds against the
most recent release candidate *every* night, but you don't want to miss when an
RC is posted.

This workflow checks whether a release candidate has been added within the last
`ndays` days. It sets the value of its output `hasrc`, to either the string
`'True'` if such an RC is present, or the string `'False'` if not.

The assumption is that you'll create a scheduled workflow that calls this
action, and depending on the result, triggers some other workflow. An example
of this is in
[`.github/workflows/example_use.yml`](https://github.com/dwhswenson/conda-rc-check/blob/main/.github/workflows/example_use.yml).

## Inputs

### `channel`

**Required** Channel where the package is found. Default `'conda-forge'`. Note:
if using the "defaults" channel, you must actually specify which specific
channel the package comes from (`'main'`, `'r'`, etc.) Verify that there is a page
at `https://anaconda.org/$CHANNEL/$PACKAGE`.

### `package`

**Required** Package name.

### `ndays`

**Required** Max number of days to search for release candidates. Default `7`.

### `labels`

**Required** Space-separated list of conda labels where RCs are found. Default
`main`.

## Outputs
### `hasrc`

Whether there is a release candidate for this package. The string `'True'` if
there is one; `'False'` if not.

## Example usage

```yaml
- id: checkrc
  uses: dwhswenson/conda-rc-check@v1
  with:
    channel: conda-forge
    package: openmm
    ndays: 7
    labels: 'main openmm_rc'
```
