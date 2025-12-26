export const getMediaUrl = (url) => {
    if (!url) return null;

    // If it's already a relative path, return it
    if (url.startsWith('/')) return url;

    // If it's the internal docker container URL, strip it to make it relative
    // This allows Nginx to handle the /media/ path correctly
    if (url.includes('backend:8000')) {
        const path = url.split('backend:8000')[1];
        return path;
    }

    // If it's localhost (dev), keep it or adjust if needed
    // But in production, we want relative paths so Nginx serves them
    if (url.includes('localhost:8000')) {
        const path = url.split('localhost:8000')[1];
        return path;
    }

    return url;
};
