You are reviewing a change in this repository. The change under review is `git diff base HEAD`; `base` is a tag.
The spec, if there is one, is in SPEC.md. Review only; don't edit anything.

Return your result as JSON matching the output schema: one entry per finding, with the repo-relative path,
the line range in the HEAD version of the file, the severity (Blocking, Should-fix or Optional, as the rubric
defines them), a one-line title and the evidence. List every changed file you read in `covered`, and any you
couldn't in `not_covered`. No findings is a valid answer.
