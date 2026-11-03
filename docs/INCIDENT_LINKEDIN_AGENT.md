# Post-mortem: scheduled LinkedIn content agent (Oct 2026)

**Symptom:** the agent was meant to publish 4 items/day (3 text posts + 1 carousel). Posts stopped for weeks after a migration, and afterwards only 3 of 4 slots published.

**Investigation and findings**
1. The process was not running: its scheduled task had been disabled and pointed at an archived folder after a repo reorganization. Fix: re-register the task against the current repository location.
2. OAuth tokens: the LinkedIn app grants a 60-day access token and does **not** expose `offline_access`, so no refresh token exists. Re-authorization is manual every ~60 days. Documented the renewal flow, and token storage now uses a configurable persistent directory instead of an ephemeral home folder.
3. Latent bug: the main loop called `verificar_prospeccao()`, a method that did not exist in one copy of the code. The loop swallowed the exception every cycle, hiding the defect in logs. Removed the dead call.
4. The carousel slot failed daily with `AttributeError: 'LinkedInTools' object has no attribute 'upload_document'`. Implemented in the current repository the Documents API upload (initializeUpload → PUT → post with media). → [examples/linkedin_document_upload_excerpt.py](../examples/linkedin_document_upload_excerpt.py)
5. Security hygiene found along the way: OAuth client credentials were hardcoded in two scripts. Removed them from the code and moved to environment variables; rotation of the exposed credential is the follow-up.

**What I'd keep as process**
- Alert when expected daily slots are missed (the log existed, nobody was reading it).
- Treat token expiry as a scheduled operational event with an owner and a date.
- Never let a broad `except` hide a missing method: fail loudly in tests.
