# Taiji API Community Governance Model

> **Core Philosophy**: Community co-ownership, co-decision, co-maintenance, co-benefit
>
> **Founder Retention Clause**: Project founder retains supreme management authority and final decision-making power

---

## 👑 Founder Rights

### Founder Definition

**Founder**: [@ad7007](https://github.com/ad7007) - Muming Yu

Project initiator and initial developer, holding special status and authority.

### Founder Rights

#### Supreme Management Rights
- ✅ **Project Direction Decision** - Decide overall project development direction
- ✅ **Final Veto Power** - Can veto any community decision
- ✅ **Emergency Disposition Power** - Quick decision-making in emergencies
- ✅ **Maintainer Appointment/Removal** - Directly appoint or remove maintainers
- ✅ **License Change Rights** - Decide project license
- ✅ **Brand Usage Rights** - Project name and trademark usage

#### Special Rights Implementation
- ✅ GitHub Repository Owner permissions (non-transferable)
- ✅ PyPI package publishing permissions
- ✅ Domain and website control
- ✅ Official social media control

### Founder Rights Constraints

To protect community interests, founder rights are subject to the following constraints:

- ⚠️ **Major Decision Publicity** - Major decisions like license changes require 30-day advance publicity
- ⚠️ **Community Supervision** - Founder decisions accept community supervision
- ⚠️ **Transparency Requirements** - Financial-related decisions must be public
- ⚠️ **Succession Plan** - If founder cannot continue, must designate successor

### Founder vs Community

| Decision Type | Decision Method | Founder Rights |
|--------------|-----------------|----------------|
| Daily PR Merge | Maintainer decision | Non-intervention |
| Feature Addition | Community vote (2/3) | Can veto |
| Architecture Change | Community vote (2/3) | Can veto |
| License Change | Founder decision + publicity | Final decision |
| Maintainer Appointment | Community vote + founder confirmation | Final appointment |
| Project Direction | Community discussion + founder decision | Final decision |

---

## 🌟 Governance Principles

### 1. Decentralization + Founder Supervision

- ✅ **Community Co-ownership** - Belongs to all contributors
- ✅ **Open Decision-making** - Major decisions by community vote
- ⚠️ **Founder Retains Final Decision** - Protect project direction

### 2. Transparency

- ✅ All discussions public on GitHub
- ✅ All decisions recorded
- ✅ All code reviewable
- ✅ Founder decisions require justification

### 3. Meritocracy

- ✅ Contribution determines influence
- ✅ Ability determines responsibility
- ✅ Fair treatment of every contributor
- ⚠️ Founder has right to exceptional promotion

### 4. Sustainable Development

- ✅ Avoid overburdening individuals
- ✅ Cultivate new maintainers
- ✅ Long-term planning
- ✅ Founder succession plan

---

## 👥 Roles and Responsibilities

### 👑 Founder

**Definition**: Project initiator and initial developer

**Current**: [@ad7007](https://github.com/ad7007) - Muming Yu

**Rights**:
- ✅ Supreme management authority
- ✅ Final decision-making power
- ✅ Maintainer appointment/removal power
- ✅ License change power
- ✅ Project direction decision power
- ✅ Emergency disposition power
- ✅ Brand usage rights

**Responsibilities**:
- ✅ Guide project direction
- ✅ Protect community interests
- ✅ Cultivate maintainer team
- ✅ Develop succession plan

**Term**: Permanent (unless voluntarily relinquished or successor designated)

---

### Core Maintainer

**Definition**: Senior maintainers responsible for daily project operations

**Rights**:
- ✅ All maintainer rights
- ✅ Daily decision-making power (when uncontested)
- ✅ Represent project in external communications

**Responsibilities**:
- ✅ Commit at least 5 hours per week
- ✅ Coordinate maintainer work
- ✅ Develop project planning
- ✅ Handle community disputes
- ⚠️ Major decisions require founder approval

**Becoming**:
- Maintainer vote (3/4 approval)
- **Founder final confirmation**
- Community publicity for 7 days without objection

**Removal**:
- Maintainer vote (3/4 approval)
- **Founder has right to directly remove**

---

## 🗳️ Decision-Making Mechanism

### Daily Decisions

**Scope**: 
- Bug fixes
- Documentation updates
- Small feature improvements

**Process**:
```
Submit PR → Maintainer Review → Merge
```

**Approval**: 1 maintainer agreement

**Founder Rights**: Non-intervention (unless issues discovered)

---

### Medium Decisions

**Scope**:
- New features
- API changes
- Performance optimization

**Process**:
```
Submit Issue discussion → Submit PR → 2 Maintainers Review → Merge
```

**Approval**: 2 maintainers agreement

**Founder Rights**: Can veto (requires justification)

---

### Major Decisions

**Scope**:
- Architecture changes
- License modifications
- Governance model changes
- Core maintainer appointment

**Process**:
```
Submit RFC → Community discussion 7 days → Vote 7 days → Founder confirmation → Execute
```

**Approval**: 
- Voter turnout > 50%
- Approval votes > 2/3
- **Founder final confirmation**

**Founder Rights**:
- ✅ Can veto (requires written justification)
- ✅ Can request re-vote
- ✅ Can propose alternative solutions

---

## 📊 Voting Rules

### Voting Eligibility

- ✅ Active contributors (5+ PRs)
- ✅ Maintainers
- ✅ Core maintainers

**Weight**: One person, one vote (equal)

### Voting Process

1. **Proposal**: Submit RFC in Issue
2. **Discussion**: 7 days public discussion
3. **Voting**: 7 days voting period
4. **Result**: Announce and execute

### Voting Types

| Type | Approval Condition | Scope |
|------|-------------------|-------|
| Simple Majority | > 50% approval | Daily decisions |
| Absolute Majority | > 2/3 approval | Major decisions |
| Unanimous | 100% approval | License changes |

---

## 🔄 Version Release Process

### Version Numbering Rules

Follow semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Incompatible API changes
- **MINOR**: Backward-compatible feature additions
- **PATCH**: Backward-compatible bug fixes

### Release Process

```
1. Create Release Branch
   ↓
2. Update version number
   ↓
3. Update CHANGELOG
   ↓
4. Maintainer Review (2 people approval)
   ↓
5. Create Tag
   ↓
6. Publish to PyPI
   ↓
7. Create GitHub Release
   ↓
8. Community announcement
```

### Release Frequency

- **PATCH**: Anytime (bug fixes)
- **MINOR**: Once per month
- **MAJOR**: Once per quarter

---

## 🛡️ Conflict Resolution

### Dispute Handling Process

```
1. Parties negotiate
   ↓ (failed)
2. Maintainer mediation
   ↓ (failed)
3. Core maintainer arbitration
   ↓ (failed)
4. Community vote
```

### Code of Conduct

All community members must comply with [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

**Violation Handling**:
- First: Warning
- Second: Suspension (30 days)
- Third: Permanent ban

---

## 📝 Appendix

### Related Documents

- [README.md](README.md) - Project description
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) - Code of conduct
- [ROADMAP.md](ROADMAP.md) - Project roadmap
- [FOUNDER_STATEMENT.md](FOUNDER_STATEMENT.md) - Founder statement

### Contact

- GitHub: https://github.com/ad7007/taiji-api
- Issues: https://github.com/ad7007/taiji-api/issues
- Discussions: https://github.com/ad7007/taiji-api/discussions

---

**Last Updated**: 2026-03-18

**Version**: v1.0

**Approved By**: Community consensus

---

**Languages**: 
- [中文](GOVERNANCE.md) | [English](GOVERNANCE.en.md)
