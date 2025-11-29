/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  output: 'export', // Включаем статический экспорт для GitHub Pages
  basePath: process.env.NODE_ENV === 'production' ? '/hr-saas-mvp' : '',
  images: {
    unoptimized: true, // GitHub Pages не поддерживает оптимизацию изображений Next.js
  },
  trailingSlash: true, // Добавляем слэши в конце URL для лучшей совместимости
}

module.exports = nextConfig
