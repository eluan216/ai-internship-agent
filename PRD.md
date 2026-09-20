# Product Requirements Document (PRD)

**Project:** AI Internship Agent  
**Owner:** eluan216  
**Status:** In Development  
**Last Updated:** 2026-09-20

## 1. Overview
A lightweight, dependency-free Python AI agent that searches live internship listings, filters them according to user criteria, and produces a prioritized shortlist.

## 2. Goals
- Demonstrate pure agentic AI design (tools + reasoning loop) without heavy frameworks.
- Deliver a practical, immediately useful tool for students and early-career professionals.
- Showcase clean data handling, tool calling, and prompt engineering.

## 3. Key Features
- Live fetching from public internship listing sources.
- Keyword, location, and recency filtering.
- Structured tool calling (search + save shortlist).
- Markdown shortlist output.
- Demo mode that runs without an API key.

## 4. Non-Goals
- Full job application automation.
- Scraping private or authenticated job boards.
- Building a general-purpose chatbot.

## 5. Technical Requirements
- Pure Python (stdlib + minimal external if needed).
- Anthropic Claude (or equivalent) for the reasoning loop.
- Caching of listings to respect rate limits and improve speed.
- Clear separation between tool layer and agent loop.

## 6. Success Metrics
- Correct tool selection and usage by the model.
- Accurate, non-hallucinated results grounded in live data.
- Easy one-file setup and clear documentation.

## 7. Originality Note
This project is independently designed and implemented. All architecture, tool definitions, prompt design, error handling, and documentation are original work by the repository owner.

## 8. License
MIT (or as specified in repository).
