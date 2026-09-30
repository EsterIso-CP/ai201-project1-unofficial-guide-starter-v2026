# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This project answers student questions about campus life using a small corpus of short posts on courses, dining halls, housing, and administrative deadlines. You can ask things like how many hours a course takes outside of class, when a dining hall is open, or what laundry costs in a residence hall. If a question isn't covered by the posts, it says so instead of guessing.

## Chunking Strategy

**Chunk size:**
85
**Overlap:**
10

I chose these numbers as 85 a bit under 30% of the documents average character size which helps with chunking proper ideas and not multiple ideas. 10 overlap because we do not need more than 20 extra characters to reach the answers needed as original chunking size should keep answers and only need the overlap for cut off details. 

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week.
```

**Chunk 2** — source: `course_cs_210_exams.txt#4` — produced by: `chunker.py::split_documents`

```
CS 210 Data Structures — assessment

0% — the exams reuse the lab problems.
```

**Chunk 3** — source: `course_phys_130_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for PHYS 130 Mechanics

People keep asking so: 7 hours a week, plus 3 on lab
```

**Chunk 4** — source: `dining_verrill_street_grill_followup.txt#7` — produced by: `chunker.py::split_documents`

```
Re: Verrill Street Grill

Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_morrow_house_laundry.txt#1` — produced by: `chunker.py::split_documents`

```
Laundry in Morrow House

There are eight washers and six dryers for the building, whi
```

## Sample Answer

**Question:** `How many hours should I expect to spend outside of CS Data Structures course?`

**Answer:** `You should expect to spend 8 to 10 hours a week outside of class.`

```
Source: course_cs_210.txt (and course_cs_210_workload.txt)

Sources retrieved: course_cs_210.txt, course_cs_210_workload.txt
```

**My relevance cutoff:** 0.5

I ran five questions the corpus covers and the five in `OUT_OF_SCOPE`, and recorded the best (lowest) chunk distance for each. The in-scope group ran from 0.095 (laundry cost at Fenwick Court) to 0.342 (maximum hours students can work), and the out-of-scope group ran from 0.783 (capital of Mongolia) to 0.841 (diesel oil change). The gap runs from 0.342 to 0.783. I put the cutoff at 0.5, which leaves about 0.16 of margin above my weakest in-scope question so a rephrased question isn't wrongly refused, while staying far below the closest off-topic question.

| Question | In corpus? | Best distance |
|---|---|---|
| How many hours should I expect to spend outside of CS Data Structures course? | Yes | 0.195 |
| Which are the hours that Pellew Dining Hall? | Yes | 0.169 |
| How much does laundry wash and dry cost at Fenwick Court? | Yes | 0.095 |
| What are the maximum hours students can work? | Yes | 0.342 |
| What time is the library open to? | Yes | 0.250 |
| What is the capital of Mongolia? | No | 0.783 |
| How do I change the oil in a diesel engine? | No | 0.841 |
| Who won the 1994 World Cup? | No | 0.810 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.801 |
| How do I write a for loop in Rust? | No | 0.831 |

## How I Used AI
**1.** I asked Claude to write the chunking function for my corpus. The first version ignored both `CHUNK_SIZE` and `CHUNK_OVERLAP`, so chunks had no size cap and carried no text over from the previous chunk. It also split in the wrong places, cutting through thoughts instead of at natural boundaries. I went back and described what I expected: a post that fits in `CHUNK_SIZE` stays whole as one chunk, and a longer post has its title (the first line) prepended to every chunk. The body splits on paragraphs, then sentences, then a hard cut as a last resort. `CHUNK_SIZE` is a hard ceiling on the whole chunk, title included, and the overlap is built from whole units and capped at a quarter of the body budget so chunks can always advance. I also explained how it connects to the rest of the code: it returns `Chunk` objects tagged `produced_by="chunker.py::split_documents"`, which `app.py chunks` prints. With that spec, the function respected both settings and split cleanly.

**2.** The version Claude gave me also dropped the title from a post's chunks whenever the title left less than 20 characters of room for body text (the `MIN_BODY_ROOM` fallback). I wanted the title on every chunk of a split post, so I asked Claude to remove that fallback. It did, and it warned that a title close to or longer than `CHUNK_SIZE` would make the body budget zero or negative, which would break the slicing and the "no chunk longer than CHUNK_SIZE" guarantee. I kept the change because the titles in my corpus are short, so the fallback was never needed.


---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
