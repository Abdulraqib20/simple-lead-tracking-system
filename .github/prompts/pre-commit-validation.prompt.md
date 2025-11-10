# 🚨 PRE-COMMIT VALIDATION PROMPT
**Vasily's Rule: "Filter them out before commit/pr"**

## Quick Pre-Commit Checklist:
- [ ] **User Approved**: Did the user explicitly request this?
- [ ] **Necessary**: Is this change actually needed?
- [ ] **Minimal**: Only changing what's absolutely required?
- [ ] **Safe**: Won't break existing functionality?

## Red Flags - STOP & ASK:
❌ >5 files changed
❌ Core architecture modifications
❌ New dependencies added
❌ Breaking changes introduced
❌ Configuration files modified
❌ Complex abstractions created

## Communication Required:
🤔 "This change affects [X], is that okay?"
🤔 "I'm considering [Y], should I proceed?"
🤔 "This might be overkill, want me to scale back?"

**Remember: Better to ask permission than beg forgiveness!** 🙏
