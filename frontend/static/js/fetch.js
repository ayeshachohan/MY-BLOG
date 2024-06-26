document.addEventListener('DOMContentLoaded', () => {
    // Example Fetch API usage for post creation
    document.getElementById('post-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const title = document.getElementById('title').value;
        const content = document.getElementById('content').value;

        const response = await fetch('/dashboard', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title, content })
        });

        if (response.ok) {
            window.location.reload();
        } else {
            alert('Failed to create post.');
        }
    });

    // Example Fetch API usage for post deletion
    document.querySelectorAll('form[action$="/delete"]').forEach(form => {
        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            const action = form.getAttribute('action');

            const response = await fetch(action, {
                method: 'POST'
            });

            if (response.ok) {
                window.location.reload();
            } else {
                alert('Failed to delete post.');
            }
        });
    });
});
