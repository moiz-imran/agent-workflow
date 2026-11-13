# Spec: document-followers (illustrative revision 1)

A user can follow a document. Notify its followers when its text changes. Formatting-only saves do not notify (D2). Moving it keeps its followers and sends no notification (D1). A copy starts with no followers; the original is unchanged.

Acceptance cases: text edit sends one notification per follower; formatting edit and move send none; copy has an empty follower list and leaves the original list intact. This is a fictional scope, not a runnable app.
