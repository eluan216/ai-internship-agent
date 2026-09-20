# Product Requirements Document

**Project:** AI Internship Agent  
**Owner:** eluan216  
**Updated:** 2026-09-20

## Purpose
A small, self-contained Python agent that searches live internship listings, applies filters, and returns a short ranked list the user can act on.

## Core Requirements
- Pull current listings from public sources
- Filter by keywords, location, and how recent the post is
- Use a clear tool-calling loop (search + save results)
- Output a clean markdown shortlist
- Support a demo mode that runs without an API key

## Out of Scope
- Automatic applications
- Scraping login-walled job boards
- Turning this into a general chat assistant

## Technical Choices
- Pure Python where possible
- Simple tool definitions the model can call
- Local caching of listings
- Clear separation between data tools and the agent loop

## Acceptance Criteria
- The model correctly chooses and uses the tools
- Results stay grounded in the actual listings (no invented jobs)
- One-file setup is straightforward

## Notes on Ownership
All architecture, tool design, prompts, error handling, and documentation in this repository are original work by the owner.
