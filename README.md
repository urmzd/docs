# Project documentation

The account site at [docs.urmzd.com](https://docs.urmzd.com/) helps readers find a project guide. Its GitHub Pages workflow publishes the contents of `public/`, which contains the index, 404, styles and shared brand assets.

| To update | Change the source in | Published address |
| --- | --- | --- |
| Agent SDK guide | [urmzd/saige](https://github.com/urmzd/saige) | [Saige](https://docs.urmzd.com/saige/) |
| Agent orchestration guide | [urmzd/orchagent](https://github.com/urmzd/orchagent) | [Orchagent](https://docs.urmzd.com/orchagent/) |
| Workspace guide | [urmzd/humagen](https://github.com/urmzd/humagen) | [Humagen](https://docs.urmzd.com/humagen/) |

## Change the landing page

Edit `public/index.html`, `public/style.css` or `public/404.html`. Use Python 3 to check the links and preview the account site locally.

```sh
python3 scripts/check_site.py
python3 scripts/serve.py
```

Open [the local preview](http://127.0.0.1:8000/). Check the three guide links and try a missing URL to verify its link back to the index. The local server serves the account site's files. Use the published addresses above to read the project guides.

Open a pull request for the landing page change. The workflow checks the HTML on pull requests and publishes `public/` through the `github-pages` environment on `main`.

## Shared appearance

The index uses the logo, Elza Text and neutral surfaces from [the portfolio’s project directory](https://urmzd.com/projects/). Theme selection starts with the system setting. The header control saves an explicit light or dark choice for the account index and its 404 page.

Books can load `/brand/zensical.css`, `/brand/logo-mark.svg` and `/brand/favicon.svg` from this account site. The stylesheet imports `/brand/fonts.css`, which references the portfolio’s Adobe Fonts kit and two local IBM Plex Mono weights. Publish compatible changes to these paths before deploying a book that uses them. See the [asset credits and licenses](public/brand/CREDITS.txt).

## Preview a guide with the shared brand

Build the guide in its product repository. Keep a checkout of [urmzd.github.io](https://github.com/urmzd/urmzd.github.io) beside that repository. From the product root, mount its generated `site/` and the account’s brand assets under the same paths that Pages serves.

```sh
project=saige  # or orchagent or humagen
preview_dir=$(mktemp -d)
ln -s "$PWD/site" "$preview_dir/$project"
ln -s "$PWD/../urmzd.github.io/public/brand" "$preview_dir/brand"
python3 -m http.server 8000 --bind 127.0.0.1 --directory "$preview_dir"
```

For `project=saige`, open [the local Saige guide](http://127.0.0.1:8000/saige/). Use `/orchagent/` or `/humagen/` for the other guides. Stop with Ctrl+C. The temporary directory contains only links to the guide and shared assets.

## Publish a project guide

Change the Markdown and `zensical.toml` in the product repository. Its own Pages workflow builds the guide and publishes that repository’s `site/` artifact. To roll back a guide, revert its source change there.

## How URLs resolve

GitHub designates `urmzd/urmzd.github.io` as the account site. Set its Pages custom domain to `docs.urmzd.com`. Enable GitHub Actions as the Pages source in each of the three product repositories and leave their custom domains empty. GitHub serves each public project site at the inherited host under its repository name. Each book’s `project.site_url` should match the corresponding published address above. [GitHub’s custom domain inheritance rules](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages#using-a-custom-domain-across-multiple-repositories)
