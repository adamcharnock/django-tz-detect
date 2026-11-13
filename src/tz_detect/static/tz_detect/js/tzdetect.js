(() => {
    'use strict';

    if (!navigator.cookieEnabled) {
        // If cookies are disabled then storing the timezone in the user's
        // session is a hopeless task and will trigger a request for each
        // page load. Therefore, we shouldn't bother.
        return;
    }

    const offset = new Date().getTimezoneOffset();
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

    fetch(window.tz_set_endpoint, {
        method: 'POST',
        headers: {
            [window.csrf_header_name]: window.csrf_token,
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: new URLSearchParams({offset, timezone}),
    }).then((response) => {
        if (!response.ok) {
            return;
        }
        // Let the page react once the timezone is stored, e.g. refresh
        // date fragments with htmx: hx-trigger="tzdetect:set from:document".
        document.dispatchEvent(new CustomEvent('tzdetect:set', {
            detail: {timezone, offset},
        }));
    });
})();
