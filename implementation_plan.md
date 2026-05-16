# Radarr CLI Enhancement Plan

## Goals
- Transition to `argparse` for better CLI management.
- Implement missing core API features (Queue, History, Deletion, Commands).
- Improve output formatting for better readability.
- Enhance existing commands with more options.

## Phase 1: Foundation and Read Operations
- [ ] Replace `sys.argv` with `argparse`.
- [ ] Add `quality-profiles` command.
- [ ] Add `root-folders` command.
- [ ] Add `get` command to show details for a single movie.
- [ ] Implement better table formatting for lists.

## Phase 2: Movie Management
- [ ] Implement `delete` command.
- [ ] Enhance `add` command to support quality profile and root folder selection by name/index.
- [ ] Implement `update` command to change movie settings (monitored, quality profile).

## Phase 3: Activity and History
- [ ] Implement `queue` command (list, delete, grab).
- [ ] Implement `history` command.

## Phase 4: System and Indexers
- [ ] Implement `command` command to trigger Radarr tasks.
- [ ] Implement `indexer` command to list and test indexers.

## Phase 5: Documentation and Skill Update
- [ ] Update `SKILL.md` with new commands.
- [ ] Update `README.md`.
