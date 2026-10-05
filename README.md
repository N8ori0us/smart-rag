# Smart RAG Search & Produce

An adaptive, collaborative Retrieval-Augmented Generation (RAG) assistant designed to serve as an engineering sounding board, teacher, and brainstorming collaborator. 

## Project Architecture

This application decouples the compute backend from the client interface to maximize resource efficiency across network layers.


## Core Behavioral Protocols

To bridge the gap between open-ended conceptual brainstorming and strict code execution, the system maintains two explicit operational states:

1. **Brainstorm Mode (The Collaborator):** An open-ended, conversational environment focused on lateral thinking, cross-disciplinary analogies, and mapping nebulous ideas into concrete concepts. The system acts as a patient teacher, passively logging the trajectory of questioning for future revisitation.
2. **Implementation Mode (The Builder):** A highly dense, zero-fluff text environment featuring hardcoded anti-sycophancy instructions. The system transitions into a rigid code and logic auditor, directly challenging malformed premises and enforcing strict technical precision.

### Automated Loop Interceptor
To mitigate unproductive, circular lines of theoretical questioning, a background window counter tracks consecutive turns. If the conversation stays in an open-ended loop for more than 5 turns without reaching an actionable design phase, the system caches the conceptual summary and fires a workspace notification challenge to allow the user to pivot or lock in.