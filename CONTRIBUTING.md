# Contributing to RepoLens AI

Thanks for contributing.

## Workflow

1. Open or choose an issue that describes the change.
2. Create a focused branch from `main`.
3. Keep commits small and descriptive.
4. Update tests/documentation when behavior changes.
5. Open a pull request and explain what changed, why it changed, and how it was verified.
6. Merge only after the PR is reviewable and checks are green.

## Branch naming

Use short, descriptive prefixes:

- `feat/<topic>`
- `fix/<topic>`
- `docs/<topic>`
- `test/<topic>`
- `chore/<topic>`

## Commit style

Prefer conventional, readable commit messages such as:

- `feat: persist repository analysis`
- `fix: handle GitHub rate limit response`
- `docs: document local setup`
- `test: cover analysis service errors`

## Pull requests

A good PR should be narrow enough to review, link the relevant issue, avoid unrelated refactors, and include verification notes.

## Security

Do not commit API keys, database credentials, tokens, `.env` files, or sensitive repository data.
