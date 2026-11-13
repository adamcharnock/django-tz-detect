(() => {
    'use strict';

    // Settings come from the data- attributes that tz_detect/detector.html
    // puts on this script tag; currentScript is only set while it runs.
    const {endpoint, csrfHeader, csrfToken, reload} = document.currentScript.dataset;

    if (!navigator.cookieEnabled) {
        // If cookies are disabled then storing the timezone in the user's
        // session is a hopeless task and will trigger a request for each
        // page load. Therefore, we shouldn't bother.
        return;
    }

    const offset = new Date().getTimezoneOffset();
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

    fetch(endpoint, {
        method: 'POST',
        headers: {
            [csrfHeader]: csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: new URLSearchParams({offset, timezone}),
    }).then((response) => {
        if (!response.ok) {
            return;
        }
        // Let the page react once the timezone is stored, e.g. refresh
        // date fragments with htmx: hx-trigger="tzdetect:set from:document".
        // A listener can call event.preventDefault() to cancel the reload.
        const proceed = document.dispatchEvent(new CustomEvent('tzdetect:set', {
            detail: {timezone, offset},
            cancelable: true,
        }));
        if (proceed && reload !== undefined && canReload()) {
            window.location.reload();
        }
    });

    function canReload() {
        try {
            const reloadedAt = Number(sessionStorage.getItem('tzdetect:reloaded'));
            // This page load was started by our own reload, yet the timezone had to be
            // detected again: the session cookie doesn't stick, so stop reloading this tab.
            if (performance.timeOrigin - reloadedAt < 5000) {
                sessionStorage.setItem('tzdetect:failed', '1');
            }
            if (sessionStorage.getItem('tzdetect:failed')) {
                return false;
            }
            sessionStorage.setItem('tzdetect:reloaded', String(Date.now()));
            return true;
        } catch {
            // sessionStorage unavailable: don't risk a reload loop.
            return false;
        }
    }
})();
