function sendForm(event, message) {
    if (confirm(message)) {
        yourformelement.submit();
    } else {
        event.preventdefault();
        return false;
    }
}
