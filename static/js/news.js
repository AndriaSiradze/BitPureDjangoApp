document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.news-card').forEach(card => {
        card.addEventListener('click', e => {
            // if we clicked on any <a> inside the card (tags or the “Подробнее” link),
            // let the browser do its normal navigation
            if (e.target.closest('a')) return;
            // otherwise send the user to the article
            window.location = card.dataset.href;
        });
    });
});