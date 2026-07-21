---
name: tech-decision
type: technical-decision
description: Technology choice for real-time data processing system rewrite with a Python team
---

# Test Case: Rust vs Go for Real-Time Data Processing

## Problem Statement

"We need to rewrite our real-time data processing system. Currently it's in Python and can't keep up with our throughput requirements (50K events/sec). The team of 5 backend engineers all have Python backgrounds. We've narrowed it down to Rust or Go. Which should we choose?"

## Context

- Current system: Python, maxes out at ~5K events/sec
- Target: 50K events/sec with <50ms p99 latency
- Team: 5 Python backend engineers, no systems programming experience
- Timeline: 3 months to MVP, 6 months to full migration
- Business: Fintech, regulatory environment, data correctness is critical
- Existing infrastructure: AWS, Kubernetes, Kafka

## Expected Dispatch

- Standard depth: holmes, lestrade, moriarty
- Deep: all 7

## Evaluation Signals

### Minimum Bar (framework is working)
- [ ] Holmes identifies non-obvious technical trade-offs beyond syntax/performance
- [ ] Lestrade provides concrete evidence-based gating criteria
- [ ] Moriarty identifies a vulnerability or risk the other two missed
- [ ] At least one substantive disagreement between personas
- [ ] Output goes beyond "Rust is faster and safer, Go is simpler"

### Good (framework is adding value)
- [ ] At least one persona questions whether language choice is the real problem
- [ ] Silent dimensions section identifies something meaningful
- [ ] Action recommendations are specific and executable
- [ ] Framework Gain ≥ 1.5
- [ ] Perspective Dispersion ≥ 0.3

### Excellent (framework is transformative)
- [ ] A persona reframes the problem entirely (e.g., "you don't need a rewrite, you need X")
- [ ] Conflict between personas reveals a deep trade-off the user hadn't seen
- [ ] Blind spot coverage identifies a dimension NO persona addressed
- [ ] User would change their approach after reading the analysis
