# Protected Release Notes

The current development build is intentionally open.

For an external release that must be password protected, do not implement a client-side JavaScript password gate because the source and protected content would remain downloadable.

Preferred release patterns:

1. edge authentication in front of the static site;
2. identity-aware access / single-use invite links;
3. server-side session authentication with rate limiting and secure cookies.

The protection layer should preserve deep links, keyboard accessibility, reduced-motion behavior and static asset delivery.
