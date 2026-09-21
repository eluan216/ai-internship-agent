# Product Requirements Document

**Project:** AI Internship Agent  
**Owner:** eluan216  
**Updated:** 2026-09-21

## Purpose
A small, self-contained Python agent that searches live internship listings, applies filters, and returns a short ranked list the user can act on.

## Core Requirements
- Pull current listings from public sources
- Filter by keywords, location, and how recent the post is
- Use a clear tool-calling style loop (search → rank → save)
- Output a clean markdown shortlist
- Support a demo mode that runs without an API key

## Out of Scope
- Automatic applications
- Scraping login-walled job boards
- Turning this into a general chat assistant

## Technical Choices
- Pure Python where possible
- Simple tools the agent loop calls in order
- Local caching of listings
- Clear separation between data tools and the agent loop
- Optional LLM ranking later; default path is heuristic and offline-capable

## Acceptance Criteria
- Demo mode produces a ranked shortlist with no network and no API key
- Live mode pulls from a public API when available, falls back to demo on failure
- Results stay grounded in the actual listings (no invented jobs)
- One-command setup is straightforward

## Notes on Ownership
All architecture, tool design, prompts, error handling, and documentation in this repository are original work by the owner.
