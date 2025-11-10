You are operating inside the Glucose monorepo. Before generating anything, read and summarize the project’s architecture and product context from the repository’s root `./documentation` directory (all files, diagrams, and specs). Derive naming conventions, tone, and core flows from this source only.

Your task: create WhatsApp Business message templates tailored to Glucose’s use case, with a priority on customer re‑engagement. Produce templates across the three official categories:

- Marketing
- Utility
- Authentication

If any category definitions, constraints, or formatting specifics are ambiguous, consult the latest official Meta documentation:

- [WhatsApp Manager – Message Templates](https://business.facebook.com/latest/whatsapp_manager)
- [Meta for Developers – WhatsApp Business App Console](https://developers.facebook.com)
- [Postman API Network – Status Message Failed Callback Error 470](https://www.postman.com/meta/whatsapp-business-platform/request/ezaux2n/status-message-failed-callback-error-470?tab=body)

## Inputs

- Repo path: `./documentation` (read this first)
- Focus: re‑engagement flows (win‑back, nudge, education), plus transactional utility and secure authentication
- Audience: customers interacting with Glucose via WhatsApp

## Output requirements (for each template)

- **Template name**: snake_case, versioned (e.g., `glucose_reengage_checkin_v1`)
- **Category**: Marketing | Utility | Authentication
- **Language**: English
- **Body text**: include variables {{1}}, {{2}}, etc. Keep under WhatsApp limits and policy
- **Variables doc**: what each variable represents (name, days since last reading, latest value, appointment date, OTP)
- **Suggested buttons**: up to 2, clear CTAs (e.g., “Log reading”, “Talk to coach”, “Confirm”)
- **Policy notes**: short justification that the template aligns with category rules
- **Example payload**: a Graph API JSON snippet illustrating how we’d send this template (with name, language, and sample variables)

## Guardrails

- Use empathetic, health‑supportive language; avoid spammy claims or unsupported medical advice
- No sensitive data in the template body unless clearly necessary and compliant (e.g., masked data)
- Keep Marketing templates genuinely value‑led (education, check‑ins, reminders), not pure promotion
- Ensure Authentication templates are concise and unambiguous (OTP, consent)
- Ensure Utility templates are transactional (updates, confirmations, reminders)

## Deliverables

- 5 Marketing templates optimized for re‑engagement (diverse angles: check‑in, streak recovery, education nudge, appointment follow‑up, milestone celebration)
- 4 Utility templates (reading reminders, report ready, appointment confirmation, feedback request)
- 2 Authentication templates (OTP, data‑sharing consent)
- A brief summary of Glucose context inferred from `./documentation`
- A mapping table between variables and backend fields (based on `./documentation`)
- Notes on policy alignment with links to sources

## Review checklist

- Variables defined and consistently named across templates
- Button labels are actionable and compliant
- Template names follow repo naming conventions inferred from `./documentation`
- Length fits WhatsApp template constraints
- Each template has a clear re‑engagement rationale

### Template Name: `glucose_service_evaluation_v1`
**Category:** Utility
**Language:** English
**Body Text:** "Hi {{1}}, your {{3}} service session is complete. Please confirm service completion to update our records."
**Variables Doc:**
- {{1}}: User's first name
- {{3}}: Current journey/product name
**Suggested Buttons:**
- "Confirm Complete"
- "Report Issue"
**Policy Notes:** This template handles mandatory service completion confirmation as part of operational record-keeping processes, ensuring transactional utility compliance through required administrative workflow completion.
**Example Payload:**
```json
{
  "name": "glucose_service_evaluation_v1",
  "language": "en",
  "components": [
    {
      "type": "BODY",
      "parameters": [
        { "type": "text", "text": "John" },
        { "type": "text", "text": "Premium Support" }
      ]
    },
    {
      "type": "BUTTONS",
      "buttons": [
        { "type": "QUICK_REPLY", "text": "Confirm Complete" },
        { "type": "QUICK_REPLY", "text": "Report Issue" }
      ]
    }
  ]
}
```

Now, read `./documentation`, summarize context in 4–6 bullet points, then generate the templates and payloads. If you need category specifics, consult the WhatsApp Manager and Meta docs linked above and apply them correctly. Provide links to any external policy references used.
