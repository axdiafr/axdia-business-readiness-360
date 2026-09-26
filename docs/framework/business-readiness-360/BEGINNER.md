# BR360 V3 for beginners

**What does it do?** It checks a project from technical, product, security, operational and business angles, then separates what is actually proven from what still needs evidence.

**Does it modify my project?** No. The V3 engine is read-only: it inspects files, creates its own audit result and never commits, pushes or deploys.

**What is automatic now?** The 15 controls explicitly classified `AUTOMATED` have built-in project-local detectors. Other controls still need a test result, runtime observation, human review or real-world evidence depending on the subject.

**Why do I see NOT_TESTED?** Because BR360 refuses to guess. If it cannot prove a control with the right level of evidence, it leaves it unverified.

**Why are some controls N/A?** A CLI, local utility, API, SaaS and mobile app do not need identical controls. N/A controls are excluded from scoring.

**Why can good code still have average business readiness?** Demand, retention, actual customer value, support burden and revenue require evidence outside the repository.

**What are E0 to E4?** E0 is only a claim, E1 static source/config evidence, E2 an executed test/check, E3 runtime evidence and E4 real-world/user/customer evidence.

**What should I do after an audit?** Work through the prioritized actions, add the missing evidence, rerun BR360 and use `compare` to see which findings were resolved or introduced.
