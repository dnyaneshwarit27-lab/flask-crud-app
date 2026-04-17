document.addEventListener('DOMContentLoaded', () => {
    // Automatically dismiss flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(msg => {
                msg.style.transition = 'opacity 0.5s ease-out';
                msg.style.opacity = '0';
                setTimeout(() => {
                    msg.remove();
                }, 500);
            });
        }, 5000);
    }
});
