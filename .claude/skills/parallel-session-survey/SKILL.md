---
name: parallel-session-survey
description: >
  Survey other sessions' in-flight work on this shared repo BEFORE you build something new and
  BEFORE you land a long-lived branch, so you don't independently reimplement a style card, an
  analyzer rule, or an `aide` toolkit feature that already exists on another branch. Use it at the
  START of substantial work (a new style card, an analyzer threshold change, a new `aide`
  subcommand or module, a big gallery series) and again just BEFORE merging. It ranks branches by
  most recent activity and tells you how to adopt-vs-rebuild when two branches grow the same thing.
  The cheap catch is at start, not at merge.
---

# Parallel-session survey (Pixel-Art-Aide)

## Why this exists

This studio runs in parallel sessions on different branches of the same repo (sessions here even
share one branch name across both this repo and `thaumaturgy-the-new-age`). Two sessions can
independently change the SAME thing — a style card's palette, an analyzer threshold, an `aide`
module — with no textual merge conflict. A clean `git merge` hides it; you only find out after.

**The expensive collision is the SILENT one** — two versions of one artifact, no merge marker. A
textual conflict is cheap; git shows it to you. This survey targets the semantic collision git
can't see. (Sister skill: the same-named skill in the `thaumaturgy-the-new-age` repo, where this
pattern was first hit — a wand-vis system built twice in parallel.)

## What collides in THIS repo

- **`styles/*.md`** — two sessions re-tuning the same palette / busyness band / checklist.
- **`aide/analyze.py` thresholds** — a house rule changed on two branches to different values
  (remember: analyzer thresholds and the doc that describes them must change together — hard rule 6).
- **`aide/` toolkit modules** — a new subcommand or a rewrite of rendering/parsing landing twice.
- **`knowledge/lessons.md` / `shading.md`** — parallel appends (append-only usually merges
  cleanly, but two sessions folding the same lesson into `shading.md` collide).
- **`gallery/` series** — two sessions iterating the same subject under different session dirs.

## When to run it

1. **Pre-flight** — before authoring a new style card, changing an analyzer rule, adding/rewriting
   an `aide` module, or starting a big gallery series. Adopt what already exists before writing.
2. **Pre-land** — before merging your branch, even if `git merge` reports no conflict.

## Pre-flight survey

Run `get_me` first, then (GitHub MCP tools, `owner=minerguy341 repo=Pixel-Art-Aide`):

1. **Open PRs, most-recently-updated first** — strongest "who is working NOW" signal:
   `list_pull_requests(state="open", sort="updated", direction="desc")`; skim any that touch your
   area with `pull_request_read`.
2. **Recently-merged work on the default branch** — already-merged work is your base, not a
   collision: `list_commits(sha="main", perPage=20)` and read the messages.
3. **Rank ALL branches by recency (the key step).** `list_branches` returns only names + head SHAs
   — NO dates — so it can't rank on its own. To find the most-recently-worked branches:
   - `list_branches(perPage=100)` to enumerate.
   - For each live candidate, probe its head-commit date: `list_commits(sha="<branch>", perPage=1)`
     → read `commit.author.date` (or `commit.committer.date`). That date IS "last worked on."
   - Sort descending; read the top few branches' diffs in your area FIRST — that's where live
     parallel work is and the likeliest to collide.
   - Shortcut when you know the target: `search_commits(query="repo:minerguy341/Pixel-Art-Aide
     analyze.py", sort="committer-date")` (swap in the file/system name) finds recently-touched
     branches without probing every one.
4. **Decide before writing.** If a branch or `main` already has the style card / rule / module you
   were about to make, adopt THAT as your base. Building a parallel version is the throwaway path.

## Pre-land diff

Even when `git merge` reports no conflict:

1. `git fetch origin main`, then `git diff origin/main...HEAD -- <paths>` over the files you
   touched, and re-run the recency ranking — branches may have landed since pre-flight.
2. If a competing version of an artifact you touched already sits on `main`, **adopt main's as the
   base and redo your change onto it.** `main` is shared ground; your branch is not.
3. Special case for `lessons.md`: it's append-only and user-gated. Parallel appends usually
   auto-merge, but confirm both sessions' approved entries survived the merge and nothing got
   dropped or duplicated.

## Collision triage

| Signal | Cost | Action |
|---|---|---|
| Textual merge conflict | cheap | git shows it — resolve normally |
| Two versions of one artifact, **no** conflict marker | expensive | adopt main's/the-landed version, redo yours onto it |
| Your change already merged to main | — | not a collision; rebase onto it, don't re-add |

## Limitation — this only sees pushed work

The survey ranks **landed and pushed** branches/PRs. A parallel session mid-flight but not yet
pushed is invisible to every tool here. This reduces collision risk; it doesn't eliminate it. Before
changing something central (a shared style card, an analyzer threshold), it's worth asking the user
whether another session is already on it — the tools can't tell you.
