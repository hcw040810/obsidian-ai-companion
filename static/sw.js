// 观察者 Service Worker
const CACHE_NAME = 'observer-v2';
const STATIC_ASSETS = [
  '/',
  '/static/manifest.json',
];

// 安装：缓存静态资源
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

// 激活：清理旧缓存
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

// 请求拦截：网络优先，失败时用缓存
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // API 请求不缓存，直接走网络
  if (url.pathname.startsWith('/api/')) {
    return;
  }

  // 静态资源：网络优先，回退到缓存
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // 成功则更新缓存
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => {
          cache.put(event.request, clone);
        });
        return response;
      })
      .catch(() => {
        // 网络失败，用缓存
        return caches.match(event.request);
      })
  );
});
