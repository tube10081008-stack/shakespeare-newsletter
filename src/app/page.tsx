import Hero from '@/components/Hero';
import Features from '@/components/Features';
import NewsletterPreview from '@/components/NewsletterPreview';

export default function Home() {
  return (
    <main>
      <Hero />
      <Features />
      <NewsletterPreview />

      <footer style={{
        padding: '2rem',
        textAlign: 'center',
        color: 'var(--color-text-muted)',
        background: 'var(--color-background)',
        borderTop: '1px solid var(--color-border)'
      }}>
        <p>&copy; 2026 Shakespeare's Chronicle. All rights reserved.</p>
        <p style={{ fontSize: '0.8rem', marginTop: '0.5rem' }}>"온 세상이 무대다 (All the world's a stage)"</p>
      </footer>
    </main>
  );
}
