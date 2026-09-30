# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->

This target of 4 of 5 because questions with less related documents may struggle retrieving the correct chunk or chunks with the answer. This will most likely happen with the library question as it lacks many documents covering full scope of libraries experience. 

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->

All five is the achievable target as it proves that the model is not just providing an answer, but follows the work flow proving it does every step including providing the name of the source documnets. 

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:**
I chose 4 of 5 because the cutoff is a tradeoff. If I set it tight enough to reject every off-topic question, it starts refusing legitimate questions that happen to be phrased unusually. I'd rather the gate occasionally let through a borderline question than refuse things my documents do cover. Any miss should be a question that sits close to my documents' topic, not a random one.

---

## 4. Something about your chunks
Chunks should not be shorter than 80 characters.

**Why this target:**
85 is the threshold I chose as it is on average a bit under 30% or less of the document. The average character per document in campus_life is 317, we want to avoid having whole document chunks. This chunk size is not too strict as some documents are smaller and others are bigger. 


---

## 5. Your choice
For all 5 test questions, every factual claim in the answer can be traced to a specific setence in one of the retrieved chunks.

**Why this target:**
I picked all 5 because we want to make sure the answers provided are grounded, and any failure to do so would prove ignored context or using own knowledge for answers. 


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
