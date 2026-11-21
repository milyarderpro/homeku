# Video similarity candidates

62 videos; 900 samples; 1891 video pairs; 0 candidate pairs.

[Full data and matching frames](candidates.json) · [Corpus patterns](../corpus-patterns.md)

Method: content-cropped 64-bit difference hashes, Hamming distance ≤6, at least two unique paired samples, minimum grayscale contrast 12. It can flag a re-encode or shared scene when sampled appearances survive, but it is not exhaustive and has no calibrated precision/recall.

Every result is a review candidate. Both sources remain. Matching styles or layouts alone do not prove a duplicate.

## Limits

- Candidate screen only, not a calibrated duplicate classifier.
- Similar compositions may yield false positives; crops, heavy edits and unsampled content may be missed.
- Three uniform samples on unannotated videos have lower coverage than annotated videos.
- No automatic deletion, merging, count adjustment or claim of independent houses.
