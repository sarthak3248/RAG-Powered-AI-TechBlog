const startTime = Date.now();

window.addEventListener("beforeunload", function () {

    const duration = Math.floor(
        (Date.now() - startTime) / 1000
    );

    navigator.sendBeacon(
        readingSessionUrl,
        JSON.stringify({
            duration: duration
        })
    );

});