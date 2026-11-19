# Project documentation

The index at [docs.urmzd.com](https://docs.urmzd.com/) connects three books. Each product repository owns its Markdown and root `zensical.toml`. This repository owns the pins, index and Pages workflow.

| Book | Source | Published path |
| --- | --- | --- |
| Saige | [urmzd/saige](https://github.com/urmzd/saige) | `/saige/` |
| Orchagent | [urmzd/orchagent](https://github.com/urmzd/orchagent) | `/orchagent/` |
| Humagen | [urmzd/humagen](https://github.com/urmzd/humagen) | `/humagen/` |

## Preview a release

From this checkout, with Git and Python 3.11 or later installed, run the following commands. The build fetches each pinned commit into a temporary checkout and runs Zensical 0.1.2 there. Only the three rendered books and the files in `public/` enter `site/`.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/build.py
python scripts/serve.py
```

Open [the local index](http://127.0.0.1:8000/). Follow a project link, then open a chapter and try its search box. A missing URL such as `/saige/missing/chapter/` should return HTTP 404 and a link back to the index. Stop the preview with Ctrl+C.

To build from local clones that already contain all three commits, pass their parent directory using `python scripts/build.py --local ../`. The build still checks out the exact revisions. To repeat just the assembled-site checks, run `python scripts/check_site.py site`.

## Publish a product documentation change

1. Merge and verify the documentation change in the product repository. Copy its full commit SHA. Each book must build from its root with `zensical build --clean --strict` and set `project.site_url` to its published directory.
2. Replace that product’s `revision` in [sources.json](sources.json) and open a pull request here. The build checks all three books, their canonical URLs, local links, referenced assets and search documents.
3. Merge the passing pin change to `main`. GitHub Actions uploads the whole site as one artifact and deploys it through the `github-pages` environment. To roll back, revert the pin change and let the same workflow publish the previous contents.

The Pages source for this repository is GitHub Actions. The custom domain is `docs.urmzd.com`. [Pages workflow settings](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
