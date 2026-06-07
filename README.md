# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

This project focuses on NBA team season analysis and performance reviews. Fans often want to understand why teams succeed or fail, which teams have the strongest defenses, which teams depend on star players, and how teams compare heading into the playoffs. Official standings and statistics do not always provide this context. By collecting detailed team reports and enabling semantic search across them, this system provides an unofficial guide to NBA team performance.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:600 characters**

**Overlap:100 characters**

**Why these choices fit your documents:The team reports contain multiple sections such as season overview, strengths, weaknesses, key players, coaching analysis, and playoff outlook. A chunk size of 600 characters preserves enough context for meaningful retrieval while remaining focused on a single topic. A 100-character overlap helps prevent important information from being split across chunk boundaries.**

**Final chunk count:41 chunks**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:all-MiniLM-L6-v2 (Sentence Transformers)**

**Production tradeoff reflection:I selected all-MiniLM-L6-v2 because it is lightweight, fast, and performs well for semantic similarity tasks. In a production environment, I would evaluate larger embedding models that provide improved semantic understanding and support for longer contexts. I would also consider latency, cost, multilingual support, and retrieval accuracy when choosing an embedding model.**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:The system instructs the language model to answer questions using only the retrieved context.

Example instruction:

“Answer the question using ONLY the provided context. If the answer is not contained in the context, say: ‘I could not find enough information in the retrieved documents.’”

This prevents the model from relying on outside knowledge and encourages grounded responses.**

**How source attribution is surfaced in the response:After retrieval, the system displays the source file names associated with the retrieved chunks. These sources are shown alongside the generated answer so users can identify where the information originated.**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What made the Oklahoma City Thunder successful? | Defense, depth, MVP-level play | Correctly identified defense, depth, and Shai Gilgeous-Alexander’s impact |Relevant |Accurate |
| 2 | What are the Lakers’ biggest weaknesses? | Health and consistency | Correctly identified health concerns and roster depth issues|Relevant | Accurate|
| 3 | Which team has the strongest defense? | Thunder, Celtics, or Spurs | Returned Thunder as a leading defensive team| Relevant| Accurate|
| 4 | Which team depends most on star players? | Lakers, Suns, or Nuggets | Highlighted reliance on elite star players| Partially Relevant| Partially Accurate|
| 5 | Which team has the best playoff outlook? | Thunder, Celtics, Nuggets, or Lakers | Correctly identified championship contenders| Relevant| Accurate|

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:Which team depends most on star players?**

**What the system returned:The answer discussed several teams but did not clearly identify a single team.**

**Root cause (tied to a specific pipeline stage):The retrieval stage returned chunks from multiple teams because several reports discussed star-player dependence. The embedding model considered these chunks similarly relevant, resulting in ambiguous context for generation.**

**What you would change to fix it:I would experiment with reranking retrieved chunks or increasing document specificity so the model can better distinguish between teams that rely heavily on individual stars.**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:The planning document helped define the chunking strategy, retrieval approach, and evaluation questions before implementation. Having these decisions documented made it easier to verify whether the system was behaving as intended.**

**One way your implementation diverged from the spec, and why:The original plan anticipated using ten reports with approximately equal lengths. During implementation, some reports contained more detailed analysis than others, which resulted in varying chunk counts across documents. The retrieval system still performed effectively despite this difference.**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:    My chunking requirements and project architecture.*
- *What it produced:    Python code for document ingestion and chunking.*
- *What I changed or overrode:    I verified the chunk sizes manually and adjusted the implementation to use a 600-character chunk size with 100-character overlap.*

**Instance 2**

- *What I gave the AI:    The retrieval requirements, embedding model choice, and ChromaDB storage design.*
- *What it produced:    Code for embedding generation, vector storage, retrieval, and Groq-based answer generation.*
- *What I changed or overrode:    I tested retrieval quality with evaluation questions and modified the number of retrieved chunks to improve answer relevance.*
