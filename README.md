# Canonical Take-Home Task

## Quick setup
To run coverage for tests:
```
 pip install coverage
``` 
Tests
```python
 python -m unittest test_utils.py
 or
 coverage run -m unittest test_utils.py
```
Coverage report
```
coverage report -m
```

## Task
Build CLI tool that accepts architecture as argument and prints top 10 packages that have the most files associated with them.

## Deliverable(s)
CLI tool for showing statistics of top 10 packages for given architecture.

Example usage: 
```python
python package_statistics.py amd64
python package_statistics.py -h  # help on usage
```

## Assumptions, prerequsites.
Inline comments are note-like, informal, not present everywhere, this guide can help understand the whole process.

## Plan of attack
- Study the given task thoroughly.
- Make notes of assumptions.
- Study the Debian mirror's Contents indices.
- Study the "Contents" indices information to get a raw picture of what data to expect.
- Make notes of limitations, potential issues (filesize, a quick `wc` gave around 6mln rows for `amd64` contents file).
- Get feet wet by actually downloading any Contents-xxx.gz file, unpacking it and seeing what's inside.
- Sketch out raw algorithm and design services for each step.

## Raw algorithm
- Take architecture input in CLI
- Establish FTP connection
- Download .gz file
- Unpack it
- Parse file by keeping track of packages
- Use Counter to find top N packages
- Pretty-print the results in terminal

## Approximate breakdown of time taken
| Task | Time Taken |
|------|------------|
| Research | 30-40 minutes |
| Design   | 50-60 minutes |
| Implementation + Testing | ~ 1 hour |
| Refactoring | ~ 1 hour|
| Wrap up | ~ 30 minutes |

## Quick improvements
- Added a --top argument to specify any number of top packages to show.
- Added a --country argument to specify closest mirror location.
- Added --dist and --comp arguments.
- Added a vizual flair by utilizing colors, to make things not so boring and more readable.

## Future plans
- Add check for nearest mirror. Downloading gzip files from UK mirror while in Poland is taking a while.
- Maybe add checking the cache signature of remote Contents-xxx.gz file to avoid downloading everytime.
- Would be good to add functional test to get top 3 for each architecture present.
  
## Personal thoughts

I tried not to overcomplicate things and would usually ask some clarifying questions, but I went with basic assumptions (I would rarely do this in real life since ambigious requirements would create unnecessary work). I also went with using Python built-ins to keep it simple and avoid any extra actions.

I have included very basic set of tests to ensure that all moving parts are working as expected. Of course, more tests should be included. Presence of tests will also assist with adding new functionality, you would not start adding it if tests fail, and you would cover your functionality with tests to help with next iteration of feature development.

I have done around two cycles of refactoring while implementing the design, some things are clearer when you actually arrive at them.
Ideally this small CLI tool could take a microservice-like arrangement, but it's easier to start with all services in one place and later to separate them rather than separating in the beginning and if it's too bloated, trying to put things back together.
