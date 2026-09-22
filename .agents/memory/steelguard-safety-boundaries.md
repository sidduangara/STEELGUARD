---
name: SteelGuard safety simulation boundary
description: Durable guardrails for emergency controls, notifications, and industrial safety claims in the SteelGuard prototype.
---

Emergency shutdown and authority escalation are tabletop simulation workflows only. The product must label them as simulated, require explicit operator confirmation, record an audit identifier, and never claim to control machinery, contact responders, or replace qualified safety procedures.

**Why:** This prototype uses synthetic data and has no physical sensor, camera, plant-control, SMS, email, or dispatch integration.

**How to apply:** Preserve the simulation disclaimer and two-step confirmation whenever extending emergency controls; keep real outbound integrations disconnected unless the user explicitly requests and authorizes one.