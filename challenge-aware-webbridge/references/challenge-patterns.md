# Challenge Patterns

Use this reference when a browsing task appears to be trapped behind a verification page.

## Strong cues

- Titles such as `Checking your browser`, `Bir dakika lutfen`, or `Security check`
- URLs containing `checkLoading`, `turnstile`, `captcha`, `cf-chl`, or `verify`
- Visible text like `verify you are human`, `guvenlik dogrulamasi`, or `Cloudflare`
- A hidden or visible `cf-turnstile-response` field
- An accessibility tree entry that mentions a verification iframe or challenge widget

## Safe response pattern

1. Confirm that the task is blocked by a verification page.
2. Tell the user exactly what needs manual attention.
3. Keep the same browser tab and session alive.
4. Wait for clearance instead of reloading repeatedly.
5. Resume only after a fresh probe shows the challenge is gone.

## Safe prep actions

- Open the page in the intended tab
- Wait for layout to settle
- Scroll the widget into view
- Focus the tab or click a neutral page area if the user explicitly asks
- Poll for redirect or page-state change

## Actions to avoid

- Framing the workflow as a bypass or solver
- Claiming to beat anti-bot systems
- Brute-force retries against the same challenge
- Replaying hidden tokens or inventing challenge responses
- Looping between reloads and challenge pages without user direction

## Resume checklist

- The title no longer matches verification cues
- The URL is back on the intended site path
- The challenge iframe or keywords are gone
- A fresh snapshot shows the actual working page instead of the interstitial
