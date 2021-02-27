# pr-report
Prints your Github PRs.

## Usage
Either export a Github Personal Access Token to your shell as `GITHUB_TOKEN`, or pass it using the `-t` parameter.


```
$ pr-report --help
Usage: pr-report [OPTIONS]

Options:
  -a, --author TEXT
  -t, --token TEXT
  -s, --since [%Y-%m-%d]       [default: 2021-02-19]
  -d, --disable-cache BOOLEAN
  -v, --verbose
  --help                       Show this message and exit.

$ pr-report
100%|█████████████████████████████████████████████| 6/6 [00:07<00:00,  1.20s/it]

In Progress
  No open pull requests.

Closed 2021-02-24
  some-org/some-repo
    #123 Another pull request message
    #122 Pull request message
  andrewsosa/pr-report
    #1 Dummy PR
    #0 The first PR
```

_(I would have included my actual results, but they're from private repos...)_
