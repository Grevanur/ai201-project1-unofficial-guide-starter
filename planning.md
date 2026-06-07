# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

This project focuses on NBA team season analysis and performance reviews. Fans and analysts often rely on season reports, expert commentary, and team evaluations to understand why teams succeed or struggle. This information is scattered across multiple sources and perspectives, making it difficult to compare teams and identify common themes. The system acts as an unofficial NBA team analysis guide that allows users to ask questions about team strengths, weaknesses, key players, coaching impact, and playoff outlook.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |Oklahoma City Thunder Report| Team season analysis|data/okc.txt|
| 2 |Boston Celtics Report|Team season analysis|data/celtics.txt|
| 3 |New York Knicks Report|Team season analysis|data/knicks.txt|
| 4 |Los Angeles Lakers Report|Team season analysis|data/lakers.txt|
| 5 |Denver Nuggets Report|Team season analysis|data/nuggets.txt|
| 6 |Minnesota Timberwolves Report|Team season analysis|data/timberwolves.txt|
| 7 |San Antonio Spurs Report|Team season analysis|data/spurs.txt|
| 8 |Phoenix Suns Report|Team season analysis|data/suns.txt|
| 9 |Cleveland Cavaliers Report|Team season analysis|data/cavs.txt|
| 10|Atlanta Hawks Report|Team season analysis|data/hawks.txt|

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:600 characters**

**Overlap:100 characters**

**Reasoning: NBA season reports contain multiple topics including team strengths, weaknesses, key players, coaching analysis, and playoff outlook. A chunk size of 600 characters preserves meaningful context while remaining focused enough for accurate retrieval. A 100-character overlap helps prevent important information from being split across chunk boundaries.**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:all-MiniLM-L6-v2 (Sentence Transformers)**

**Top-k:3**

**Production tradeoff reflection: If this system were deployed in production, I would evaluate larger embedding models that offer stronger semantic understanding and support for longer context windows. I would also consider multilingual support, retrieval accuracy, latency, and inference costs. The chosen model provides a good balance between speed, quality, and resource usage for this project.**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 |What made the Oklahoma City Thunder successful?|Elite defense, depth, and MVP-level play from Shai Gilgeous-Alexander.|
| 2 |What are the Lakers’ biggest weaknesses?|Health concerns, consistency, and roster depth.|
| 3 |Which team has the strongest defense?|Oklahoma City Thunder, Boston Celtics, or San Antonio Spurs based on retrieved reports.|
| 4 |Which team depends most on star players?|Lakers, Suns, or Nuggets depending on retrieved context.|
| 5 |Which team has the best playoff outlook?|Thunder, Celtics, Nuggets, or Lakers depending on context.|

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.    Different reports may contain subjective opinions or conflicting evaluations of teams and players.

2.    Similar basketball terminology across multiple reports may lead to retrieval of related but less relevant chunks.

---

## Architecture

+----------------------+
|  Team Report Files   |
|   (10 TXT Files)     |
+----------+-----------+
           |
           v
+----------------------+
| Document Ingestion   |
|     ingest.py        |
+----------+-----------+
           |
           v
+----------------------+
|      Chunking        |
| 600 chars, overlap   |
|       = 100          |
+----------+-----------+
           |
           v
+----------------------+
|  Embedding Model     |
| all-MiniLM-L6-v2     |
+----------+-----------+
           |
           v
+----------------------+
| ChromaDB Vector DB   |
|      embed.py        |
+----------+-----------+
           |
           v
+----------------------+
| Semantic Retrieval   |
|      Top-K = 3       |
|      query.py        |
+----------+-----------+
           |
           v
+----------------------+
|   Groq Llama 3.3     |
|      ask.py          |
+----------+-----------+
           |
           v
+----------------------+
| Final Answer +       |
| Source Attribution   |
+----------------------+

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:I used claude to generate document loading and chunking code based on my chunk size and overlap requirements. I verified the implementation by inspecting the generated chunks and ensuring they preserved meaningful basketball analysis content.**

**Milestone 4 — Embedding and retrieval:I used Claude to generate embedding and retrieval code using Sentence Transformers and ChromaDB. I verified correctness by testing retrieval with basketball-related questions and checking that relevant team reports were returned.**

**Milestone 5 — Generation and interface:I used claude to generate retrieval-augmented generation code using Groq’s Llama 3.3 model. I verified correctness by asking evaluation questions and confirming that generated answers were grounded in retrieved context and included source attribution.**
